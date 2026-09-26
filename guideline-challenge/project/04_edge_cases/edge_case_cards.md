# Edge-case library

Tối thiểu **8 card**, khuyến nghị 10–12. Một edge case tốt là case mà hai annotator hợp lý có thể làm khác nhau nếu
guideline chưa rõ. Tám ảnh dễ có label rõ ràng không được tính là edge-case library.

Cần có đủ độ đa dạng: occlusion / truncation / small-far · ambiguous semantics · conflicting road elements · **một case
critical-risk** · **một case guideline cho phép escalation**.

File này là kho nội bộ của nhóm, **không gửi cho peer**. Card dùng ảnh example/calibration thì chép rule + ví dụ sang
`02_guideline.md` (mục 7 và 9) để peer đọc được. Card về ảnh blind chỉ nằm ở đây, và decision của nó phải có trong
`gold_decisions.csv` trước `make freeze`.

`make status` đếm số dòng `CASE ID:` đã điền (đã thay placeholder). Copy khối dưới cho mỗi case.

---

CASE ID: TODO
Sample: TODO (sample_id)
Scene: TODO
Observation: TODO — thấy gì trong ảnh
Decision: TODO — LABEL / IGNORE / UNKNOWN / ESCALATE
Expected: TODO — class, attribute, geometry cụ thể
Rationale: TODO — gắn với downstream contract ở `01_problem_statement.md`
Common mistake: TODO
Diversity: TODO — occlusion / small_far / ambiguity / conflict / critical / escalation / …

---

CASE ID: CASE-01
Sample: BDD26
Scene: Đường phố ban đêm, có đảo giao thông nhỏ cạnh cột đèn.
Observation: Đảo giao thông hình tam giác nằm sát phần mặt đường; ánh sáng yếu làm mép đảo khó thấy.
Decision: IGNORE; ESCALATE nếu không xác định chắc mép đảo.
Expected: Vẽ `drivable_area` trên mặt đường lưu thông và không vẽ polygon phủ đảo; nếu mép đảo không rõ, bật `needs_review` trên polygon gần đó.
Rationale: Tính đảo cố định là vùng đi được có thể khiến module free-space đánh giá sai vùng an toàn cho xe.
Common mistake: Vẽ polygon phủ cả đảo vì bề mặt đảo và mặt đường đều tối, khó phân biệt.
Diversity: small_far;ambiguity;critical

CASE ID: CASE-02
Sample: BDD25
Scene: Đường phố lúc chạng vạng, mặt đường phản chiếu ánh sáng.
Observation: Ánh phản chiếu có thể giống vạch ranh giới; phía trước có dấu hiệu/làn dành cho xe đạp.
Decision: LABEL; ESCALATE nếu không phân biệt được ranh giới thật với phản chiếu.
Expected: Vẽ polygon theo vạch sơn thật hoặc mép vật lý; không bao gồm bike lane khi nhận diện được làn riêng; bật `needs_review` nếu ranh giới bị phản chiếu che lẫn.
Rationale: Nhận nhầm phản chiếu hoặc bike lane thành mặt đường xe chạy làm module tự hành ước lượng sai free-space hợp pháp.
Common mistake: Dùng vệt sáng phản chiếu làm ranh giới polygon hoặc gộp bike lane vào `drivable_area`.
Diversity: low_visibility;ambiguity;conflict

CASE ID: CASE-03
Sample: BDD24
Scene: Đường phố có tuyết.
Observation: Gò tuyết ven đường lấn vào phần mặt đường lưu thông và làm bề rộng đường còn lái được hẹp lại.
Decision: LABEL; ESCALATE nếu mép gò tuyết không đủ rõ để xác định.
Expected: Polygon dừng ở mép ngoài gò tuyết; không tính phần tuyết chất đống là `drivable_area`. Bật `needs_review` nếu mép gò bị hòa lẫn với mặt đường.
Rationale: Bao gồm gò tuyết như vùng đi được có thể khiến planner cho phép xe đi vào vùng bị cản trở.
Common mistake: Vẽ theo ranh giới mặt đường suy đoán bên dưới tuyết thay vì phần còn thực sự lái được.
Diversity: critical;low_visibility;ambiguity

