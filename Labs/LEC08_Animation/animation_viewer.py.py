from pico2d import *

open_canvas(800, 600)

# 캐릭터 로딩
grass = load_image('grass.png')
character = load_image('hero_sheet.png')

# 프레임마다 크기가 달라서, 프레임 좌표/크기는 JSON 에서 불러옴
sheet_info = {'image': 'hero_sheet.png', 'animations': {'idle': {'fps': 6, 'frames': [{'x': 2, 'y': 2, 'w': 20, 'h': 42, 'pivot_x': 10, 'offset_y': -4}, {'x': 24, 'y': 2, 'w': 20, 'h': 42, 'pivot_x': 10, 'offset_y': -4}, {'x': 46, 'y': 2, 'w': 20, 'h': 41, 'pivot_x': 10, 'offset_y': -4}, {'x': 68, 'y': 2, 'w': 20, 'h': 41, 'pivot_x': 10, 'offset_y': -4}]}, 'walk': {'fps': 10, 'frames': [{'x': 2, 'y': 46, 'w': 22, 'h': 41, 'pivot_x': 10, 'offset_y': -4}, {'x': 26, 'y': 46, 'w': 20, 'h': 42, 'pivot_x': 8, 'offset_y': -4}, {'x': 48, 'y': 46, 'w': 19, 'h': 41, 'pivot_x': 6, 'offset_y': -4}, {'x': 69, 'y': 46, 'w': 23, 'h': 41, 'pivot_x': 4, 'offset_y': -4}, {'x': 94, 'y': 46, 'w': 21, 'h': 42, 'pivot_x': 2, 'offset_y': -4}, {'x': 117, 'y': 46, 'w': 19, 'h': 41, 'pivot_x': 0, 'offset_y': -4}]}, 'run': {'fps': 14, 'frames': [{'x': 2, 'y': 90, 'w': 26, 'h': 41, 'pivot_x': 16, 'offset_y': -4}, {'x': 30, 'y': 90, 'w': 20, 'h': 42, 'pivot_x': 12, 'offset_y': -4}, {'x': 52, 'y': 90, 'w': 19, 'h': 42, 'pivot_x': 8, 'offset_y': -4}, {'x': 73, 'y': 90, 'w': 22, 'h': 42, 'pivot_x': 4, 'offset_y': -4}, {'x': 97, 'y': 90, 'w': 25, 'h': 41, 'pivot_x': 0, 'offset_y': -4}, {'x': 124, 'y': 90, 'w': 20, 'h': 42, 'pivot_x': -4, 'offset_y': -4}, {'x': 146, 'y': 90, 'w': 19, 'h': 42, 'pivot_x': -8, 'offset_y': -4}, {'x': 167, 'y': 90, 'w': 22, 'h': 42, 'pivot_x': -12, 'offset_y': -4}]}, 'jump': {'fps': 9, 'frames': [{'x': 2, 'y': 134, 'w': 22, 'h': 39, 'pivot_x': 11, 'offset_y': -4}, {'x': 26, 'y': 134, 'w': 21, 'h': 42, 'pivot_x': 10, 'offset_y': -1}, {'x': 49, 'y': 134, 'w': 21, 'h': 41, 'pivot_x': 10, 'offset_y': 7}, {'x': 72, 'y': 134, 'w': 22, 'h': 39, 'pivot_x': 10, 'offset_y': 16}, {'x': 96, 'y': 134, 'w': 23, 'h': 38, 'pivot_x': 10, 'offset_y': 20}, {'x': 121, 'y': 134, 'w': 20, 'h': 41, 'pivot_x': 9, 'offset_y': 12}, {'x': 143, 'y': 134, 'w': 19, 'h': 42, 'pivot_x': 9, 'offset_y': 2}, {'x': 164, 'y': 134, 'w': 22, 'h': 39, 'pivot_x': 11, 'offset_y': -4}]}, 'attack': {'fps': 10, 'frames': [{'x': 2, 'y': 178, 'w': 21, 'h': 50, 'pivot_x': 10, 'offset_y': -4}, {'x': 25, 'y': 178, 'w': 24, 'h': 53, 'pivot_x': 10, 'offset_y': -4}, {'x': 51, 'y': 178, 'w': 36, 'h': 48, 'pivot_x': 10, 'offset_y': -4}, {'x': 89, 'y': 178, 'w': 39, 'h': 45, 'pivot_x': 10, 'offset_y': -4}, {'x': 130, 'y': 178, 'w': 36, 'h': 41, 'pivot_x': 10, 'offset_y': -4}, {'x': 168, 'y': 178, 'w': 36, 'h': 42, 'pivot_x': 10, 'offset_y': -4}]}}}

SCALE = 9    # 크기 조절
GROUND_Y = 50    # 캐릭터 발이 닿는 y좌표

def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            close_canvas()
            raise SystemExit

# 재생할 애니메이션 순서
animations = ['idle', 'walk', 'run', 'jump', 'attack']

# 애니메이션 순서를 계속 반복
while True:
    for name in animations:
        frames = sheet_info['animations'][name]['frames']
        # 각 애니메이션을 5번 반복
        for repeat in range(5):
            # 현재 애니메이션의 프레임 수만큼 재생 (애니메이션마다 프레임 수가 다름)
            for frame in frames:
                handle_events()
                clear_canvas()
                grass.draw(400, 30)
                # 현재 프레임의 위치와 크기 (프레임마다 다름)
                left = frame['x']
                width = frame['w']
                height = frame['h']
                # pico2d 는 이미지 아래가 0 이므로 위 기준 y 좌표를 변환
                bottom = character.h - (frame['y'] + height)
                x = 400 + (width / 2 - frame['pivot_x']) * SCALE
                y = GROUND_Y + frame['offset_y'] * SCALE + height * SCALE / 2
                # 캐릭터 행동
                character.clip_draw(
                 left, bottom,
                 width, height,
                 x, y,
                 width * SCALE,
                 height * SCALE
                ) 
                update_canvas()

                delay(0.08)
        # 정지 후 반복
        handle_events()
        delay(1.0)
    
close_canvas()
