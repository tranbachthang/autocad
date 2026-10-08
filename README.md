# Phuoc_JR 🔧📐 — trợ lý AI thiết kế cơ khí

**Một con Pi riêng, chuyên gợi ý DUNG SAI (IT) và ĐỘ NHÁM (Ra) cho bề mặt chi tiết máy** —
theo ISO 286 / TCVN 5707, có ký hiệu ghi lên bản vẽ, có cảnh báo khi yêu cầu vượt khả năng gia công.

Chỉ cần **Python** (không cần AutoCAD/SolidWorks để chạy phần tính toán).
Tài liệu riêng (giáo trình, sổ tay) **nạp tại máy đang dùng** — không mang sẵn từ máy khác.

Repo vừa là **pi package**, vừa là **agent dir độc lập** (chạy như một Pi riêng), vừa có
**giao diện chat web local** và **pipeline 5 agent**.

---

## 1. Cài đặt (1 lần)

```cmd
CaiDat.bat
```

Tự cài: Node.js → Git → Python → thư viện (`pypdf`, `python-docx`, `easyocr`) → `pi`.
Cần quyền admin thì chuột phải → *Run as administrator*. Gỡ bằng `GoCaiDat.bat`.

## 2. Chạy

| Cách | Lệnh |
|---|---|
| **Giao diện chat** (kiểu Claude/Gemini) | `MoGiaoDien.bat` → `http://127.0.0.1:8766` |
| **Terminal** | `ChayAI.bat` |
| **Gọi script trực tiếp** (không cần AI) | xem mục 3 |

Lần đầu: gõ `/login` → chọn DeepSeek → dán API key.

Ví dụ câu hỏi:
> mặt trụ Ø25 lắp ổ lăn thì ghi dung sai với nhám thế nào

## 3. Gọi thẳng script (không cần AI)

```bash
python skills/cad-tolerance/scripts/rait.py suggest "lo lap o lan" --size 25
python skills/cad-tolerance/scripts/rait.py suggest "mat lam kin dau" --size 40 --process "phay tinh"
python skills/cad-tolerance/scripts/rait.py it --size 25 --grade 7
python skills/cad-tolerance/scripts/rait.py ra --process "mài tinh"
python skills/cad-tolerance/scripts/rait.py list
```

Ví dụ kết quả:

```
Chuc nang     : Mặt lắp ổ lăn (trên trục)
Cap chinh xac : IT6
Do nham goi y : Ra 0.4 - 0.8 um (▽0.8)
Mien dung sai : k6 | js6 | m6
Tri so dung sai: 13 um  (0.013 mm)  [ISO 286-1]
GHI TREN BAN VE: ⌀25k6  (tra bang ISO 286-2 cho mien 'k6')  Ra 0.4 - 0.8 um (▽0.8)
```

## 4. Nạp tài liệu của bạn (học tại máy đích)

```bash
python skills/cad-tolerance/scripts/learn.py add "D:\tai_lieu\giao_trinh_cnctm.pdf"
python skills/cad-tolerance/scripts/learn.py add "D:\tai_lieu\" --recursive
python skills/cad-tolerance/scripts/learn.py search "do nham be mat"
```

Hỗ trợ `.txt .md .csv .json` · `.pdf` · `.docx` · ảnh (OCR `vi`+`en`).

## 5. Tự push lên GitHub

```bash
python skills/cad-tolerance/scripts/autopush.py status                 # có gì chưa push
python skills/cad-tolerance/scripts/autopush.py push                   # commit + push
python skills/cad-tolerance/scripts/autopush.py note "<phát hiện mới>" # ghi findings/ rồi push
python skills/cad-tolerance/scripts/autopush.py watch --interval 1800  # tự push mỗi 30 phút
```

Muốn chạy nền theo lịch (tự push định kỳ) — mở **PowerShell** và đăng ký 1 lần:

```powershell
schtasks /create /tn "PhuocJR-AutoPush" /sc minute /mo 30 /tr "python \"C:\duong\dan\autocad\skills\cad-tolerance\scripts\autopush.py\" push"
```

## 6. Pipeline 5 agent

Gọi bằng tool `subagent` với `agentScope: "both"`: `cad-planner` → `cad-critic` → `cad-worker`
→ `cad-critic` (thanh tra) → `cad-verifier`. Ngưỡng đạt **8/10**. Chi tiết: `AGENTS.md`.

## 7. Chia bộ nhớ (4 tầng)

| Tầng | Nơi lưu | Nhớ gì | Push lên GitHub |
|---|---|---|---|
| 1. Tri thức | `knowledge/` | tài liệu đã nạp | ❌ (giữ ở máy đang dùng) |
| 2. Phát hiện | `findings/` | điều mới phát hiện khi dùng | ✅ |
| 3. Nhật ký agent | `.pi/agents/MEMORY.md` | mỗi việc 1 dòng | ✅ |
| 4. Bảng chuẩn | `skills/cad-tolerance/data/` | ISO 286 (IT), chức năng→Ra, phương pháp→Ra | ✅ |

## 8. Cấu trúc repo

```
autocad/
├─ CaiDat.bat / ChayAI.bat / GoCaiDat.bat / MoGiaoDien.bat
├─ giao_dien.py / giao_dien.html          # chat UI web local (port 8766)
├─ AGENTS.md                              # persona Phuoc_JR + chia bộ nhớ + pipeline
├─ QUY_TRINH_NHANH.md / KE_HOACH.md
├─ .pi/agents/                            # 5 sub-agent + MEMORY.md
├─ extensions/subagent/                   # extension gọi sub-agent
├─ knowledge/                             # tầng 1 (rỗng khi clone)
├─ findings/                              # tầng 2 (phát hiện mới)
└─ skills/cad-tolerance/
   ├─ SKILL.md
   ├─ data/iso286_it.csv                  # bảng IT01..IT18 (ISO 286-1)
   ├─ data/surface_ra.csv                 # chức năng bề mặt → IT + Ra
   ├─ data/process_ra.csv                 # phương pháp gia công → Ra
   └─ scripts/{rait.py, learn.py, autopush.py}
```

## 9. Tự kiểm

```bash
python skills/cad-tolerance/scripts/rait.py --selftest       # SELFTEST PASS
python skills/cad-tolerance/scripts/learn.py --selftest      # SELFTEST PASS
python skills/cad-tolerance/scripts/autopush.py --selftest   # SELFTEST PASS
```

## 10. Giới hạn đã biết (nói thẳng)

- Sai lệch giới hạn script **chỉ tính cho miền H (lỗ cơ bản) và h (trục cơ bản)**; miền khác
  (k, m, n, p, f, g, js…) script chỉ ghi **ký hiệu** — ra số phải tra bảng ISO 286-2.
- Bảng phủ **Ø0–500 mm**, 13 dải kích thước.
- `learn.py` **chưa OCR được PDF scan** (nó báo rõ khi phát hiện) — chuyển PDF thành ảnh rồi nạp ảnh.
- Chưa nối trực tiếp vào AutoCAD (chưa đọc/ghi `.dwg`).

## Nguồn dữ liệu

- Trị số IT: **ISO 286-1** (bảng công khai, đối chiếu chéo — xem header `data/iso286_it.csv`).
- Bảng chức năng → IT/Ra và phương pháp → Ra: **bảng kinh điển giáo trình Công nghệ chế tạo máy**
  (giá trị *điển hình* — khi đã nạp tài liệu riêng thì tra chéo trước khi chốt).

## License

MIT — xem `LICENSE`.
