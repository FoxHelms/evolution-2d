import pygame, random, math

pygame.init()


WIDTH, HEIGHT = 800,800
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Ecosystem View")

class Bush:
    def __init__(self, pos_x, pos_y, size, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size
        self.color = color

        self.is_eaten = False

    def draw(self,win):
        x = self.pos_x
        y = self.pos_y
        pygame.draw.circle(win, self.color, (x,y), self.size)



class Rabbit:
    def __init__(self,pos_x,pos_y,age):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.age = age

        self.is_hungry = True
        self.is_near_food = False
        self.trail = []
        self.distance_to_nearest_bush = 0
        self.awareness_rad = 200

        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self,win):
        pos_x = self.pos_x
        pos_y = self.pos_y
        pygame.draw.circle(win, (255,0,0), (pos_x,pos_y), self.age)

    def wander(self):
        urge_x = random.randint(1,500)
        urge_y = random.randint(1,500)
        unit_urge_x = urge_x / math.sqrt(urge_x ** 2 + urge_y ** 2)
        unit_urge_y = urge_y / math.sqrt(urge_x ** 2 + urge_y ** 2)
        self.pos_x += unit_urge_x
        self.pos_y += unit_urge_y


    def near_food(self, bush):
        dx = bush.pos_x - self.pos_x
        dy = bush.pos_y - self.pos_y
        self.distance = math.sqrt(dx**2 + dy**2)
        if self.distance <= self.awareness_rad:
            self.is_near_food = True

    def move_towards_food(self,bush):
        dx = bush.pos_x - self.pos_x
        dy = bush.pos_y - self.pos_y
        distance = math.sqrt(dx**2 + dy**2)
        unit_x = dx / distance
        unit_y = dy / distance
        self.pos_x += unit_x
        self.pos_y += unit_y
        




def main():
    run = True
    clock = pygame.time.Clock()
    bushes = []
    
    george = Rabbit(400,500,60)
    harry = Rabbit(700,700,20)
    rabbits = [george,harry]
    
    while run:
        clock.tick(60)
        WIN.fill((217,217,217))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x,pos_y = pygame.mouse.get_pos()
                newBush = Bush(pos_x,pos_y,30,(0,0,0))
                bushes.append(newBush)

        for bush in bushes:
            bush.draw(WIN)
        
        for rabbit in rabbits:
            if rabbit.is_hungry:
                if bushes:
                    for bush in bushes:
                        rabbit.near_food(bush)
                        if rabbit.is_near_food:
                            rabbit.move_towards_food(bush)
                        if abs(rabbit.distance) < 50:
                            bushes.remove(bush)
                            print("yum")
                    else:
                        rabbit.wander()
                else:
                    rabbit.wander()
            rabbit.draw(WIN) 

        pygame.display.update()
        
        
    pygame.quit()

main()
