# Character state diagram

```mermaid
stateDiagram-v2
    [*] --> IDLE

    IDLE --> AUTORUN: 'a' 키 입력
    AUTORUN --> IDLE: 5초 이상 경과
    AUTORUN --> WALK: 좌우 방향키 입력
    AUTORUN --> AUTORUN: 좌우 끝 도달<br/>방향 자동 반전

    IDLE --> WALK: 왼쪽/오른쪽 방향키 누름
    IDLE --> IDLE: 기타 키 입력<br/>idle_time = 0
    WALK --> WALK: 방향키 누름<br/>지정 방향으로 이동
    WALK --> IDLE: 방향키를 뗌
    IDLE --> SLEEP: 3초 동안 입력 없음
    SLEEP --> IDLE: 스페이스바 입력<br/>wake_up()

    IDLE: 8개 프레임 애니메이션 반복
    WALK: 방향에 따라 이동<br/>걷기 애니메이션 반복
    AUTORUN: 5초 제한<br/>고속/확대 자동 이동
    SLEEP: 현재 프레임 유지<br/>90도 회전 및 낮은 높이
```

`ESC` 키는 게임 종료에 사용합니다. 방향키를 누르고 있는 동안 캐릭터가 이동하며,
방향키를 떼면 `IDLE` 상태로 돌아갑니다. `AUTORUN` 상태에서는 5초 동안 자동 이동하며,
좌우 끝에서 방향을 바꿉니다. `SLEEP` 상태에서는 스페이스바를 눌러야 `IDLE` 상태로 깨어납니다.
