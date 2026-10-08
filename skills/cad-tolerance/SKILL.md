---
name: cad-tolerance
description: Gợi ý CẤP CHÍNH XÁC (IT) và ĐỘ NHÁM BỀ MẶT (Ra) cho từng bề mặt chi tiết máy theo chuẩn ISO 286 / TCVN 5707 — tra bảng dung sai, tính sai lệch H/h, ký hiệu ghi trên bản vẽ, và cảnh báo khi yêu cầu vượt khả năng gia công. Kèm cơ chế nạp tài liệu riêng (learn) để tra chéo giáo trình. Dùng khi cần ghi dung sai/nhám lên bản vẽ, hỏi "bề mặt này Ra bao nhiêu / IT mấy", hoặc kiểm tra bản vẽ có hợp lý không.
license: MIT
allowed-tools: bash, read, write
metadata:
  version: 0.2.0
  purpose: "Gợi ý Ra/IT cho bề mặt chi tiết máy + nạp tài liệu tại chỗ + tự đẩy GitHub"
  dependencies: "python3 (khong can thu vien ngoai cho rait.py/autopush.py); learn.py: tuy dinh dang (pypdf/python-docx/easyocr)"
  tests: "bash:python scripts/rait.py --selftest && python scripts/learn.py --selftest && python scripts/autopush.py --selftest"
  triggers: "dung sai, IT, Ra, nhám bề mặt, độ bóng, ký hiệu nhám, lắp ghép, H7, h6, ISO 286, TCVN 5707, thiết kế máy, CAD, AutoCAD, mặt cắt, phát hiện mới, push github"
---

# CAD Tolerance — gợi ý Ra/IT cho bề mặt

Hai câu hỏi gốc: **bề mặt này cần cấp chính xác nào (IT)?** và **cần nhám bao nhiêu (Ra)?**
Trả lời bằng bảng chuẩn, kèm ký hiệu ghi lên bản vẽ + cảnh báo nếu vượt khả năng gia công.

## Công cụ

```bash
python scripts/rait.py suggest "lo lap o lan" --size 25
python scripts/rait.py suggest "mat lam kin dau" --size 40 --process "phay tinh"
python scripts/rait.py it --size 25 --grade 7
python scripts/rait.py ra --process "mài tinh"
python scripts/rait.py list
python scripts/rait.py --selftest          # phai in SELFTEST PASS

python scripts/learn.py add "<file hoac thu muc tai lieu>" [--recursive]
python scripts/learn.py search "nham be mat"
python scripts/learn.py list
python scripts/learn.py --selftest

python scripts/autopush.py status                  # co gi chua push
python scripts/autopush.py push                    # commit + push
python scripts/autopush.py note "<phat hien moi>"   # ghi findings/ roi push
python scripts/autopush.py watch --interval 1800   # tu push dinh ky
python scripts/autopush.py --selftest
```

## Quy trình gợi ý (5 bước, không bỏ bước)

1. **Xác định bề mặt + CHỨC NĂNG** — không hỏi "bề mặt này nhám bao nhiêu?" chung chung.
   Phải biết nó làm gì: lắp ổ lăn? làm kín? rãnh then? mặt kê? tự do?
   Chưa rõ chức năng → hỏi lại 1 câu, đừng đoán.
2. **Tra bảng** `rait.py suggest "<chức năng>" --size <mm>` → ra IT + Ra + miền dung sai.
3. **Tính trị số dung sai** từ bảng ISO 286-1 (script tự tra theo dải kích thước).
   Sai lệch giới hạn script chỉ tính cho miền **H** (lỗ cơ bản, EI=0) và **h** (trục cơ bản, es=0).
   Miền khác (k, m, n, p, f, g, js…) → **chỉ ghi ký hiệu**, muốn ra số phải tra bảng ISO 286-2.
4. **Kiểm tra khả năng gia công** — nếu biết phương pháp (`--process`), script tự cảnh báo
   khi yêu cầu Ra/IT chặt hơn khả năng. Có cảnh báo → **nói thẳng với người dùng**, đề xuất
   thêm bước tinh (mài/nghiền) hoặc hạ yêu cầu.
