# 공용 사례 연구 인덱스

이 폴더는 프로젝트와 벤치마킹에서 얻은 판단을 재사용 가능한 학습 사례로 기록한다.

사례는 활성 프로젝트 기획서를 대신하지 않는다. 현재 수치·파일·로드맵은 각 프로젝트 저장소에서 관리하며, Base 사례에는 문제 해결 원리와 검증 교훈만 남긴다.

## 사례 작성 상태

- `가설`: 채택했지만 아직 실제 검증 전.
- `부분 검증`: 일부 PoC·화면·문서 검증 완료.
- `검증`: 실제 작업·플레이테스트·운영에서 효과 확인.
- `제외`: 검토했으나 적용하지 않음.
- `폐기`: 더 나은 접근으로 대체.

## OMENWARD 사례

| 사례 | 주제 | 상태 |
|---|---|---|
| `OMENWARD_SHARED_ARCHETYPE_FACTION_VISUAL_CASE.md` | 공용 병종 데이터와 진영별 시각 세트 | 채택·구현 전 |
| `OMENWARD_TACTICAL_VISIBILITY_WITHOUT_MINIMAP_CASE.md` | 전체 조망 전장에서 미니맵 제거 | 채택·PoC 검증 전 |
| `OMENWARD_FOGGED_SPECIALIST_ROUTE_CASE.md` | 특수 이동 경로의 조건부 공개 | 채택·PoC 검증 전 |
| `OMENWARD_CANONICAL_HANDOFF_CONTEXT_CASE.md` | 중복 문서 정리와 인수인계 컨텍스트 | 문서 운영 검증 |

## urban-legend / 괴이 기록국 사례

| 사례 | 주제 | 상태 |
|---|---|---|
| `URBAN_LEGEND_SCENE_FIRST_UI_CASE.md` | 정보 패널 중심 화면을 장면 중심 조사 UI로 재구성 | 구현·화면 검증 |
| `URBAN_LEGEND_DISPLAY_NAME_INTERNAL_ID_CASE.md` | 플레이어 표시명과 내부 영속 ID 분리 | 구현·저장 호환 검증 |
| `URBAN_LEGEND_DIALOGUE_DENSITY_BY_CONTEXT_CASE.md` | 기능 장면과 관계 장면의 대사 밀도 분리 | 채택·부분 검증 |
| `URBAN_LEGEND_RELATIONSHIP_MEMORY_CASE.md` | 상시 호감도 숫자 대신 선택 기억과 후속 반응 | 승인 기획·검증 전 |
| `URBAN_LEGEND_PRESENTATION_STATE_BOUNDARY_CASE.md` | 표정·컷인·대화 UI의 상태 비소유 경계 | 승인 아키텍처·검증 전 |
| `URBAN_LEGEND_TEXT_FREE_GENERATIVE_ART_CASE.md` | 생성 이미지와 제품 의미 텍스트 분리 | 자산·엔진 검증 |
| `URBAN_LEGEND_ACTIVE_DOCUMENT_ARCHIVE_CASE.md` | 현행 책임 문서와 날짜별 백업 분리 | 문서 운영 검증 |

## 문제별 라우팅

| 문제 | 우선 사례 |
|---|---|
| 화면에 정보가 많아 현재 행동이 묻힘 | `URBAN_LEGEND_SCENE_FIRST_UI_CASE.md` |
| 공개 명칭 변경과 저장 호환 | `URBAN_LEGEND_DISPLAY_NAME_INTERNAL_ID_CASE.md` |
| 캐릭터 대사가 기능 흐름을 방해함 | `URBAN_LEGEND_DIALOGUE_DENSITY_BY_CONTEXT_CASE.md` |
| 관계를 점수와 보너스로만 표현함 | `URBAN_LEGEND_RELATIONSHIP_MEMORY_CASE.md` |
| UI·연출이 결과·저장을 중복 소유함 | `URBAN_LEGEND_PRESENTATION_STATE_BOUNDARY_CASE.md` |
| 생성 이미지 글자·현지화 문제 | `URBAN_LEGEND_TEXT_FREE_GENERATIVE_ART_CASE.md` |
| 오래된 문서가 기본 읽기를 방해함 | `URBAN_LEGEND_ACTIVE_DOCUMENT_ARCHIVE_CASE.md`, `OMENWARD_CANONICAL_HANDOFF_CONTEXT_CASE.md` |
| 같은 역할의 진영별 데이터 중복 | `OMENWARD_SHARED_ARCHETYPE_FACTION_VISUAL_CASE.md` |
| 전체 조망 화면의 미니맵 필요성 | `OMENWARD_TACTICAL_VISIBILITY_WITHOUT_MINIMAP_CASE.md` |
| 특수 경로·범위의 조건부 공개 | `OMENWARD_FOGGED_SPECIALIST_ROUTE_CASE.md` |

## 작성 규칙

- 새 사례는 `templates/KNOWLEDGE_CASE_STUDY.md`를 사용한다.
- 프로젝트 이름과 공개 가능한 맥락을 표시한다.
- 외부 작품의 아트·코드·문구를 복제하지 않는다.
- 채택안뿐 아니라 제외안과 위험도 남긴다.
- 실제 결과가 없으면 `가설` 또는 `구현 전`으로 표시한다.
- 여러 프로젝트에서 반복 확인된 원칙만 methods 또는 skills로 승격한다.
- 현재 프로젝트의 수치·파일 경로·비공개 원문은 프로젝트 저장소에 남긴다.
