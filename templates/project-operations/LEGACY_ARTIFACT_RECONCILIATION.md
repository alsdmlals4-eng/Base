# 구형 파일·파생본 정리표

## 작업 계약

```yaml
repository:
canonical_baseline:
work_mode: PLAN/BUILD/REVIEW
approval_ref:
rollback_ref:
```

## 판정 값

- `CURRENT`: 현행 정본이며 유지한다.
- `UPDATE_IN_PLACE`: 경로는 유지하고 내용을 최신 정본에 맞춘다.
- `MERGE_TO_CANONICAL`: 고유 정보를 현행 정본으로 승계한 뒤 구형본을 종료한다.
- `COMPATIBILITY_STUB`: 외부 참조를 위해 새 경로 안내만 남긴다.
- `ARCHIVE_HISTORY`: 실행 경로에서 제외하고 역사 기록으로 보존한다.
- `DELETE_APPROVED`: 고유 정보·참조·복구·승인이 확인돼 삭제한다.
- `KEEP_UNRESOLVED`: 충돌·소유권·참조가 불명확해 유지한다.

## 파일별 처리표

| 구형 경로 | 추정 버전·상태 | 현행 정본 | 고유 정보 | 활성 참조 | 파생본·Manifest | 판정 | 승인 | 처리·검증 | 롤백 |
|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |

## 정리 순서

```text
인벤토리·해시·참조 수집
→ 현행 정본 판정
→ 고유 정보·결정·예외·이미지·보류 승계
→ 충돌·미확정 분리
→ UPDATE / MERGE / STUB / ARCHIVE / DELETE 승인
→ 참조·Registry·생성기·테스트·발행본 갱신
→ 원본 처리
→ reference-freshness·회귀·복구 검증
```

## 삭제 게이트

- [ ] 구형 파일의 고유 정보·이미지·예외·보류를 승계했다.
- [ ] 활성 코드·문서·Workflow·템플릿·테스트·외부 링크를 갱신했다.
- [ ] 파생 PDF·DOCX·Manifest·해시를 갱신하거나 종료했다.
- [ ] Git 이력·태그·백업 등 복구 경로가 있다.
- [ ] 사용자 또는 승인된 작업 계약의 삭제 근거가 있다.
- [ ] `auditing-canonical-reference-freshness` 결과에 차단 finding이 없다.

## 결과

```yaml
updated: []
merged: []
compatibility_stubs: []
archived: []
deleted: []
kept_unresolved: []
remaining_stale_references: []
verification:
rollback:
```
