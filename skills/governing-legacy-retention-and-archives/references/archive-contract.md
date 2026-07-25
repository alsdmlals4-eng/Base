# Archive Retention Contract

## Authority before location

`backup`, `[백업]`, `archive`, `old`라는 경로명은 보존 위치만 설명한다. 현재 권한 제거는 다음을 모두 만족해야 성립한다.

1. 현재 정본이 별도 경로에 명시돼 있다.
2. Documentation Map·Registry·START_HERE가 archive를 현행 원본으로 읽지 않는다.
3. 구현 계획과 자동 Router가 archive 항목을 직접 선택하지 않는다.
4. Manifest가 `active_authority: false`, `implementation_authority: NONE`을 선언한다.
5. rollback ref와 검증 상태가 있다.

## Classification table

| 분류 | 적용 | 기본 처리 |
|---|---|---|
| `CURRENT_AUTHORITY` | 현재 책임 원본 | archive 금지 |
| `COMPATIBILITY_ONLY` | 과거 ID·경로 소비자가 남음 | inactive·alias·stub, direct route 금지 |
| `ARCHIVE_HISTORY` | 대체된 기획·계획·설명 | 원문 보존 + metadata + Manifest |
| `EVIDENCE_RETENTION` | 승인·테스트·결함·감사 증거 | 버전·실행 상태·주장 범위 보존 |
| `GENERATED_DERIVATIVE` | PDF·DOCX·diagram·export | source·generator·hash·freshness 기록 |
| `DELETE_PROHIBITED_SECRET` | token·credential·private key | revoke·remove; archive 금지 |
| `DELETE_APPROVED` | 고유 정보·소비자·복구 검증 완료 | 승인 범위에서 삭제 |
| `KEEP_UNRESOLVED` | 권한·고유성·참조 불명확 | 변경 금지, 조사 지속 |

## Metadata

문서 본문 상단 또는 Manifest에 동등한 정보를 기록한다.

```yaml
archive_metadata:
  status: SUPERSEDED
  archived_at: 2026-07-25
  original_path: docs/design/old-rule.md
  archived_path: docs/archive/superseded-design/old-rule.md
  superseded_by:
    - docs/design/current-rule.md
  reason: current-rule이 동일 책임을 승계함
  unique_material_preserved:
    - historical decision rationale
  active_authority: false
  implementation_authority: NONE
  compatibility_consumers: []
  rollback_ref: 0123456789abcdef0123456789abcdef01234567
```

승인 migration에서 알 수 없는 값은 빈 문자열이나 `TBD`가 아니라 `UNKNOWN`과 차단 사유를 사용한다.

## Documents and plans

- 원문을 보존하고 현재 관점에 맞게 과거 문장을 다시 쓰지 않는다.
- metadata header를 추가할 수 있지만 본문을 비우지 않는다.
- 활성 문서의 link와 backtick path는 현재 정본으로 바꾼다.
- archive 문서를 기본 cold start, current canon registry 또는 자동 실행 계획에 두지 않는다.

## Inactive Skills

과거 Skill ID·PR·학습 기록 소비자가 있으면 `COMPATIBILITY_ONLY`로 유지한다.

```text
status: inactive 또는 프로젝트의 BACKUP 호환 상태
load_by_default: false
routable: false
replaced_by: active-skill-id
```

물리 이동은 Registry, Router, alias, dependency, test와 문서 참조를 같은 변경에서 갱신할 때만 허용한다.

## Tests and evidence

- 실패를 숨기기 위해 테스트나 로그를 삭제하지 않는다.
- 실행 가능한 테스트가 현재 계약과 불일치하면 migrate, retire-with-rationale 또는 `KEEP_UNRESOLVED` 중 하나를 선택한다.
- 과거 증거에는 build, commit, seed, 환경, 실행 결과와 주장 범위를 기록한다.
- `NOT_RUN`을 `PASS`로 바꾸지 않는다.

## Generated derivatives

PDF, DOCX, diagram과 export는 source path, source commit 또는 input hash, generator·version, freshness status와 publication Manifest를 기록한다. stale derivative는 archive하거나 재생성하며 current로 표시하지 않는다.

## Code and runtime assets

활성 source tree에 도달 불가능 코드와 미사용 runtime asset을 장기 보존하지 않는다. 고유 구현은 Git history, tag, release 또는 별도 archival repository로 복구 가능하게 한 뒤 승인된 migration에서 제거한다. 대형 binary는 저장 비용·license·redistribution 계약을 별도로 검토한다.

## Secrets

API token, password, credential, private key, session cookie와 규제 데이터는 archive 대상이 아니다. 발견 즉시 revoke·rotate·remove 절차를 적용하며 사고 기록에 secret 원문을 복제하지 않는다.

## Branch and tag retention

branch는 폴더로 이동할 수 없다.

```text
unique commits audited
→ PR merged 또는 명시적 superseded close
→ 필요한 경우 archive tag 생성
→ tag와 target SHA 검증
→ delete capability와 승인 존재 시 branch 삭제
```

삭제 기능이 없으면 closed PR과 검증된 tag를 보존 증거로 사용하고 `branch deletion: NOT_RUN`으로 기록한다. 장기 `archive/*` branch는 기본 보존 방식으로 사용하지 않는다.

## Manifest verification

각 record는 고유 `archive_id`와 `current_path`를 사용한다. `superseded_by`는 존재하는 저장소 경로 또는 `external:` prefix를 가진다. Markdown 본문은 metadata를 제외하고도 비어 있지 않아야 한다. hash와 rollback ref는 실제 원문에 연결돼야 한다.

## Restore procedure

1. Manifest record와 rollback ref를 확인한다.
2. 원문 hash를 재검증한다.
3. 현재 정본·Schema·소비자와 충돌을 분석한다.
4. archive 파일을 직접 current로 복사하지 않고 별도 변경안으로 승계한다.
5. Registry·references·tests·cold start를 갱신한다.
6. 사용자 승인과 검증 뒤에만 현재 권한을 부여한다.
