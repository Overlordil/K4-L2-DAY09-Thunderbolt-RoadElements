# Ontology + CVAT setup

Bảng ontology là **source of truth** cho schema CVAT: `03_cvat_labels.json` phải khớp từng dòng ở đây. Thay mọi
placeholder mới là xong (gate G2).

## Ontology table

| Name | Geometry | Type (class / attribute) | Allowed values | Default | Mutable? | Rationale |
|---|---|---|---|---|---|---|
| `drivable_area` | polygon | class | — (object type) | — | false | Mọi mặt đường lái được hợp pháp thuộc tuyến ego. Chỉ 1 class duy nhất — theo đúng quy ước gốc của BDD100K, vùng không lái được đơn giản là không có polygon, không cần class loại trừ riêng |
| `needs_review` (attribute của `drivable_area`) | — | attribute (checkbox) | `false` | `false` | false | Escalation object-level khi ranh giới polygon không chắc |
| `image_escalate` | tag | class (tag cho cả ảnh) | — | — | false | Escalation cả ảnh khi không xác định được vùng lái an toàn |

## Class hay attribute

- `drivable_area` là **một class duy nhất**: downstream (free-space/tránh chướng ngại) chỉ cần biết "lái được hay
  không", không cần phân biệt loại vùng loại trừ (bike lane/parking/gore...) ở bước annotation này.
- Không có class hay attribute riêng cho vùng loại trừ: **absence of polygon = không lái được**, đúng theo cách
  BDD100K gốc công bố drivable area (chỉ 1 class, phần còn lại của ảnh mặc định không phải drivable). Danh sách cụ
  thể vùng nào bị loại (gore, bike lane, làn đậu xe, lối vào tư nhân, đảo giao thông, lề đường) nằm ở
  `02_guideline.md` mục 5 dưới dạng rule văn bản, annotator tuân theo khi quyết định có vẽ polygon hay không.
- `needs_review` là **attribute** (không phải class hay tag riêng) vì nó là cờ tạm gắn lên một polygon cụ thể đã
  vẽ, không đổi ý nghĩa hình học/class của polygon đó.
- **Đánh đổi đã chấp nhận:** vì không có label loại trừ riêng, export không phân biệt được "annotator cố tình
  không vẽ vùng X" với "annotator quên vẽ X". Nhóm chấp nhận rủi ro này để đổi lấy schema đơn giản, đúng chuẩn
  gốc; `needs_review`/`image_escalate` là van an toàn cho case annotator không chắc, còn case rõ ràng loại trừ
  (bike lane, gore...) dựa vào rule văn bản + calibration để phát hiện lệch.

## CVAT

- **Phiên bản CVAT** (`make cvat-status`): 2.75.1
- **Tên task calibration**: `day09` (task id 27, job id 16) — đặt tên chưa theo quy ước gợi ý
  `<tên nhóm>-calib-<tên bạn>` của GUIDE.md, nhưng không bắt buộc, chỉ là gợi ý đặt tên dễ tra cứu.
- **Guide của task đã dán `02_guideline.md`?** **Chưa** — kiểm tra trực tiếp trong CVAT (task id 27 chưa có Guide
  nào được lưu). Cần vào **Task → Task description → Edit**, dán toàn bộ nội dung `02_guideline.md`, **Submit**
  (xem GUIDE.md mục 2.3) trước khi coi bước setup là xong.
- **Nhóm dùng Track hay Shape, vì sao:** Shape — task dùng ảnh tĩnh BDD100K, không có chuỗi frame liên tục nên
  không áp dụng Track (xem mục 8 `02_guideline.md`).

## Setup test

Một thành viên `Nguyễn Văn Thịnh` mở task và trả lời: 
- label `drivable_area`
- dùng Polygon tool
- gán attribute `needs_review` cho polygon
- khi nào escalate : 
  - Một polygon: bật needs_review=true nếu ranh giới mờ/khuất, hoặc không chắc vùng đó là mặt đường hay vùng cần loại trừ. Ví dụ: phản chiếu che vạch thật, mép đường xa không rõ.
  - Cả ảnh: gắn tag image_escalate nếu gần như không thể xác định được vùng lái an toàn nào để vẽ, chẳng hạn tuyết hoặc bóng tối che phần lớn cảnh.
Ghi lại ai test và chỗ họ vấp:
- Tester: Nguyễn Văn Thịnh (chưa tham gia setup).
- Kết quả: Xác định được `drivable_area`, Polygon tool, `needs_review` và cách escalate.
- Chỗ vấp: Không có.
