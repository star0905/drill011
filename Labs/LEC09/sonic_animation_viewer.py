from pathlib import Path

from pico2d import *


CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
DISPLAY_HEIGHT = CANVAS_HEIGHT // 2
FRAME_INTERVAL = 0.08
REPETITIONS_PER_ACTION = 5
ACTION_PAUSE = 1.0
IMAGE_PATH = Path(__file__).resolve().parent / "sonic-sprite.png"
ANIMATION_REGIONS = (
    ("동작 01", 0, 38, 335, 41),
    ("동작 02", 0, 78, 399, 40),
    ("동작 03", 0, 120, 262, 45),
    ("동작 04", 0, 166, 299, 35),
    ("동작 05", 0, 205, 218, 30),
    ("동작 06", 0, 237, 218, 38),
    ("동작 07", 0, 282, 258, 39),
    ("동작 08", 0, 325, 172, 48),
    ("동작 09", 180, 325, 95, 48),
    ("동작 10", 0, 376, 288, 42),
    ("동작 11", 0, 425, 150, 45),
)
ANIMATION_FRAME_COUNTS = (11, 12, 6, 9, 6, 6, 6, 6, 2, 8, 4)
ANIMATION_FRAME_BOUNDS = (
    (0, 30, 57, 85, 114, 146, 177, 208, 239, 268, 299, 335),
    (0, 36, 64, 96, 135, 169, 205, 235, 262, 294, 332, 368, 399),
    (0, 37, 82, 127, 174, 222, 262),
    (0, 33, 66, 98, 130, 161, 192, 227, 264, 299),
    (0, 34, 68, 102, 137, 171, 218),
    (0, 33, 70, 108, 145, 183, 218),
    (0, 33, 71, 117, 167, 214, 258),
    (0, 29, 60, 89, 117, 146, 172),
    (180, 229, 275),
    (0, 30, 63, 97, 134, 172, 213, 252, 288),
    (0, 45, 90, 122, 150),
)


def build_animations():
    animations = []
    for region, frame_bounds, expected_count in zip(
        ANIMATION_REGIONS, ANIMATION_FRAME_BOUNDS, ANIMATION_FRAME_COUNTS
    ):
        name, region_x, region_y, region_width, region_height = region
        if frame_bounds[0] != region_x or frame_bounds[-1] != region_x + region_width:
            raise ValueError(f"프레임 경계가 동작 영역과 일치하지 않습니다: {name}")

        frames = tuple(
            (left, region_y, right - left, region_height)
            for left, right in zip(frame_bounds, frame_bounds[1:])
        )
        if len(frames) != expected_count:
            raise ValueError(f"프레임 수가 일치하지 않습니다: {name}")
        animations.append((name, frames))

    return tuple(animations)


def to_pico2d_rect(frame, image_height):
    left, top, width, height = frame
    bottom = image_height - (top + height)
    return left, bottom, width, height


def draw_frame(sprite, frame, center_x, base_y):
    left, bottom, width, height = to_pico2d_rect(frame, sprite.h)
    scale = DISPLAY_HEIGHT / height
    draw_width = int(round(width * scale))
    draw_height = DISPLAY_HEIGHT
    draw_y = base_y + draw_height // 2
    sprite.clip_draw(left, bottom, width, height, center_x, draw_y, draw_width, draw_height)


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT or (
            event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE
        ):
            return False
    return True


def load_sprite():
    if not IMAGE_PATH.is_file():
        raise FileNotFoundError(f"스프라이트 파일을 찾을 수 없습니다: {IMAGE_PATH}")

    try:
        return load_image(str(IMAGE_PATH))
    except Exception as error:
        raise RuntimeError(f"스프라이트 파일을 불러올 수 없습니다: {IMAGE_PATH}") from error


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sprite = load_sprite()
    except (FileNotFoundError, RuntimeError) as error:
        print(error)
        close_canvas()
        return

    animations = build_animations()
    action_index = 0
    _, current_action_frames = animations[action_index]
    center_x = CANVAS_WIDTH // 2
    base_y = (CANVAS_HEIGHT - DISPLAY_HEIGHT) // 2

    running = True
    frame_index = 0
    repeat_count = 0

    while running:
        running = handle_events()
        clear_canvas()
        draw_frame(sprite, current_action_frames[frame_index], center_x, base_y)
        update_canvas()

        frame_index += 1
        if frame_index >= len(current_action_frames):
            frame_index = 0
            repeat_count += 1
            if repeat_count >= REPETITIONS_PER_ACTION:
                repeat_count = 0
                delay(ACTION_PAUSE)
                action_index = (action_index + 1) % len(animations)
                _, current_action_frames = animations[action_index]

        delay(FRAME_INTERVAL)

    close_canvas()


if __name__ == "__main__":
    main()