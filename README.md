# autocad-assistant 🔧📐

**Một con Pi riêng, chỉ để gợi ý DUNG SAI (IT) và ĐỘ NHÁM (Ra) cho bề mặt chi tiết máy** —
theo ISO 286 / TCVN 5707, có ký hiệu ghi lên bản vẽ, có cảnh báo khi yêu cầu vượt khả năng gia công.

Chỉ cần **Python** (không cần SolidWorks/AutoCAD để chạy phần tính toán).
Tài liệu riêng (giáo trình, sổ tay) **nạp tại máy đang dùng**, không mang sẵn từ máy khác.

Repo này vừa là **pi package** (cài vào Pi có sẵn), vừa là **agent dir độc lập** (chạy như một Pi riêng).

---

## 1. Lấy về

```bash
git clone https://github.com/tranbachthang/autocad.git
cd autocad
```

`rait.py` chạy bằng stdlib, cài thêm chỉ khi cần đọc tài liệu:

```bash
pip install pypdf python-docx easyocr
```

## 2. Cách sử dụng

### (A) Chạy như một con Pi riêng (khuyến nghị)

```cmd
run.cmd
```

rồi hỏi thẳng: *"mặt trụ Ø25 lắp ổ lăn thì ghi dung sai với nhám thế nào?"*

### (B) Cài vào Pi đang dùng

```bash
pi /install .            # hoặc trỏ skills trong settings.json tới ./skills
```

### (C) Gọi thẳng script (không cần AI)

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

## 3. Nạp tài liệu của bạn (học tại máy đích)

```bash
python skills/cad-tolerance/scripts/learn.py add "D:\tai_lieu\giao_trinh_cnctm.pdf"
python skills/cad-tolerance/scripts/learn.py add "D:\tai_lieu\" --recursive
python skills/cad-tolerance/scripts/learn.py search "do nham be mat"
python skills/cad-tolerance/scripts/learn.py list
```

Hỗ trợ `.txt .md .csv .json` · `.pdf` · `.docx` · ảnh (OCR `vi`+`en`).
Kho lưu ở `knowledge/` (bị `.gitignore`, **không** đẩy lên GitHub) — đổi bằng `CAD_KNOWLEDGE`.

## 4. Tự kiểm

```bash
python skills/cad-tolerance/scripts/rait.py --selftest    # SELFTEST PASS
python skills/cad-tolerance/scripts/learn.py --selftest   # SELFTEST PASS
```

## 5. Nội dung repo

```
autocad/
├─ run.cmd / run.sh                  # chạy như một Pi riêng
├─ settings.json, package.json       # khai báo pi package
├─ knowledge/                        # kho tài liệu nạp tại chỗ (rỗng khi clone)
└─ skills/cad-tolerance/
   ├─ SKILL.md                       # quy trình 5 bước + nguyên tắc
   ├─ data/iso286_it.csv             # bảng IT01..IT18 (ISO 286-1)
   ├─ data/surface_ra.csv            # chức năng bề mặt → IT + Ra
   ├─ data/process_ra.csv            # phương pháp gia công → Ra đạt được
   └─ scripts/{rait.py, learn.py}
```

## Nguồn dữ liệu

- Trị số IT: **ISO 286-1** (đối chiếu bảng công khai, xem header `data/iso286_it.csv`).
- Bảng chức năng → IT/Ra và phương pháp → Ra: **bảng kinh điển giáo trình Công nghệ chế tạo máy**
  (giá trị *điển hình* — khi đã nạp tài liệu riêng thì tra chéo trước khi chốt).

## Giới hạn đã biết (nói thẳng)

- Sai lệch giới hạn script **chỉ tính cho miền H (lỗ cơ bản) và h (trục cơ bản)**.
  Miền khác (k, m, n, p, f, g, js…) script chỉ ghi **ký hiệu**; ra số phải tra bảng ISO 286-2.
- Bảng chỉ phủ **Ø0–500 mm**, 13 dải kích thước.
- `learn.py` **chưa OCR được PDF scan** (nó báo rõ khi phát hiện) — chuyển PDF thành ảnh rồi nạp ảnh.
- Chưa nối trực tiếp vào AutoCAD (chưa đọc/ghi `.dwg`).

## License

MIT — xem `LICENSE`.
