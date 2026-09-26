# Annotation guideline — Drivable area trên ảnh BDD100K

**Version:** v1

## 1. Objective + scope

Gán nhãn vùng đường lái được để cung cấp input cho module free-space/obstacle-avoidance của ADAS/AV — xác định
toàn bộ mặt đường xe có thể lái vào một cách hợp pháp, không phân biệt làn ego đang đi hay làn cần đổi làn.

- **Trong scope:** mặt đường trải nhựa/bê tông thuộc cùng tuyến đường ego đang di chuyển, còn nhìn thấy trong
  khung hình — kể cả làn ego đang đi lẫn làn khác cùng chiều/ngược chiều lái được hợp pháp.
- **Ngoài scope (không vẽ gì cả):** bầu trời, nhà cửa, vỉa hè không nối liền mặt đường, biển báo/đèn tín hiệu,
  phương tiện, người đi bộ, và các vùng loại trừ dù trải nhựa/bê tông (gore, bike lane, làn đậu xe, lối vào tư
  nhân, đảo giao thông, lề đường — chi tiết ở mục 5).

## 2. Annotation unit

Đơn vị là **ảnh tĩnh** (image), gán nhãn theo **region**, không phải instance đếm được. Mỗi polygon là một vùng
liên tục thuộc cùng một class. Nếu vùng bị chia thành hai mảng rời nhau bởi vật cản che khuất hoàn toàn ở giữa
(ví dụ xe tải lớn chắn ngang hết bề rộng), vẽ **hai polygon riêng** — không nối bằng đường tưởng tượng xuyên qua
vật cản.

## 3. Geometry rule

- Hình dạng: **polygon**, tối thiểu 3 điểm.
- Đặt điểm sát mép vạch sơn làn hoặc mép mặt đường nhìn thấy (không amodal) — chỉ vẽ phần mặt đường thực sự nhìn
  thấy, trừ ngoại lệ mục 6 (occlusion tạm thời do xe/người di chuyển).
- **Tolerance:** lệch ≤ 5 px mỗi cạnh so với vạch/mép đường ở ảnh gốc 1280×720.
- Polygon chạm mép ảnh: đóng thẳng theo cạnh khung hình, không tự khép kín bên trong ảnh.

## 4. Taxonomy

| Name | Class/Attribute | Ý nghĩa |
|---|---|---|
| `drivable_area` | class (polygon) | Mọi phần mặt đường lái được hợp pháp thuộc tuyến đường ego đang di chuyển — làn ego đang đi và làn khác cùng chiều/ngược chiều, không phân biệt cần đổi làn hay không. |
| `needs_review` | attribute (checkbox, trên `drivable_area`) | Bật khi ranh giới polygon không đủ bằng chứng để quyết chắc chắn (mục 6, 7). |
| `image_escalate` | class (tag, cho cả ảnh) | Dùng khi không xác định được vùng lái an toàn ở mức tối thiểu để vẽ bất kỳ polygon nào đáng tin. |

Bảng đầy đủ (kèm CVAT type/default) ở `03_ontology_and_cvat_setup.md` — hai nơi phải khớp nhau.

**Vì sao class, vì sao attribute:** `drivable_area` là một class duy nhất vì downstream (free-space/tránh
chướng ngại) không cần phân biệt lane-change ngay ở bước annotation — mọi phần đường lái được hợp pháp đều xử lý
như nhau ở bước này. Không có class hay attribute riêng cho vùng loại trừ (gore, bike lane, làn đậu xe, lối vào
tư nhân, đảo giao thông, lề đường): **không vẽ polygon = không lái được**, đúng theo cách BDD100K gốc công bố
drivable area (chỉ 1 class, phần còn lại của ảnh mặc định không phải drivable). Danh sách cụ thể vùng nào bị loại
nằm ở mục 5 dưới dạng rule văn bản. `needs_review` là attribute vì nó là cờ tạm gắn lên một polygon đã vẽ, không
đổi ý nghĩa hình học/class của polygon đó.

## 5. Inclusion / exclusion

- **Bắt buộc label** (`drivable_area`): mọi mặt đường trải nhựa/bê tông còn nhìn thấy trong hành lang tuyến
  đường ego, kể cả phần bị xe/người đang di chuyển che tạm thời (mục 6), kể cả vạch qua đường/vạch dừng nằm trên
  mặt đường đó (không tách polygon riêng cho vạch qua đường).
- **Không vẽ gì cả (ngoài scope, kể cả khi trông giống mặt đường):** trời, nhà cửa, vỉa hè không nối liền mặt
  đường, biển báo, phương tiện, người đi bộ, **và các vùng loại trừ dù trải nhựa/bê tông**: gore/chevron gần exit
  ramp, bike lane có vạch/ký hiệu riêng, làn đậu xe có vạch riêng, lối vào bãi đỗ/tư nhân, đảo giao thông, lề
  đường không lưu thông. Không có label riêng cho các vùng này — **không vẽ polygon nghĩa là không lái được**.
  Nếu không chắc một vùng có thuộc danh sách loại trừ hay không, bật `needs_review` trên polygon `drivable_area`
  gần đó thay vì tự đoán.

## 6. Visibility / occlusion

