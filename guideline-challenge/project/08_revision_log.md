# Revision log

Guideline v1 = bản nháp đầu; v2 = sau calibration nội bộ; v3 = sau blind handoff. Mỗi lần tăng `Version` trong
`02_guideline.md`, thêm một hoặc nhiều dòng vào bảng: đổi gì và vì sao, kèm bằng chứng (sample_id, dòng
calibration report, câu hỏi trong clarification log, feedback của peer).

Cột Version ghi dạng `v1`, `v2`, `v3` — `make status` tìm dòng bảng có `v2` và dòng có `v3`.

| Version | Đổi gì | Vì sao | Bằng chứng |
|---|---|---|---|
| v2 | Thêm rule mật độ điểm tối thiểu khi vẽ theo đường cong/chướng ngại vật (mục 3); thêm rule vùng foreground ngay trước đầu xe vẫn tính drivable_area (mục 5); thêm ví dụ BDD17 (góc ranh giới hẹp) và BDD23 (đường rộng nhiều làn, gold-standard) vào mục 9; thêm 3 lỗi thường gặp mới vào mục 10 | Calibration nội bộ giữa loc và phucai trên 5 ảnh cho thấy 4/5 case là `guideline_gap`: BDD07/BDD17 lệch mật độ điểm (IoU 0.92–0.93, không sai vùng nhưng rule chưa quy định mật độ điểm); BDD20 bỏ sót vùng foreground; BDD23 bỏ sót gần nửa đường rộng (IoU 0.42, đáng kể nhất) | `06_calibration_measure.csv`, `06_calibration_report.csv` (5 dòng, sample_id BDD07/BDD17/BDD20/BDD22/BDD23) |
