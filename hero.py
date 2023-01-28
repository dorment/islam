# напиши свой код здесь
key_switch_camera = 'c' #камера привязана к герою или нет
key_switch_mode = 'z' #можно проходить сквозь препятствия или нет

key_forward = 'w' #шаг вперед (куда смотрит камера)
key_back = 's' #шаг назад
key_left = 'a' #шаг влево(ввод от камеры)
key_right = 'd' #шаг вправо
key_up = 'e' # шаг вверх
key_down = 'q' #шаг вниз

key_turn_left = 'n' #поворот камеры направо (a мира - налево)
key_turn_right = 'm' #поворот камеры налево (a мира - направо)

class Hero():
    def __init__(self, pos,land):
        self.land = land
        self.mode = True #режим прохождения сквозь всё
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()

    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparenTo(self.hero)
        base.camera.setPos(0,0,1.5)
        self.cameraOn = True
    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False
    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()
    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)
    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)
    def look_at(self,angle):
        '''возвращает координаты, в которые переместится  персонаж, стоящий в точке (x, y),если он делает шаг в направлении angle'''
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())
        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from
    def just_move(self,angle):
        #перемещается в нужные координаты в любом случае
            pos = self.look_at(angle)
            self.hero,setPos(pos)
    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
    def check_dir(self, angle):
        '''возвращает округленные изменение координат x,y,
        соответствующие перемещению в сторону угла angle. 
        Координата Y уменьшается, если персонаж смотрит на угол 0,
        и увеличивается, если смотрит на угол 180.
        Координата X увеличивается, если персонаж смотрит на угол 90,
        и уменьшается, если смотрит на угол 270''' 
        if angle >= 0 and angle <= 20:
            return(0, -1)
        elif angle <= 65:
            return(1, -1)
        elif angle <= 110:
            return(1,0)
        elif angle <= 155:
            return(1,1)
        elif angle <= 200:
            return(0,1)
        elif angle <= 245:
            return(-1,1)
        elif angle <= 290:
            return(-1, 0)
        elif angle <= 335:
            return(-1,1)
        else:
            return(0, -1)

    def forward(self):
        angle =(self.hero.getH()) % 360
        self.move_to(angle)

    def back(self):
        angle =(self.hero.getH()+180) % 360
        self.move_to(angle)
    def left(self):
        angle =(self.hero.getH()+90) % 360
        self.move_to(angle)
    def right(self):
        angle =(self.hero.getH()+270) % 360
        self.move_to(angle)

    def accept_events(self):
        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left +'-repeat', self.turn_left)
        base.accept(key_turb_right, self.turn_right)
        base.accept(key_turn_right + '-repeat', self.turn_right)
        
        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)
        base.accept(key_back, self.back)
        base.accept(key_back + '-repeat', self.back)
        base.accept(key_left,self.left)
        base.accept(key_left + '-repeat', self.left)
        base.accept(key_right, self.right)
        base.accept(key_right + '-repeat', self.right)
        base.accept(key_switch_camera, self.changeView)
    def try_move(self, angle):
        '''перемещается, если может'''
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2], 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)
    def down(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)
    
    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)
        
    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.block.land.delBlock(pos)

    def findBlocks(self,pos):
        return self.land.findALLMatches("=at="+str(pos))
    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True

    def findHighestEmpty(self,pos):
        x,y,z = pos
        z = 1
        while not self.isEmpty((x,y,z)):
            z+=1
        return(x,y,z)
    def BuildBlock(self,pos):
        #Ставим блок с учетом гравитацией
        x,y,z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)
    def delBlock(self, position):
        #удаляем блоки в указанной позиций
        blocks = self.findBlocks(position)
        for blocks in blocks:
            block.removeNode()
    def delBlockFrom(self, position):

        x,y,z = self.findHighestEmpty(position)
        pos = x,y,z - 1
        for block in self.findBlocks(pos):
            block.removeNode()
         












        