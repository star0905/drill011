from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('homework_character_4actions.png')
# fill here
frame = 0

FRAME_WIDTH = 200
FRAME_HEIGHT = 190

def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            close_canvas()
            raise SystemExit
#액션 번호
DASH = 0
ATTACK = 1
JUMP = 2
WALK = 3
# 프레임
animations = [
    (WALK, 6),
    (JUMP, 8),
    (ATTACK, 8),
    (DASH, 6)
]

BASE_Y = 200

while True:


    for action, frame_count in animations:

        for repeat in range(5):

            for frame in range(frame_count):
                handle_events()
                clear_canvas()
                grass.draw(400, 30)

                # 현재 프레임의 위치 계산
                left = frame * FRAME_WIDTH
                bottom = action * FRAME_HEIGHT

                x = 400
                y = BASE_Y

                if action == JUMP:

                    jump_height = [ 
                        0,    
                        50,   
                        100,
                        140,
                        140,  
                        100,
                        50,
                        0    
                    ]

                    y = BASE_Y + jump_height[frame]
                character.clip_draw(
                    left, bottom,
                    FRAME_WIDTH, FRAME_HEIGHT,
                    x, y,
                    FRAME_WIDTH * 2,
                    FRAME_HEIGHT * 2

                )
                update_canvas()

                delay(0.05)
        handle_events()
        delay(1.0)

close_canvas()

