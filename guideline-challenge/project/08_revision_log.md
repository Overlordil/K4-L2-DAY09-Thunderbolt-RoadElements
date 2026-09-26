# Revision log

Guideline v1 = bản nháp đầu; v2 = sau calibration nội bộ; v3 = sau blind handoff. Mỗi lần tăng `Version` trong
`02_guideline.md`, thêm một hoặc nhiều dòng vào bảng: đổi gì và vì sao, kèm bằng chứng (sample_id, dòng
calibration report, câu hỏi trong clarification log, feedback của peer).

Cột Version ghi dạng `v1`, `v2`, `v3` — `make status` tìm dòng bảng có `v2` và dòng có `v3`.

| Version | Đổi gì | Vì sao | Bằng chứng |
|---|---|---|---|
| v1 | Tạo bản nháp đầu: định nghĩa `drivable_area` bằng polygon cho toàn bộ mặt đường hợp pháp trên tuyến ego; quy định các vùng loại trừ, cách xử lý che khuất và hai mức escalation (`needs_review`, `image_escalate`). | Module free-space/obstacle-avoidance cần phân biệt vùng xe có thể lái an toàn; một class và quy tắc không vẽ vùng loại trừ giữ schema gọn, còn escalation đánh dấu phần chưa đủ chắc chắn. | `01_problem_statement.md` (downstream contract, failure risk và scope); `03_ontology_and_cvat_setup.md` (rationale ontology, setup test); ví dụ `BDD05`, `BDD10`, `BDD11`, `BDD20` trong `02_guideline.md`. |
