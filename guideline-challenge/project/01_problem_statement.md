# Problem statement + downstream contract

Tối đa nửa trang, viết **trước khi mở CVAT**. Đây là bằng chứng của gate G1 (topic lock). Thay mọi placeholder
mới là xong.

## Bài toán

Phân loại vùng mặt đường lái được (**drivable_area**) trên ảnh tĩnh chụp từ camera trước xe — khó nhất ở khu dân
cư có xe đậu hai bên, vùng gạch chéo (gore) gần exit ramp, và điều kiện tuyết/đêm che khuất ranh giới làn.

## Downstream contract

1. **Downstream task / model / user là ai?** Module free-space / obstacle-avoidance của hệ thống ADAS/AV — cần
   biết toàn bộ vùng mặt đường xe có thể lái an toàn để giữ xe trong biên và tránh chướng ngại, không cần phân
   biệt làn nào là ego đang đi hay làn nào cần đổi làn.
2. **Output annotation nào thực sự cần?** Polygon 1 class duy nhất `drivable_area` mỗi ảnh. Vùng trông giống
   đường nhưng không được lái (gore, bike lane, làn đậu xe, lối vào tư nhân, đảo giao thông, lề đường) không có
   label riêng — không vẽ polygon ở đó là tín hiệu loại trừ, đúng theo quy ước gốc của BDD100K.
3. **Failure nào gây hậu quả lớn nhất?** Gán nhầm vùng không an toàn để lái (gò tuyết lấn làn, làn đậu xe, đảo
   giao thông, gore) thành `drivable_area` → planner cho phép xe đi vào vùng nguy hiểm. Đây là decision
   `critical` trong gold.
4. **Khi ambiguity không resolve được, ai / ở đâu là escalation path?** Attribute `needs_review` (checkbox) trên
   từng polygon khi ranh giới không đủ bằng chứng; tag `image_escalate` cho cả ảnh khi không thể xác định được
   vùng lái an toàn ở mức tối thiểu (tuyết/đêm phủ gần hết cảnh).

## Scope

- **Trong scope (bắt buộc label):** mọi mặt đường trải nhựa/bê tông thuộc tuyến đường ego đang di chuyển mà xe có
  thể lái vào một cách hợp pháp — bao gồm làn ego đang đi lẫn làn khác cùng chiều/ngược chiều còn nhìn thấy trong
  khung hình. Không phân biệt "ego đang đi" hay "cần đổi làn".
- **Ngoài scope (ignore):** vỉa hè, làn xe đạp, làn đậu xe có vạch riêng, lối vào bãi đỗ/tư nhân, đảo giao thông,
  vùng gạch chéo (gore/keep-clear), lề đường không dành cho lưu thông.
- **Geometry tolerance:** polygon bám theo vạch sơn/mép mặt đường nhìn thấy, lệch ≤ 5 px mỗi cạnh (ảnh gốc
  1280×720); không đoán phần bị che bởi vật thể tĩnh lâu dài, nhưng vẫn vẽ xuyên qua phần bị xe/người che tạm
  thời nếu đủ bằng chứng hình học hai bên để suy ra ranh giới.

## Output chấm được

LABEL (polygon `drivable_area`), IGNORE (không vẽ polygon ở vùng loại trừ — absence of polygon là tín hiệu),
ESCALATE object-level (`needs_review` = true) khi ranh giới hoặc việc loại trừ không chắc, ESCALATE cả ảnh (tag
`image_escalate`) khi cả cảnh không xác định được vùng lái an toàn. LABEL và ESCALATE nhìn thấy trực tiếp trong
file export CVAT (polygon, giá trị attribute, hoặc tag); IGNORE được suy ra từ việc không có polygon tại vùng đó
— đây là đánh đổi nhóm chấp nhận để giữ schema đơn giản (xem `03_ontology_and_cvat_setup.md` mục "Class hay
attribute").

## Dữ liệu và giới hạn

Toàn bộ ảnh lấy từ `data/bdd100k/` (26 ảnh, license BDD100K — giáo dục/nghiên cứu, xem `ATTRIBUTION.txt`). Không
dùng `lisa` (chỉ 1 clip 30 frame đèn giao thông, không liên quan drivable area) hay `gtsdb` (biển báo Đức, không
có drivable area). Giới hạn: chỉ 26 ảnh tĩnh, không có track nên không kiểm được tính nhất quán polygon qua thời
gian; scene chủ yếu đường Mỹ (vạch sơn/luật giao thông có thể khác chuẩn VN nếu áp dụng thực tế); số ảnh có tuyết
(2) và mưa (1) ít, hạn chế độ đa dạng case low-visibility.
