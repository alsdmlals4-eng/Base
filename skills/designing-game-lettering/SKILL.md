---
name: designing-game-lettering
description: Use when designing or reviewing custom game logos, title lettering, chapter or boss-name wordmarks, or display typography. Not for ordinary UI text sizing, localization, or font rendering bugs.
---

# Designing Game Lettering

로고·타이틀의 의미를 글자 형태로 표현하는 전문 제작 계약이다. 정확한 문구와 실제 사용처를 입력받아 형태·간격·표현·검수 기준을 만든다. 특정 폰트, 장르, 색상, 기울기, 장식을 공용 기본값으로 고정하지 않는다.

## 선택과 책임

- `lettering-brief`: 게임 로고/타이틀/챕터·보스 이름의 조형 방향과 제작 조건.
- `lettering-production`: 승인 범위의 후보 제작·편집 지시와 수정 가능한 원본/출력.
- `lettering-review`: 문구·형태·크기별 가독성·배경 적합성과 승인 준비.
- 일반 버튼/본문/숫자/일본어 현지화/폰트 fallback은 `auditing-and-refining-ui-art`로 보낸다. 장식 레터링으로 대체하지 않는다.
- 이 Skill이 글자 조형의 주 책임이다. 실제 이미지 생성·편집·후보 승인은 `designing-art-prompts-and-technique-cards`의 기존 경로를 소비한다. 같은 단계에 주 책임을 둘로 두거나 승인 절차를 다시 만들지 않는다.

## 입력과 제작

프로젝트 current-authority와 최신 아트 정본·승인 로고·Visual Requirement를 먼저 확인한다. 정확한 표시 문자열/언어, 의미·인상, keep/avoid, 실제 screen 또는 배포 consumer, 사용 크기/배경/크롭, 현재 가능한 도구가 입력이다.

레터링 작업일 때만 [레터링 제작과 검수](references/lettering-production.md)를 읽는다. 컨셉/benchmark → 기본 형태·무게 → 간격·균형 → 필요한 장식 → 실제 크기 검수 순서를 출발점으로 사용한다. 효과 없는 형태부터 확인하며 획 두께 비율을 고정 공식으로 강제하지 않는다.

consumer나 필수 프로젝트 정본이 없으면 부족한 입력을 명시하고 조사/brief까지만 준비한다. 채팅 이미지·외부 예시는 프로젝트 승인 자산이 아니다. 새 폰트·플러그인 구매/설치 권한도 아니다.

## 산출물

기존 프로젝트 brief/asset record에 다음을 연결한다. 필요 없는 새 추적표는 만들지 않는다.

- 정확한 문구, 의미·형태 선택 이유, reference의 ADOPT/ADAPT/REJECT.
- 기존 승인 원본 보존, 글자 형태/장식 분리 및 실제 도구로 수정 가능한 source 경로.
- 실제 consumer에 필요한 출력/크기별 preview, source/font provenance와 권리 확인.
- 오탈자·글자 구별·시각 균형·배경·크롭 검수와 남은 수정.
- `CANDIDATE / USER_APPROVED / CANON_REGISTERED / IMPLEMENTED / RUNTIME_VERIFIED` 중 실제 증거로 확인된 단계.

이미지 생성만으로 편집 가능한 벡터·폰트·레이어 원본을 만들었다고 주장하지 않는다. 최종 제품 문자는 기존 아트 owner의 편집 가능한 UI/graphics layer 기준을 따른다. 정확한 글자 형태 원본을 확보하지 못하면 후보로 유지한다.

## 승인·정본·검증 경계

repository가 기본 정본이며 Notion은 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`의 명시적 예외/legacy migration일 때만 사용한다. 게임별 로고 교체·최종 이미지 승인은 별도 프로젝트 계약을 따른다.

시각 후보 검수, 권리 검토, 실제 화면 적용, runtime 캡처, 사람 승인을 합치지 않는다. 게임 화면용 자산이면 적용 후 실제 consumer의 캡처가 필요하며, 홍보 배포 전용이면 해당 배포 크기/배경 증거를 남긴다. 사용자 검수는 사용자 선언/승인 시 수행하고 AI 시각 검사를 사람 승인으로 쓰지 않는다.

학습·실패 기록은 `skills/SKILL_LEARNING_LOG.md`. 정적 연결 검사와 실제 모델 선택/아트 품질은 별도 증거다.
