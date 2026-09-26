# Peer feedback + owner response

Phần 1 do **nhóm peer** trả lời (gửi kèm file export). Phần 2 do **nhóm owner** điền. Thay mọi placeholder mới
là xong (gate G5).

- **Nhóm peer:** `Nhom09`
- **Người label blind:** `Nhom09` (peer annotator)

## 1. Peer trả lời

1. Rule nào rõ nhất / giúp quyết định nhanh nhất?
   - Vẽ xuyên qua xe/người đang chạy (Mục 6): khi thấy xe hoặc người di chuyển trên mặt đường, cứ vẽ polygon tiếp tục theo hướng đường, không mất công cắt tỉa viền quanh xe.
   - Chỉ có 1 class duy nhất `drivable_area` (Mục 4): gom hết làn xe chạy vào một khối, không cần phải phân loại các làn theo chiều/làn khác.

2. Rule nào mơ hồ hoặc phải tự suy diễn?
   - Có mâu thuẫn giữa Mục 2 và Mục 6: Mục 2 bảo xe tải chắn hết đường thì tách thành 2 polygon riêng, nhưng Mục 6 lại bảo xe cộ luôn vẽ xuyên qua. Khi gặp xe buýt/container chắn ngang ngã tư, annotator không biết nên cắt đôi hay vẽ xuyên.
   - Xe đỗ sát lề mà không có vạch kẻ cũng khó phân biệt: xe tắt máy đỗ cố định (phải né ra) hay xe tạm dừng chờ đèn/tắc đường (được vẽ xuyên qua) thì không rõ.

3. Sample nào khiến guideline "vỡ"?
   - `BDD24.jpg` (tuyết lầy lội): vệt bùn và gò tuyết không phân biệt được ranh giới tuyết mỏng với gò tuyết lấn đường; cố bóc mép tuyết khiến polygon bị vỡ, dễ sinh self-intersection.
   - `BDD26.jpg` (đêm, đường ướt loá đèn): mất hoàn toàn vạch đường thật do phản chiếu; annotator khó phân biệt giữa việc vẽ đại kèm `needs_review` và bỏ vẽ để gắn tag `image_escalate`.

4. Attribute / default nào trong CVAT dễ gây thao tác sai?
   - Checkbox `needs_review` mặc định `false`: nằm ẩn trong menu thuộc tính bên phải, vẽ xong bấm Save dễ quên bật khi ranh giới không đủ bằng chứng.
   - Tag `image_escalate`: thuộc cấp ảnh (Frame Tag), tách biệt hẳn với công cụ vẽ polygon nên annotator mới rất dễ không tìm ra chỗ bấm.

5. Một thay đổi cụ thể giúp annotator mới ít hỏi hơn?
   - Chốt dứt khoát ở Mục 2: mọi phương tiện giao thông di chuyển, kể cả xe buýt, xe tải lớn, container chắn ngang, đều luôn vẽ xuyên qua liên tục; chỉ tách 2 polygon khi gặp vật cản tĩnh cố định như dải phân cách bê tông hoặc công trường rào chắn.

## 2. Owner phân loại

Owner không tranh luận để bảo vệ guideline. Mỗi feedback và mỗi decision peer làm sai được xếp vào một hướng xử lý.

| Feedback / decision sai | Nguyên nhân (guideline gap / data ambiguity / execution error) | Xử lý (accept + revise / reject with evidence / add escalation rule) | Bằng chứng |
|---|---|---|---|
| Rule rõ nhất: vẽ xuyên qua xe/người đang chạy + `drivable_area` là class duy nhất | Không phải guideline gap; đây là rule mạnh nhất và đã đúng với downstream contract | Accept + revise | Mục 4 và Mục 6 trong `02_guideline.md`: `drivable_area` chỉ là 1 class và dynamic occlusion được vẽ xuyên qua; ví dụ `BDD05`, `BDD11` trong mục 9 cho thấy rule này thực tế ổn định |
| Rule mơ hồ: Mục 2 và Mục 6 không chốt rõ xe buýt/tải/container chắn ngang nên phải suy diễn | Guideline gap | Add escalation rule | Mục 2 định nghĩa "vật cản che khuất hoàn toàn ở giữa" nhưng không nêu rõ phương tiện di chuyển có được coi là vật cản tĩnh hay động; Mục 6 chỉ nói dynamic object mà không phân biệt loại phương tiện. Cần bổ sung quy tắc rõ như peer đề xuất |
| Sample `BDD24` và `BDD26` khiến guideline "vỡ" | Data ambiguity + guideline gap ở các trường hợp tuyết và phản chiếu | Add escalation rule | Mục 6 đã có phần `Tuyết phủ` và `Phản chiếu/loá`, nhưng peer vẫn thấy thiếu định nghĩa rõ ràng cho trường hợp mà vệt tuyết/ánh sáng làm ranh giới không phân biệt được; cần thêm ví dụ và cờ `needs_review` khi ranh giới không chắc |
| Checkbox `needs_review` và tag `image_escalate` dễ gây thao tác sai | Execution error | Accept + revise | `03_ontology_and_cvat_setup.md`/`03_cvat_labels.json` xác định `needs_review` là attribute và `image_escalate` là tag, nhưng UI/đặt vị trí tách biệt khiến annotator mới dễ bỏ sót. Nên bổ sung checklist trong task setup và phần hướng dẫn vận hành |
| Thay đổi cụ thể: quy định rõ mọi phương tiện di chuyển đều vẽ xuyên qua, chỉ tách polygon khi vật cản tĩnh cố định | Guideline gap | Accept + revise | Đây là sửa rule trực tiếp từ feedback peer, đúng với nguyên tắc ở Mục 6: dynamic object = semantic road surface, static object = visible-extent. Cần chèn câu rõ vào Mục 2 và Mục 6 để loại bỏ suy diễn |

