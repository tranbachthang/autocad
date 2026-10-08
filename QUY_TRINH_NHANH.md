# Quy trình nhanh — Phuoc_JR

> Mở file này khi cần làm nhanh. Mỗi việc 1-2 lệnh.

## 0. Biến chung

- `PY="python"` — máy nào cũng dùng được; **đừng hardcode** `C:\Users\...\python.exe` của máy khác.
- Trên console Windows đặt `PYTHONIOENCODING=utf-8` để in được tiếng Việt.
- Luôn chạy lệnh **từ thư mục repo** (chỗ có `skills/`).

## 1. Gợi ý nhanh cho 1 bề mặt

```bash
$PY skills/cad-tolerance/scripts/rait.py suggest "lo lap o lan" --size 25
$PY skills/cad-tolerance/scripts/rait.py suggest "mat lam kin dau" --size 40 --process "phay tinh"
```

Đọc kết quả: `Cap chinh xac`, `Do nham goi y`, `Mien dung sai`, `GHI TREN BAN VE`, và **mọi dòng `✗ CANH BAO`**.

## 2. Tra 1 trị số dung sai

```bash
$PY skills/cad-tolerance/scripts/rait.py it --size 25 --grade 7     # -> 21 um
```

## 3. Kiểm phương pháp gia công có đạt không

```bash
$PY skills/cad-tolerance/scripts/rait.py ra --process "mài tinh"
```

## 4. Nạp tài liệu rồi tra lại

```bash
$PY skills/cad-tolerance/scripts/learn.py add "D:\tai_lieu\giao_trinh.pdf"
$PY skills/cad-tolerance/scripts/learn.py search "do nham be mat"
```

## 5. Việc dài / nhiều bề mặt → pipeline 5 agent

Gọi tool `subagent` với `agentScope: "both"`: `cad-planner` → `cad-critic` → `cad-worker`
→ `cad-critic` (thanh tra) → `cad-verifier`. Ngưỡng đạt 8/10.

## 6. Có phát hiện mới → ghi + đẩy lên GitHub

```bash
$PY skills/cad-tolerance/scripts/autopush.py note "mat phang ep gioang nen ghi Ra 3.2 chu khong phai 0.8"
```

Lệnh này ghi vào `findings/<ngày>.md` rồi commit + push.
Nếu phát hiện là **quy tắc chung** → sửa `skills/cad-tolerance/data/*.csv` hoặc `SKILL.md` trước, rồi `autopush.py push`.

## 7. Trước khi báo "xong"

- [ ] Trị số lấy từ `rait.py` (không phải nhớ).
- [ ] Kích thước rơi đúng dải (Ø25 → 18–30).
- [ ] Đã đọc và xử lý mọi dòng `✗ CANH BAO`.
- [ ] Đã chạy `--selftest` của script vừa dùng → `SELFTEST PASS`.
- [ ] Ghi 1 dòng vào `.pi/agents/MEMORY.md` (việc tầng M/L).
