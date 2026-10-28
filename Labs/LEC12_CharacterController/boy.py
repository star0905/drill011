
from math import pi

from pico2d import SDLK_LEFT, SDLK_RIGHT, SDLK_SPACE, load_image
from transitions import Machine

class Boy:
    CANVAS_WIDTH = 800
    SPRITE_WIDTH = 100
    NORMAL_Y = 90
    SLEEP_Y = 60
    SLEEP_AFTER = 3.0
    SLEEP_ANGLE = pi / 2
    WALK_SPEED = 150

    def __init__(self):
        self.x = self.CANVAS_WIDTH / 2
        self.y = self.NORMAL_Y
        self.frame = 0
        self.idle_time = 0.0
        self.face_dir = 1
        self.pressed_keys = set()
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(
            model=self,
            states=['IDLE', 'WALK', 'SLEEP'],
            initial='IDLE',
            auto_transitions=False,
        )
        self.machine.add_transition(
            trigger='start_walking',
            source='IDLE',
            dest='WALK',
            before='reset_idle_time',
        )
        self.machine.add_transition(
            trigger='stop_walking',
            source='WALK',
            dest='IDLE',
            after='reset_idle_time',
        )
        self.machine.add_transition(
            trigger='fall_asleep',
            source='IDLE',
            dest='SLEEP',
        )
        self.machine.add_transition(
            trigger='wake_up',
            source='SLEEP',
            dest='IDLE',
            after='reset_idle_time',
        )

    def update(self, elapsed_time=0.01):
        if self.state == 'IDLE':
            self.frame = (self.frame + 1) % 8
            self.idle_time += elapsed_time
            if self.idle_time >= self.SLEEP_AFTER:
                self.fall_asleep()
        elif self.state == 'WALK':
            self.frame = (self.frame + 1) % 8
            self.x = min(
                self.CANVAS_WIDTH - self.SPRITE_WIDTH / 2,
                max(
                    self.SPRITE_WIDTH / 2,
                    self.x + self.face_dir * self.WALK_SPEED * elapsed_time,
                ),
            )

    def handle_key(self, key):
        if self.state == 'SLEEP':
            if key == SDLK_SPACE:
                self.wake_up()
            return
        if key not in (SDLK_LEFT, SDLK_RIGHT):
            self.reset_idle_time()
            return

        self.pressed_keys.add(key)
        self.face_dir = -1 if key == SDLK_LEFT else 1
        if self.state == 'IDLE':
            self.start_walking()

    def handle_key_up(self, key):
        if key not in (SDLK_LEFT, SDLK_RIGHT):
            return

        self.pressed_keys.discard(key)
        if self.state != 'WALK':
            return
        if self.pressed_keys:
            self.face_dir = -1 if SDLK_LEFT in self.pressed_keys else 1
        else:
            self.stop_walking()

    def reset_idle_time(self):
        self.idle_time = 0.0

    def draw(self):
        if self.state == 'WALK':
            source_y = 100 if self.face_dir == 1 else 0
        else:
            source_y = 300 if self.face_dir == 1 else 200
        angle = self.SLEEP_ANGLE if self.state == 'SLEEP' else 0
        draw_y = self.SLEEP_Y if self.state == 'SLEEP' else self.y
        self.image.clip_composite_draw(
            self.frame * 100,
            source_y,
            self.SPRITE_WIDTH,
            self.SPRITE_WIDTH,
            angle,
            ' ',
            self.x,
            draw_y,
            self.SPRITE_WIDTH,
            self.SPRITE_WIDTH,
        )