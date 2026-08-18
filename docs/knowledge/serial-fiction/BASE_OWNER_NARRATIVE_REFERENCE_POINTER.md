# Base-owner Narrative Preference Reference Pointer

이 문서는 Base 사용자의 소설·스토리·대화 **선호 참고자료**를 공개 저장소에 복사하지 않고, 필요할 때 연결된 개인 자료에서 최신 상태를 다시 읽기 위한 포인터 계약이다.

```text
SOURCE_ROLE: USER_PREFERENCE_EVIDENCE
RESOLUTION: LIVE_CONNECTED_DRIVE_READ
SOURCE_TITLE: 글따라쓰기
AUTHORITY: NOT_CANON
IMITATION_BOUNDARY: NO_STYLE_IMITATION
```

## Purpose

사용자가 관리하는 Google Docs 문서 **`글따라쓰기`**에는 사용자가 좋아하는 소설의 따라쓰기·연습 자료가 계속 추가될 수 있다. 소설·스토리·대화 작업에서 사용자 선호를 이해하는 데 관련이 있으면, 저장된 과거 복사본보다 **연결된 Google Drive의 현재 문서**를 다시 읽는다.

이 문서는 URL, raw document ID, 원문 사본을 저장하지 않는다. 접근은 현재 연결된 Drive에서 정확한 제목과 사용자가 제공한 현재 문맥으로 해석한다.

## What may be learned

원문 문장을 재사용하기보다 다음과 같은 **형식·구조적 선호 신호**를 추출한다.

- 문단 길이가 변하는 위치와 기능
- 대사와 서술이 교차하는 리듬
- 짧은 반응·침묵·충격을 독립 문단으로 두는 패턴
- 대사 전후의 빈 호흡과 장면 beat
- 서술 → 대사 → 반응 → 설명의 전환 방식
- 장면 전환에서의 blank-line 사용
- 모바일 화면에서 읽을 때의 덩어리 크기와 시선 이동
- 정보 공개 속도와 문단 경계의 관계

이 증거는 `PARAGRAPH_BREAK_AND_BREATH` 판단의 한 입력일 뿐, 고정 문단 길이나 보편 공식으로 승격하지 않는다.

## Authority boundary

`USER_PREFERENCE_EVIDENCE`는 다음이 아니다.

- 작품/프로젝트 정본
- 특정 작가의 문체를 복제하라는 지시
- 공개 benchmark dataset
- Base에 영구 보존해야 하는 원문 corpus
- 다른 사용자의 선호에 적용되는 universal rule

사용자 선호와 프로젝트 정본이 충돌하면 현재 프로젝트 정본과 최신 사용자 결정이 우선한다.

## Originality and privacy

### `NO_STYLE_IMITATION`

- 식별 가능한 문장, 비유, 개그, 말버릇, 장면 배열을 복제하지 않는다.
- 특정 현역 작가/작품의 문체를 그대로 모사하지 않는다.
- 참고자료에서 유용한 점은 문단 호흡, 정보 밀도, 대사/서술 전환, 반응 배치 같은 높은 수준의 기능으로 추상화한다.

### Private-source handling

- 공개 Base에 원문, 공유 URL, document ID를 커밋하지 않는다.
- 필요한 만큼만 live read하고, 결과에는 구조적 관찰과 적용 판단만 남긴다.
- source 접근권이 없으면 공개 설정으로 바꾸라고 자동 요구하지 않는다. 사용자에게 필요한 최소 공유/연결 방법만 안내한다.

## Freshness

문서는 계속 갱신될 수 있으므로 과거 관찰을 영구 선호로 고정하지 않는다.

```text
relevant serial-fiction/story/dialogue task
→ resolve connected Drive source by current user context + exact title
→ LIVE_CONNECTED_DRIVE_READ
→ current relevant passages/structure inspect
→ compare with existing preference hypothesis
→ keep / refine / reject hypothesis
→ apply only to current task where useful
```

새 내용이 기존 관찰과 다르면 최신 자료 전체를 보고 선호가 다양해진 것인지, 장르·장면별 조건부 선호인지 구분한다.

## Failure semantics

- 연결된 Drive에서 문서를 읽을 수 없음 + 현재 결과에 필수 → `BLOCKED_UNVERIFIED`
- 문서를 읽을 수 없음 + 독립 작업 가능 → 해당 preference analysis만 defer하고 다른 작업 계속
- 특정 작품 문구를 그대로 재현해야만 성립하는 결론 → `STYLE_COPY_RISK`, 고수준 기능으로 다시 추상화
- 샘플이 너무 적어 일반 선호를 단정하기 어려움 → `PREFERENCE_SAMPLE_LIMITED`

## Owner

- 주 책임: `skills/developing-and-revising-serial-fiction/SKILL.md`
- 작법 적용: `SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md`
- 외부 benchmark/reader evidence와의 구분: `READER_FEEDBACK_AND_BENCHMARK_EVIDENCE_GUIDE.md`
