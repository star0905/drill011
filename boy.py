
from math import pi

from pico2d import SDLK_a, SDLK_LEFT, SDLK_RIGHT, SDLK_SPACE, load_image
from transitions import Machine


class AutoRun:
    DURATION = 5.0
    SPEED = 300
    SIZE = 140
    Y_OFFSET = 15

    def __init__(self):
        self.elapsed_time = 0.0

    def enter(self, boy):
        self.elapsed_time = 0.0

    def update(self, boy, elapsed_time):
        self.elapsed_time += elapsed_time
        next_x = boy.x + self.SPEED * boy.face_dir * elapsed_time
        left_edge = self.SIZE / 2
        right_edge = boy.CANVAS_WIDTH - left_edge

        if next_x <= left_edge:
            boy.x = left_edge
            boy.face_dir = 1
        elif next_x >= right_edge:
            boy.x = right_edge
            boy.face_dir = -1
        else:
            boy.x = next_x
        if self.elapsed_time >= self.DURATION:
            boy.finish_auto_run()

    def exit(self, boy):
        self.elapsed_time = 0.0


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
        self.auto_run = AutoRun()
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(
            model=self,
            states=['IDLE', 'WALK', 'SLEEP', 'AUTORUN'],
            initial='IDLE',
            auto_transitions=False,
        )
        self.machine.add_transition(
            trigger='start_auto_run',
            source='IDLE',
            dest='AUTORUN',
            before='enter_auto_run',
            after='reset_idle_time',
        )
        self.machine.add_transition(
            trigger='finish_auto_run',
            source='AUTORUN',
            dest='IDLE',
            before='exit_auto_run',
            after='reset_idle_time',
        )
        self.machine.add_transition(
            trigger='cancel_auto_run',
            source='AUTORUN',
            dest='WALK',
            before='exit_auto_run',
            after='reset_idle_time',
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
        elif self.state == 'AUTORUN':
            self.frame = (self.frame + 1) % 8
            self.auto_run.update(self, elapsed_time)

    def handle_key(self, key):
        if self.state == 'SLEEP':
            if key == SDLK_SPACE:
                self.wake_up()
            return
        if self.state == 'AUTORUN' and key in (SDLK_LEFT, SDLK_RIGHT):
            self.pressed_keys.add(key)
            self.face_dir = -1 if key == SDLK_LEFT else 1
            self.cancel_auto_run()
            return
        if key == SDLK_a and self.state == 'IDLE':
            self.start_auto_run()
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

    def enter_auto_run(self):
        self.auto_run.enter(self)

    def exit_auto_run(self):
        self.auto_run.exit(self)

    def draw(self):
        if self.state in ('WALK', 'AUTORUN'):
            source_y = 100 if self.face_dir == 1 else 0
        else:
            source_y = 300 if self.face_dir == 1 else 200
        angle = self.SLEEP_ANGLE if self.state == 'SLEEP' else 0
        draw_size = self.auto_run.SIZE if self.state == 'AUTORUN' else self.SPRITE_WIDTH
        if self.state == 'SLEEP':
            draw_y = self.SLEEP_Y
        elif self.state == 'AUTORUN':
            draw_y = self.y + self.auto_run.Y_OFFSET
        else:
            draw_y = self.y
        self.image.clip_composite_draw(
            self.frame * 100,
            source_y,
            self.SPRITE_WIDTH,
            self.SPRITE_WIDTH,
            angle,
            ' ',
            self.x,
            draw_y,
            draw_size,
            draw_size,
        )