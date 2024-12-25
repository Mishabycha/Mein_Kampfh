from time import time

class Hero:
    def __init__(self, pos, land):
        self.mode = True
        self.land = land
        self.hero = loader.loadModel("smiley")
        self.hero.setColor((.43, .92, .93, 1))
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        

        self.camera_bind()

        self.accept_events()

        self.damage_snd = base.loader.loadSfx("sounds/inecraft_damage.ogg")
        self.jump_snd = base.loader.loadSfx("sounds/up.mp3")

        self.last_walk_sound_time = 0
        self.walk_sound_delay = 0.3
        self.walk_snd = base.loader.loadSfx("sounds/step.ogg")

    def camera_bind(self):
        base.disableMouse()
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        base.camera.setH(180)  
        self.camera_on = True

    def camera_up(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.camera_on = False

    def switch_camera(self):
        if self.camera_on:
            self.camera_up()
        else:
            self.camera_bind()

    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    def change_mode(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True

        change_snd = base.loader.loadSfx("sounds/change_mode.ogg")
        change_snd.set_volume(0.5)
        change_snd.setLoop(True)
        change_snd.play()

    def move_to(self, angle):
        
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)

    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.is_empty(pos):
            pos = self.land.find_highest_empty(pos)
            self.hero.setPos(pos)
            self.walk_snd.play()
            self.walk_snd.set_volume(1)
            self.walk_snd.setLoop(False)
            self.walk_snd.play()
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.is_empty(pos):
                self.jump_snd.play()
                self.hero.setPos(pos)
            else:
                self.damage_snd.play()

    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

        current_time = time()
        if current_time - self.last_walk_sound_time > self.walk_sound_delay:
            self.walk_snd.set_volume(0.5)
            self.walk_snd.setLoop(False)
            self.walk_snd.play()
            self.last_walk_sound_time = current_time

    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.add_block(pos)
        else:
            self.land.build_block(pos)

        build_snd = base.loader.loadSfx("sounds/build.ogg")
        build_snd.set_volume(1)
        build_snd.setLoop(False)    

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.del_block(pos)
        else:
            self.land.del_block_from(pos)

        start_snd = base.loader.loadSfx("sounds/break.ogg")
        start_snd.set_volume(1)
        start_snd.setLoop(False)

    def check_dir(self, angle):
        ''' повертає заокруглені зміни координат X, Y,
        відповідні переміщенню у бік кута angle.
        Координата Y зменшується, якщо персонаж дивиться на кут 0,
        та збільшується, якщо дивиться на кут 180.
        Координата X збільшується, якщо персонаж дивиться на кут 90,
        та зменшується, якщо дивиться на кут 270.
            кут 0 (від 0 до 20) -> Y - 1
            кут 45 (від 25 до 65) -> X + 1, Y - 1
            кут 90 (від 70 до 110) -> X + 1
            від 115 до 155 -> X + 1, Y + 1
            від 160 до 200 -> Y + 1
            від 205 до 245 -> X - 1, Y + 1
            від 250 до 290 -> X - 1
            від 290 до 335 -> X - 1, Y - 1
            від 340 -> Y - 1
        '''
        if 0 <= angle <= 20:
            return 0, -1
        elif angle <= 65:
            return 1, -1
        elif angle <= 110:
            return 1, 0
        elif angle <= 155:
            return 1, 1
        elif angle <= 200:
            return 0, 1
        elif angle <= 245:
            return -1, 1
        elif angle <= 290:
            return -1, 0
        elif angle <= 335:
            return -1, -1
        else:
            return 0, -1

    def look_at(self, angle):
        from_x = round(self.hero.getX())
        from_y = round(self.hero.getY())
        from_z = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)

        return from_x + dx, from_y + dy, from_z

    def forward(self):
        angle = self.hero.getH() % 360
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() - 90) % 360
        self.move_to(angle)    

    def right(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle) 

    def accept_events(self):
        base.accept("c", self.switch_camera)
        base.accept("a", self.turn_left)
        base.accept("a" + "-repeat", self.turn_left)
        base.accept("d", self.turn_right)
        base.accept("d" + "-repeat", self.turn_right)
        base.accept("w", self.forward)
        base.accept("w" + "-repeat", self.forward)
        base.accept("s", self.back)
        base.accept("s" + "-repeat", self.back)
        base.accept("x", self.right)
        base.accept("x" + "-repeat", self.right)
        base.accept("z", self.left)
        base.accept("z" + "-repeat", self.left)
        base.accept("l", self.change_mode)
        base.accept("b", self.build)
        base.accept("m", self.destroy)
        #base.accept("p", self.load_map_from_file)
        #base.accept("o", self.save_map)