- **Bị che bởi xe/người đang di chuyển (occlusion tạm thời — dynamic object):** vẫn vẽ polygon xuyên qua như
  đường tiếp tục bình thường, dựa vào bằng chứng hình học hai bên (vạch sơn, mép đường, hướng đường) để suy ra
  ranh giới hợp lý. Nhãn này biểu diễn mặt đường theo **ngữ nghĩa** (semantic road surface), bỏ qua occlusion
  tạm thời do giao thông — hệ thống nhận diện xe/người là input riêng biệt (object detection), annotator không
  cần đoán hình dạng dưới gầm xe, chỉ tiếp tục polygon theo xu hướng đường.
- **Bị che bởi vật thể tĩnh/lâu dài** (cây, cột, rào chắn công trình): theo **visible-extent** — polygon dừng ở
  ranh giới nhìn thấy cuối cùng, không đoán tiếp. Nếu phần còn lại không đủ bằng chứng để suy ra tiếp (ví dụ
  đường cong khuất hẳn sau công trình), dừng polygon và bật `needs_review`.
- **Nhỏ/xa** (mặt đường ở cuối tầm nhìn, gần điểm hội tụ phối cảnh): vẫn vẽ tới giới hạn còn phân biệt được là
  mặt đường; nếu ánh sáng yếu/ngược sáng khiến ranh giới ở xa không phân biệt được nữa, polygon dừng ở điểm cuối
  còn phân biệt và bật `needs_review`.
- **Phản chiếu/loá** (mặt đường ướt phản chiếu đèn, ngược sáng hoàng hôn): không tính vạch phản chiếu ảo là ranh
  giới; dùng vạch sơn thật hoặc mép vật lý mặt đường làm chuẩn. Không phân biệt được thật/ảo → bật `needs_review`.
- **Tuyết phủ:** tuyết mỏng còn thấy vạch/mép đường bên dưới → vẽ theo mặt đường suy luận được; tuyết chất đống
  thành gò lấn vào phần đường lưu thông → phần gò tuyết **không tính là drivable** (loại khỏi polygon dù về bản
  chất là mặt đường bị che, vì hiện tại không lái qua được); ranh giới polygon là mép ngoài gò tuyết.

## 7. Ambiguity / escalation

| Quyết định | Khi nào | Thể hiện trong CVAT |
|---|---|---|
| LABEL | Đủ bằng chứng hình học/ngữ cảnh để vẽ polygon `drivable_area` | Polygon với label `drivable_area` |
| IGNORE | Vùng thuộc danh sách loại trừ ở mục 5 (gore, bike lane, làn đậu xe, lối vào tư nhân, đảo giao thông, lề đường) | Không vẽ polygon ở vùng đó — absence of polygon là tín hiệu loại trừ |
| ESCALATE (object) | Ranh giới không chắc chắn, hoặc không chắc một vùng có thuộc danh sách loại trừ hay không (mục 6) | Checkbox `needs_review` = true trên polygon `drivable_area` gần đó |
| ESCALATE (cả ảnh) | Không xác định được vùng lái an toàn ở mức tối thiểu để vẽ bất kỳ polygon đáng tin nào (tuyết/đêm phủ gần hết cảnh) | Tag `image_escalate` cho ảnh |

Khi hai annotator hợp lý có thể chọn khác nhau và guideline không có rule rõ cho case đó: escalate, sau đó nhóm
bổ sung rule/ví dụ vào bản v2.

## 8. Temporal rule

Không áp dụng — task ảnh tĩnh, không dùng Track.

## 9. Examples

| sample_id | Thấy gì | Expected output | Rule áp dụng |
|---|---|---|---|
| BDD05 | Highway nhiều làn, xe thưa, làn rõ ràng | `drivable_area` bao trùm mọi làn cùng chiều còn nhìn thấy | Mục 3, mục 4 |
| BDD10 | Đường 2 chiều không dải phân cách, xe đậu 2 bên, có xe ngược chiều đang tới | `drivable_area` bao gồm cả làn ego lẫn làn ngược chiều còn nhìn thấy; không vẽ vào làn đậu xe | Mục 4, mục 5 |
| BDD11 | Ngã tư khu dân cư, vạch qua đường ngay trước xe, người đi bộ ở góc phải | `drivable_area` bao trùm cả phần vạch qua đường, không tách polygon riêng cho vạch qua đường | Mục 5, mục 6 |
| BDD20 | Khu dân cư, có cọc tiêu và một làn kẻ vạch riêng bên phải | Không vẽ polygon ở làn kẻ vạch riêng đó (IGNORE); `drivable_area` các làn còn lại | Mục 4, mục 5 |

## 10. Common mistakes

- Cắt polygon quanh từng xe đang di chuyển trên đường thay vì vẽ xuyên qua theo mục 6.
- Vẽ cả làn đậu xe/làn xe đạp/gore vào `drivable_area` vì "vẫn là mặt đường trải nhựa" — các vùng này không vẽ gì
  cả (mục 5), không phải một class khác.
- Bỏ sót làn ngược chiều hoặc làn cùng chiều bên cạnh vì chỉ chú ý vào làn ego đang đi.
- Đoán tiếp polygon qua khúc cua bị che khuất hoàn toàn thay vì dừng lại và bật `needs_review`.
- Không chắc một vùng có phải loại trừ hay không nhưng vẫn tự quyết (vẽ hoặc không vẽ) mà không bật
  `needs_review` — làm mất dấu vết để calibration/QA phát hiện bất đồng.
