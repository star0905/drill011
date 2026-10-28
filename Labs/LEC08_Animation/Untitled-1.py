import json
from pico2d import *

open_canvas(800, 600)

grass = load_image('grass.png')
sheet = load_image('hero_sheet.png')

# 스프라이트 시트 정보 (프레임별 좌표/크기/기준점) 불러오기
with open('hero_sheet.json', 'r', encoding='utf-8') as f:
    sheet_info = json.load(f)

SCALE = 9          # 캐릭터 높이 약 34px -> 화면(600)의 절반 이상이 되도록 확대
CENTER_X = 400     # 캐릭터 기준점이 오는 화면 x좌표 (화면 중앙)
GROUND_Y = 60      # 캐릭터 발이 닿는 y좌표 (잔디 위)
REPEAT = 5         # 애니메이션별 반복 횟수
PAUSE = 1.0        # 애니메이션 종료 후 정지 시간(초)

# 재생 순서: 시트에 들어 있는 모든 애니메이션을 차례로 재생
ANIMATION_ORDER = ['idle', 'walk', 'run', 'jump', 'attack']


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            close_canvas()
            raise SystemExit


def draw_frame(frame):
    # pico2d 는 이미지 좌하단이 (0, 0) 이므로 시트의 y좌표(위 기준)를 변환
    bottom = sheet.h - (frame['y'] + frame['h'])

    # 프레임 크기가 제각각이므로 기준점(pivot_x)을 중앙에 맞추고
    # 프레임 아래쪽을 바닥에 맞춰서 그림 (점프 높이가 자연스럽게 표현됨)
    draw_w = frame['w'] * SCALE
    draw_h = frame['h'] * SCALE
    x = CENTER_X + (frame['w'] / 2 - frame['pivot_x']) * SCALE
    y = GROUND_Y + draw_h / 2

    sheet.clip_draw(
        frame['x'], bottom,
        frame['w'], frame['h'],
        x, y,
        draw_w, draw_h
    )


def wait(seconds):
    # 대기 중에도 종료 이벤트를 받을 수 있도록 잘게 나눠서 기다림
    steps = int(seconds / 0.05)
    for _ in range(steps):
        handle_events()
        delay(0.05)


while True:

    for name in ANIMATION_ORDER:
        anim = sheet_info['animations'][name]
        frames = anim['frames']
        frame_delay = 1.0 / anim['fps']

        # 각 애니메이션을 5번 반복
        for repeat in range(REPEAT):
            for frame in frames:
                handle_events()

                clear_canvas()
                grass.draw(400, 30)
                draw_frame(frame)
                update_canvas()

                delay(frame_delay)

        # 한 애니메이션이 5번 끝나면 1초 정지 (마지막 화면 유지)
        wait(PAUSE)