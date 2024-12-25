import pickle

class Mapmanager:
    def __init__(self):
        self.model = "models/block"
        self.texture = "textures/custom1.png"
        self.color = (164, 190, 169, 0.8)

        self.start_new()
        self.add_block((1, 1, 1))

    def add_block(self, position: tuple) -> None:
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setColor(self.color)
        self.block.setPos(position)
        self.block.setTag("at", str(position))
        self.block.reparentTo(self.land)

    def del_block(self, pos):
        blocks = self.find_blocks(pos)
        for block in blocks:
            block.removeNode()

    def build_block(self, pos):
        x, y, z = pos
        new = self.find_highest_empty(pos)
        if new[2] <= z + 1:
            self.add_block(new)

    def del_block_from(self, pos):
        x, y, z = self.find_highest_empty(pos)
        pos = x, y, z - 1
        blocks = self.find_blocks(pos)
        for block in blocks:
            block.removeNode()

    def load_map(self, filename):
        self.clear()
        with open(filename, "r") as file:
            y = 0
            for line in file:
                x = 0
                line_lst = line.split(" ")
                for z in line_lst:
                    for z0 in range(int(z) + 1):
                        block = self.add_block((x, y, z0))
                    x += 1
                y += 1
            return x, y

    def load_map_from_file(self):
        self.clear()
        with open('maps/my_map.dat', 'rb') as map:
            lenght = pickle.load(map)
            for i in range(lenght):
                pos = pickle.load(map)
                self.add_block(pos)

    def save_map(self):
        blocks = self.land.getChildren()
        with open('maps/my_map.dat', 'wb') as map:
            pickle.dump(len(blocks), map)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, map)


    def find_blocks(self, pos):
        return self.land.findAllMatches('=at=' + str(pos))

    def is_empty(self, pos):
        blocks = self.find_blocks(pos)
        if blocks:
            return False
        else:
            return True

    def find_highest_empty(self, pos):  # (10, 20, 1)
        x, y, z = pos
        z = 1
        while not self.is_empty((x, y, z)):
            z += 1
        return x, y, z

    def start_new(self):
        self.land = render.attachNewNode("Land")

    def load_map(self, filename):
        with open(filename, "r") as file:
            y = 0
            for line in file:
                line_lst = line.split(" ")
                x = 0
                for z in line_lst:
                    for i in range(int(z) + 1):
                        self.add_block((x, y, i))
                    x += 1
                y += 1
        return x, y                    


