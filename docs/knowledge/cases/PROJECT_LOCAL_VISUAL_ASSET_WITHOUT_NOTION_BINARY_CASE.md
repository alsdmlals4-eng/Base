# Project-local Visual Asset Without Notion Binary — Case

```text
NOTION_BINARY_IS_NOT_REQUIRED_FOR_PROJECT_OWNED_VISUAL_BYTES
LOCAL_ONLY_IS_NOT_DURABLE_HANDOFF
CANDIDATE_FRESHNESS_FOLLOWS_PLAYER_FACING_BYTES
```

## 1. 문제

Work에서 이미지를 만들 수 있고 로컬 프로젝트 filesystem에 직접 저장할 수 있는데도 모든 이미지 binary를 Notion에 다시 업로드·attach·readback하면 다음 비용이 반복된다.

- 동일 bytes의 중복 저장과 상태 동기화
- Work→Notion→Codex 전달 단계 증가
- attachment capability·렌더링·업로드 실패로 current Slice가 불필요하게 정지
- Notion record와 repository/runtime asset identity drift

반대로 이미지를 local-only 후보로만 두면 새 Work·remote Codex·GitHub Actions·다른 PC가 해당 bytes를 볼 수 없고, Scene/Resource가 local path를 참조할 경우 제품이 깨진다.

## 2. 비교한 대안

| 대안 | 장점 | 실패 모드 | 판정 |
|---|---|---|---|
| Notion binary + local/repository 중복 | 사람에게 직접 보이고 기존 Notion workflow와 호환 | duplicate truth, upload/readback 지연, attachment/runtime identity drift | **REJECT as required default**. Project가 명시적으로 요구할 때만 사용 |
| local-only untracked image | 가장 빠른 생성·검토 | Codex/CI/new session에 durable하지 않음, local path dependency | **REJECT for implementation handoff** |
| project-local candidate → 승인 후 tracked project asset + manifest | 로컬 생성 속도와 repository durability를 함께 확보 | promotion·manifest·Git readback Gate가 필요 | **ADOPT** |

## 3. 기존 해결 우선

새 Asset system을 만들지 않았다. Base에는 이미 다음 owner가 있었다.

- `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`
- `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`

따라서 새 broad Skill·provider·SaaS 대신 explicit user delegation에만 적용되는 좁은 delivery adapter로 결합했다.

## 4. 최종 패턴

```text
Notion Home / Visual Bible / Asset Catalog fresh-read
→ actual consumer + current Art Direction
→ local GPT가 exact project root의 candidate path에 직접 저장
→ existence / dimensions / format / SHA-256 readback
→ local preview/import
→ PROJECT_ASSET_APPROVED
→ tracked project path로 promote
→ ASSET_MANIFEST.yml + provenance/rights
→ feature branch commit/push + remote readback
→ Codex consumes project-relative path + exact commit
→ import/runtime/screen evidence
```

Notion은 사람용 구조·방향·상태 요약을 계속 제공할 수 있지만 binary upload는 explicit project policy가 요구하지 않는 한 완료 필수조건이 아니다.

## 5. Godot·Git 경계

### Godot

공식 Godot 문서에서 source asset은 project folder 안에 두며 `.godot/` 내부 imported cache는 source-control 대상과 분리된다.

- Project organization: https://docs.godotengine.org/en/stable/tutorials/best_practices/project_organization.html
- Import process: https://docs.godotengine.org/en/latest/tutorials/assets_pipeline/import_process.html

```text
IMPORT_CACHE_DIFF != PRODUCT_SOURCE_DIFF
```

`*.import`, `*.uid`의 의미는 engine version과 current Project tracking policy를 확인한다. 공용 Base에서 확장자만 보고 일괄 commit 금지·허용하지 않는다.

### Git / LFS

Git LFS는 binary 내용을 pointer로 대체하는 유효한 선택이지만 repository storage/bandwidth·checkout/toolchain 계약이 추가된다.

- Git LFS: https://git-lfs.com/
- GitHub LFS: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage

따라서 일반 project image에 LFS를 자동 강제하지 않고 current repository policy·file size·history impact·quota·Codex/CI 호환성을 비교한다.

## 6. Candidate freshness

패키지·runtime screenshot·visual QA candidate는 생성 당시 exact player-facing bytes에만 유효하다.

다음이 바뀌면 영향 candidate를 `HISTORICAL_SUPERSEDED_BY_PRODUCT_BYTE_CHANGE`로 내린다.

- code/Scene/Resource/data/localization
- 실제 소비 asset bytes/path/import setting
- HUD/renderer/player-facing feedback
- export/package setting

도구·테스트·문서만 바뀌고 product/package bytes와 claim 의미가 같으면 자동 무효화하지 않는다.

## 7. CI 증거

```text
TEST_LOGIC_PASS != CI_GATE_PASS
```

테스트 로직이 통과해도 workflow parser·summary·artifact·required check가 실패하면 merge-ready가 아니다. 실패 로그를 읽고 test logic과 workflow contract를 분리해 수정한다.

## 8. 프로젝트 전용 값 제외

공용화하지 않은 값:

- 특정 PR·Task·Decision 번호
- 특정 SHA·worktree·scene 경로
- 특정 해상도·전투 수·캐릭터 기본값
- 특정 프로젝트 Art Direction·palette·faction·social policy

위 값은 해당 프로젝트 정본에 남고, Base에는 반복 가능한 storage·freshness·evidence 원리만 흡수한다.

## 9. Evidence ceiling

이 Case와 계약은 process evidence다.

```text
policy present
!= local file written
!= tracked asset promoted
!= Codex consumed
!= runtime verified
!= Human usability PASS
!= Player Experience PASS
```

각 프로젝트는 실제 filesystem/Git/Godot/CI evidence를 별도로 남긴다.
