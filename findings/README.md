# findings/ — tầng 2: PHÁT HIỆN MỚI

Nơi agent ghi điều mới phát hiện khi dùng: bảng thiếu loại bề mặt, ngưỡng Ra sai, phương pháp
gia công bị đánh giá sai, mâu thuẫn giữa tài liệu và bảng mặc định…

```bash
python skills/cad-tolerance/scripts/autopush.py note "<phát hiện + nguồn>"
```

Lệnh đó ghi 1 dòng vào `findings/<YYYY-MM-DD>.md` rồi **commit + push** lên GitHub.

Phát hiện là **quy tắc chung** → sửa luôn `skills/cad-tolerance/data/*.csv` hoặc `SKILL.md`
rồi `autopush.py push`. Chỉ ghi note mà không sửa bảng = chưa học được gì.
