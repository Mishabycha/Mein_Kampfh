from direct.showbase.ShowBase import ShowBase
from hero import Hero
from mapmanager import Mapmanager

class Game(ShowBase):
    def __init__(self):
        super().__init__()
        base.camLens.setFov(90)
        self.land = Mapmanager()
        x, y = self.land.load_map("maps/land2.txt")
        self.hero = Hero((x//2, y//2, 1), self.land)

        start_snd = base.loader.loadSfx("sounds\inecraft_forest.ogg") 
        start_snd.set_volume(0)
        start_snd.setLoop(True)
        start_snd.play()

game = Game()
game.run()