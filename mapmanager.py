# напиши здесь код создания и управления картой
class Mapmanager():
    #Управление картой
    def __init__(self):
        self.model = 'block' #модель кубика лежит в файле block.egg
        self.texture = 'block.png'
        self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.2, 0.5, 0.2, 1),
            (0.7, 0.2, 0.2, 1),
            (0.5, 0.3, 0.0, 1)
        ]#rgba
        self.startNew()
    def startNew(self):
        #создаем основу для новой карты
        self.land = render.attachNewNode('Land') #узел, к которому привязаны все блоки
    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors)- 1]
    def addBlock(self, position):
        #создаем строительные блоки
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.color = self.getColor(int(position[2]))
        self.block.setColor(self.color)
        self.block.reparentTo(self.land)
    def clear(self):
        #обнуляет карту
        self.land.removeNode()
        self.startNew()
    def loadLand(self, filename):
        #создаем карту земли из текстового файла, возвращает её размеры
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z in range(int(z)+1):
                        block = self.addBlock((x, y, z))
                    x +=1
                y += 1
    

