# QA plan + quality gates

Không được viết "reviewer kiểm tra lại". Phải có sampling, metric, threshold và action khi fail. Thay mọi placeholder
mới là xong (gate G6).

## Flow

Guideline → Calibration → Production → Self-QC → Review → Rework → Quality Gate. Ghi cụ thể cho project của nhóm:

- **Ai review, review bao nhiêu:** 
  - Reviewer sẽ review (không phải chính annotator đã thực hiện annotation)
  - Review ngẫu nhiên 20% số ảnh, review 100% ảnh được đánh dấu high-risk (High-risk gồm:boundary của drivable area khó xác định;road bị che/khuất;drivable area bị cắt ở mép ảnh;boundary giữa drivable và non-drivable không rõ;vùng có bóng, phản chiếu hoặc ánh sáng gây ambiguity;annotation được annotator đánh dấu UNKNOWN) 
  - Với annotator mới: review 30% random sample
  - Nếu phát hiện Critical defect trong sample thì mở rộng review thành 100% batch.
- **Chọn sample theo rule nào**: 
  - Random baseline: chọn 20% ảnh trong batch bằng random sampling.
  - Risk-based sampling: bổ sung 100% ảnh có high-risk tag.
  - Không được thay random sample bằng việc chỉ chọn các ảnh dễ hoặc khó.
- **Issue được ghi ở đâu, đóng thế nào:** 
  1. Issue được ghi trong qa/qa_log.csv gồm các trường:
      - Image_id
      - Object_id
      - Annotator 
      - Reviewer 
      - Defect_type
      - Description 
      - Status
      - Rework_count
  2. Workflow: OPEN => REWORK => RESOLVED => VERIFIED => CLOSED
      - OPEN: reviewer phát hiện defect.
      - REWORK: annotation được trả về để sửa.
      - RESOLVED: annotator sửa xong và ghi done rework.
      - VERIFIED: reviewer xác nhận annotation sau rework đạt guideline.
      - CLOSED: không còn defect liên quan.
- **Khi phát hiện guideline gap thì update và version ra sao:** 
  1. Tạo Question / Guideline Gap.
  2. Không tự thêm rule ngoài guideline.
  3. Tạm dừng các annotation cùng loại.
  4. Spec owner và nhóm thống nhất cách xử lý.
  5. Cập nhật guideline.
  6. Tăng version.
  7. Ghi thay đổi vào 08_revision_log.md.
  8. Nếu rule mới ảnh hưởng annotation cũ, re-check các ảnh bị ảnh hưởng.
  9. Nếu thay đổi lớn về geometry hoặc output contract, calibration lại trước khi production tiếp tục.

## Defect severity

Nhóm được đổi mapping nếu downstream contract khác, nhưng phải giải thích và chốt trước khi QA.

| Severity | Định nghĩa cho project này | Ví dụ | Action mặc định |
|---|---|---|---|
| Critical | Annotation làm downstream không thể sử dụng đúng drivable area hoặc làm thay đổi nghiêm trọng semantic của vùng cần label | Bỏ toàn bộ drivable area rõ ràng; polygon nằm hoàn toàn ngoài drivable region | REWORK ngay + review 100% batch |
| Major | Lỗi làm sai đáng kể phạm vi drivable area nhưng vẫn có thể sửa theo guideline | Bỏ sót một phần lớn drivable area; polygon ăn sang non-drivable region đáng kể; boundary sai rõ ràng | REWORK + kiểm tra mở rộng nếu vượt threshold |
| Minor | Sai lệch nhỏ về geometry nhưng semantic của drivable area vẫn đúng | Boundary lệch nhẹ trong vùng tolerance; polygon chưa thật sát boundary nhưng vẫn thể hiện đúng vùng | REWORK trước khi PASS |
| Question | Bằng chứng không đủ hoặc guideline chưa có rule rõ ràng | Không xác định rõ boundary; vùng road bị che mạnh; trường hợp chưa được quy định | ESCALATE => chốt rule => update guideline/version => rework nếu cần |

