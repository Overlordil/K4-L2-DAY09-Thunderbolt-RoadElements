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
| Critical | TODO | TODO | TODO |
| Major | TODO | TODO | TODO |
| Minor | TODO | TODO | TODO |
| Question | TODO | TODO | TODO |

## Metrics

| Metric | Cách tính | Vì sao phù hợp với bài toán |
|---|---|---|
| TODO | TODO | TODO |

Metric high-risk tách riêng (ví dụ critical defect escape rate): TODO

## Quality gate

Threshold là đề xuất của nhóm, không phải chuẩn ngành. Giải thích trade-off cost/risk.

```text
PASS if:
  TODO
REWORK if: TODO
REJECT / ESCALATE if: TODO
```

Trade-off: TODO
