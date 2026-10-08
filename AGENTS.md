# AGENTS.md — agent AutoCAD / dung sai - nham be mat

Đây là thư mục config của **một con Pi riêng** chuyên thiết kế cơ khí.
Chạy bằng `run.cmd` (Windows) hoặc `./run.sh` (bash).

## Việc của agent này

Gợi ý **cấp chính xác (IT)** và **độ nhám bề mặt (Ra)** cho từng bề mặt chi tiết máy,
theo ISO 286 / TCVN 5707, kèm ký hiệu ghi lên bản vẽ và cảnh báo vượt khả năng gia công.

## Skill có sẵn

| Skill | Việc |
|---|---|
| `cad-tolerance` | gợi ý Ra/IT + nạp & tra tài liệu riêng |

Đọc `skills/cad-tolerance/SKILL.md` **trước khi** trả lời bất kỳ câu hỏi về dung sai/nhám.

## Lệnh thường dùng

```bash
python skills/cad-tolerance/scripts/rait.py suggest "lo lap o lan" --size 25
python skills/cad-tolerance/scripts/learn.py add "<duong dan tai lieu>"
python skills/cad-tolerance/scripts/learn.py search "<tu khoa>"
```

## Nguyên tắc

1. **Không bịa số** — trị số IT tra từ `data/iso286_it.csv`, không nhớ.
2. **Không rõ chức năng bề mặt thì hỏi lại**, đừng đoán.
3. **Tài liệu ở đâu học ở đó** — máy này chưa có tài liệu thì `learn.py add` trước,
   tra chéo rồi mới chốt. Mâu thuẫn với bảng mặc định → báo rõ, không im lặng chọn một bên.
4. **Mọi kết luận phải kèm căn cứ** (bảng nào / file nào / trang nào).
5. Việc xong phải chạy `--selftest` của script đã dùng, in `SELFTEST PASS` mới báo xong.