## Metrics

| Metric | Cách tính | Vì sao phù hợp với bài toán |
|---|---|---|
| Critical Defect Rate | Critical defects / reviewed images | Theo dõi lỗi nghiêm trọng của drivable-area annotatio |
| Major Defect Rate | Major defects / reviewed images | Đo lỗi geometry/coverage đáng kể |
| Minor Defect Rate | Minor defects / reviewed images | Theo dõi consistency của boundary |
| Image Defect Rate | images with ≥1 defect / reviewed images | Đo tỷ lệ ảnh cần rework |
| Rework Rate | images requiring rework / production images | Đo chi phí QA |
| Guideline Gap Rate | Question issues / reviewed images | Phát hiện rule chưa đủ rõ |
| Critical Escape Rate | Critical defects found after gate / total Critical defects | Theo dõi Critical defect lọt qua QA |

Metric high-risk tách riêng (ví dụ critical defect escape rate): High-risk Critical Defect Rate = Critical defects in high-risk samples / Total high-risk samples reviewed

Threshold:
High-risk Critical Defect Rate = 0%
High-risk samples phải được review 100%.

## Quality gate

Threshold là đề xuất của nhóm, không phải chuẩn ngành. Giải thích trade-off cost/risk.

PASS if:

- Critical Defect Rate = 0%
- Critical Defect Escape Rate = 0%
- Major Defect Rate ≤ 5%
- Minor Defect Rate ≤ 10%
- High-risk Critical Defect Rate = 0%
- 100% high-risk samples đã được review
- Không còn issue OPEN hoặc REWORK
- Không còn Question ảnh hưởng đến annotation chưa được resolve
- Annotation sử dụng đúng guideline version của batch

REWORK if:

- Critical Defect Rate > 0%
- Major Defect Rate > 5%
- Minor Defect Rate > 10%
- Có high-risk sample chưa được review
- Có issue OPEN / REWORK
- Có guideline gap ảnh hưởng đến annotation
- Annotation không khớp guideline version

Action khi REWORK

1. Xác định defect.
2. Sửa annotation.
3. Nếu lỗi có tính hệ thống → review 100% batch.
4. Nếu nguyên nhân là guideline gap → update guideline + version.
5. Calibration lại nếu rule thay đổi.
6. Chạy lại QA.
7. Chạy lại Quality Gate.

REJECT / ESCALATE if:

- Critical defect vẫn còn sau rework.
- Critical defect lặp lại qua ≥2 vòng QA.
- Cùng lỗi xuất hiện có tính hệ thống trên nhiều batch.
- Guideline mâu thuẫn với downstream contract.
- Không thể resolve ambiguity bằng escalation path.
- Thay đổi geometry/output contract làm annotation hiện tại không còn hợp lệ.

Batch bị REJECT / ESCALATE không được đưa vào downstream dataset cho đến khi vấn đề được giải quyết.

Trade-off

Nhóm không review 100% toàn bộ production vì chi phí QA tăng theo số lượng ảnh. Thay vào đó: "20% random sampling + 100% high-risk sampling" để cân bằng giữa QA cost và risk of bad annotations.

- Random sampling giúp sample không bị thiên lệch về các ảnh mà reviewer chủ động chọn.
- Risk-based sampling tập trung nguồn lực vào các ảnh có boundary drivable khó.
- Critical threshold bằng 0% vì Critical defect có thể làm sai hoàn toàn downstream meaning.
- Major/Minor có threshold cao hơn để tránh việc QA phải review lại toàn bộ dataset chỉ vì những sai lệch nhỏ.
- Khi vượt threshold, chi phí review/rework tăng nhưng giảm rủi ro đưa annotation lỗi vào downstream dataset.

Decision

- PASS → Batch đạt Quality Gate và được đưa vào downstream dataset.
- REWORK → Batch bị giữ lại, sửa annotation và chạy lại QA + Quality Gate.
- REJECT / ESCALATE → Batch bị chặn khỏi downstream dataset cho đến khi defect hoặc specification issue được giải quyết.