CASE ID: CASE-04
Sample: BDD18
Scene: Đường phố ban đêm, có vạch qua đường và xe đậu hai bên.
Observation: Vạch qua đường nằm ở phần gần xe; xe đậu che khuất một phần mép đường.
Decision: LABEL; ESCALATE tại ranh giới bị che nếu không đủ bằng chứng.
Expected: Bao gồm vạch qua đường trong polygon `drivable_area`; không vẽ polygon lên xe hoặc vỉa hè. Chỉ nối qua phần bị xe che khi có bằng chứng rõ theo guideline; nếu ranh giới khuất, dừng polygon và bật `needs_review`.
Rationale: Cắt bỏ vạch qua đường làm vùng mặt đường bị đứt; đoán rộng qua vùng khuất có thể mở rộng free-space vào vùng không an toàn.
Common mistake: Loại vạch qua đường khỏi polygon, hoặc tự đoán ranh giới phía sau xe đậu.
Diversity: occlusion;low_visibility;ambiguity

CASE ID: CASE-05
Sample: BDD17
Scene: Đường phố ban ngày khi trời mưa.
Observation: Mặt đường ướt phản chiếu ánh sáng và vạch làn bị mờ.
Decision: LABEL; ESCALATE ở cấp polygon nếu ranh giới không phân biệt chắc chắn.
Expected: Vẽ phần mặt đường xác định được theo vạch sơn thật hoặc mép đường; không dùng vệt phản chiếu làm ranh giới. Bật `needs_review` trên polygon có ranh giới chưa chắc.
Rationale: Ranh giới sai trong mưa có thể làm module tránh chướng ngại tính thừa vùng xe có thể đi.
Common mistake: Coi vệt phản chiếu là vạch làn hoặc vẽ hết phần nhựa mà không xét ranh giới mờ.
Diversity: low_visibility;ambiguity;escalation

CASE ID: CASE-06
Sample: BDD16 (ứng viên; chưa có trong `sample_pack.csv`)
Scene: Cao tốc nhiều làn, trời âm u.
Observation: Các làn và mép mặt đường thu hẹp theo phối cảnh; ranh giới ở xa khó phân biệt hơn phần gần.
Decision: LABEL; ESCALATE ở cấp polygon khi ranh giới xa không còn đủ bằng chứng.
Expected: Vẽ polygon tới điểm cuối còn nhận diện được mặt đường; không kéo polygon sang lề/ngoài mép đường bằng suy đoán. Bật `needs_review` nếu ranh giới ở xa không rõ.
Rationale: Sai lệch ranh giới ở điểm xa làm module free-space ước lượng sai bề rộng hành lang xe có thể đi.
Common mistake: Kéo polygon tới tận điểm tụ hoặc cắt cụt quá sớm dù mặt đường vẫn còn nhận diện được.
Diversity: small_far;ambiguity;escalation

CASE ID: CASE-07
Sample: BDD13
Scene: Đường phố ban ngày, có vùng gạch chéo vàng ở giữa.
Observation: Vùng gạch chéo nằm trên mặt nhựa và trông liên tục với các làn đường hai bên.
Decision: IGNORE vùng gạch chéo.
Expected: Vẽ `drivable_area` trên các làn lưu thông; không vẽ polygon lên vùng gạch chéo/keep-clear.
Rationale: Vùng sơn này không dành cho xe chạy; đưa nó vào free-space có thể làm planner chọn vùng không được phép lưu thông.
Common mistake: Gộp toàn bộ mặt nhựa liên tục thành một polygon, bỏ qua vùng gạch chéo.
Diversity: conflict;critical

CASE ID: CASE-08
Sample: BDD11
Scene: Ngã tư khu dân cư, có vạch qua đường và người đi bộ ở góc phải.
Observation: Vạch qua đường nằm trên mặt đường; người đi bộ ở sát rìa khu vực giao cắt.
Decision: LABEL; ESCALATE nếu ranh giới mặt đường cạnh người đi bộ không rõ.
Expected: Polygon bao gồm mặt đường và vạch qua đường; không bao gồm người đi bộ hoặc vỉa hè. Bật `needs_review` nếu không xác định chắc mép đường gần người đi bộ.
Rationale: Bỏ vạch qua đường làm thiếu mặt đường hợp lệ; gộp người đi bộ/vỉa hè vào vùng này làm sai free-space cho obstacle-avoidance.
Common mistake: Cắt polygon theo hình từng vạch qua đường hoặc kéo polygon lên vỉa hè để nối vùng.
Diversity: occlusion;conflict;ambiguity