5. **Ghi lên bản vẽ** theo ISO 1302 / TCVN 5707, dạng:
   `⌀25H7 (+0.021/0)` · `⌀25k6` · nhám `▽0.8` (Ra 0.8 µm).

## Nguyên tắc cứng

- **Không bịa số.** Mọi trị số IT lấy từ `data/iso286_it.csv` (ISO 286-1). Không nhớ — tra.
- **Không tự bịa bảng chức năng.** `data/surface_ra.csv` là bảng kinh điển; nếu bề mặt không có
  trong bảng → nói "không có trong bảng" rồi mới đề xuất, và ghi rõ đó là suy luận.
- **Kiểm chứng bằng tài liệu của người dùng khi có.** Đã nạp tài liệu (`learn.py add`) thì
  `learn.py search` **trước**, lấy trích dẫn làm căn cứ; mâu thuẫn với bảng mặc định thì
  **báo rõ mâu thuẫn**, đừng im lặng chọn một bên.
- **Nhám quá thấp cũng là lỗi.** Ra quá nhỏ làm tăng giá thành vô ích; mặt ép gioăng nhám
  quá thấp còn không giữ được keo. Luôn nêu hệ quả giá thành.

## Tài liệu riêng (học tại máy đích)

Kho tri thức nằm ở `<repo>/knowledge/` (đổi bằng biến môi trường `CAD_KNOWLEDGE`).
Tài liệu ở đâu thì nạp ở đó — agent không mang sẵn tài liệu của máy khác.

```bash
python scripts/learn.py add "D:\tai_lieu\giao_trinh_cnctm.pdf"
python scripts/learn.py add "D:\tai_lieu\" --recursive
python scripts/learn.py search "do nham be mat"
```

Hỗ trợ: `.txt .md .csv .json` (đọc thẳng) · `.pdf` (pypdf) · `.docx` (python-docx) ·
ảnh `.jpg .png …` (OCR easyocr `vi`+`en`). Thiếu thư viện thì script nói rõ cần `pip install` gì.

## Bảng dữ liệu

| File | Nội dung | Nguồn |
|---|---|---|
| `data/iso286_it.csv` | trị số IT01…IT18 theo 13 dải kích thước | ISO 286-1 |
| `data/surface_ra.csv` | chức năng bề mặt → IT + Ra + kiểu lắp | bảng kinh điển giáo trình CNCTM |
| `data/process_ra.csv` | phương pháp gia công → Ra đạt được + IT tốt nhất | bảng kinh điển giáo trình CNCTM |

## Phát hiện mới → ghi lại rồi đẩy lên GitHub

Dùng khi thấy điều **chưa có** trong bảng/tài liệu: bảng thiếu một loại bề mặt, một ngưỡng Ra sai,
phương pháp gia công bị đánh giá sai…

```bash
python scripts/autopush.py note "<mô tả phát hiện + nguồn>"      # ghi findings/<ngày>.md rồi push
```

Nếu phát hiện là **quy tắc chung** (áp cho mọi lần sau) thì phải **sửa tầng dữ liệu**, không chỉ ghi note:

1. Sửa `data/surface_ra.csv` / `data/process_ra.csv` / `data/iso286_it.csv`, hoặc `SKILL.md`
   (bump `metadata.version` + thêm dòng vào `## Changelog`).
2. Chạy `python scripts/rait.py --selftest` — phải vẫn `SELFTEST PASS`.
3. `python scripts/autopush.py push`.

**Cấm** sửa bảng rồi để đó — không push là coi như chưa học được gì.

## Changelog

- **0.2.0** — thêm `autopush.py` (tự commit/push định kỳ + ghi phát hiện mới vào `findings/`);
  skill chạy trong agent **Phuoc_JR** (`.pi/agents/` 5 sub-agent + `MEMORY.md`).
- **0.1.0** — bản đầu: `rait.py` (suggest/it/ra/list + selftest) + `learn.py` (add/search/list/stats + selftest) + 3 bảng dữ liệu.
