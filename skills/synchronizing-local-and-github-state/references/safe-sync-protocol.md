# 안전한 Git 동기화 프로토콜

1. remote·upstream·현재 branch·HEAD·working tree·untracked를 기록한다.
2. fetch 후 merge-base와 ahead/behind를 판정한다.
3. clean fast-forward만 자동 pull한다.
4. 로컬 변경은 diff·검증·명시적 파일 범위로 commit한다.
5. 원격 변경은 보호 branch 정책과 Required Checks를 지킨다.
6. diverged history는 백업 branch를 만들고 선택한 전략을 기록한다.
7. 최종 local HEAD와 remote HEAD, tree diff, CI 상태를 대조한다.
