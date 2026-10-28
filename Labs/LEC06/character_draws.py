# 실습 과제 진행
from pico2d import *
import math

# 캔버스 구현
open_canvas(800, 600)

boy = load_image('character.png')

# 이동 표현 함수
def draw_boy(x, y):
    handle_events()
    clear_canvas()
    boy.draw(x, y)
    update_canvas()
    delay(0.01)

clear_canvas()

# 캔버스 안정용
def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            close_canvas()
            raise SystemExit

# 삼각 이동용 좌표
POINT_A_START = (100, 100)
POINT_A_END = (700, 100)
POINT_B_START = (700, 100)
POINT_B_END = (400, 500)
POINT_C_START = (400, 500)
POINT_C_END = (100, 100)

# 원 이동
def move_circle():
    for degree in range(360):
         theta = math.radians(degree)
         x = 400 + 200 * math.cos(theta)
         y = 300 + 200 * math.sin(theta)

         handle_events()
         clear_canvas()
         boy.draw(x, y)
         update_canvas()
         delay(0.01)

# 사각 이동
def move_rectangle():
    move_top()
    move_right()
    move_bottom()
    move_left()

# 사각 이동 구현 함수
def move_top():    
    for x in range(50, 751, 5):
     draw_boy(x, 550)

def move_right():
    for y in range(550, 49, -5):
        draw_boy(750, y)

def move_bottom():
    for x in range(750, 49, -5):
        draw_boy(x, 50)

def move_left():
    for y in range(50, 551, 5):
        draw_boy(50, y)

# 삼각 이동
def move_triangle():
    move_point_a()
    move_point_b()
    move_point_c()
    
# 삼각 이동 구현 함수들
def move_point_a():
    x0, y0 = POINT_A_START
    x1, y1 = POINT_A_END

    for i in range(0, 100 + 1, 1):
        t = i / 100.0
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t

        draw_boy(x, y)

def move_point_b():
    x0, y0 = POINT_B_START
    x1, y1 = POINT_B_END

    for i in range(0, 100 + 1, 1):
        t = i / 100.0
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t

        draw_boy(x,y)

def move_point_c():
    x0, y0 = POINT_C_START
    x1, y1 = POINT_C_END
    

    for i in range(0, 100 + 1, 1): 
        t = i / 100.0
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t

        draw_boy(x,y)
# 실행
while True:
    move_circle()
    move_rectangle()
    move_triangle()