from pico2d import *

canvas_width = 1280
canvas_height = 1024

open_canvas(canvas_width, canvas_height)
hide_cursor()  # 마우스 커서 대신 캐릭터가 보이도록

character = load_image('animation_sheet.png')

def handle_events():
    global running, x, y, face_dir

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            # pico2d의 y좌표는 아래에서 위로, SDL의 y좌표는 위에서 아래로이므로 뒤집어줌
            new_x = event.x
            new_y = canvas_height - 1 - event.y
            # 이동 방향에 따라 보는 방향 결정
            if new_x > x:
                face_dir = 1
            elif new_x < x:
                face_dir = -1
            x, y = new_x, new_y

running = True
frame = 0
x, y = canvas_width // 2, canvas_height // 2
face_dir = 1  # 1: 오른쪽, -1: 왼쪽

while running:
    clear_canvas()

    # 스프라이트 시트: 위쪽 줄(y=100)은 오른쪽, 아래쪽 줄(y=0)은 왼쪽 (프레임 100x100, 8프레임)
    if face_dir == 1:
        character.clip_draw(frame * 100, 100, 100, 100, x, y)
    else:
        character.clip_draw(frame * 100, 0, 100, 100, x, y)

    update_canvas()
    handle_events()
    frame = (frame + 1) % 8
    delay(0.05)

close_canvas()
