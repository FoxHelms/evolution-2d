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
        self.is_at_top = False
        self.is_at_bottom = False
        self.is_at_left = False
        self.is_at_right = False
        self.is_at_corner = False
        self.trail = []
        self.distance_to_nearest_bush = 0
        self.awareness_rad = 200
        self.step_size = 2

        self.eyes_vector_x = -math.sqrt(2) / 2
        self.eyes_vector_y = -math.sqrt(2) / 2

    def check_boundary_col(self):
        if (self.pos_x <= self.age and self.pos_y <= self.age) or (self.pos_x <= self.age and self.pos_y >= HEIGHT - self.age) or (self.pos_x >= WIDTH - self.age and self.pos_y <= self.age) or (self.pos_x >= WIDTH - self.age and self.pos_y >= HEIGHT - self.age):
            self.is_at_corner = True
        elif self.pos_x <= self.age:
            self.is_at_left = True
            #print("Left")
        elif self.pos_x >= WIDTH - self.age:
            self.is_at_right = True
            #print("Right")
        elif self.pos_y <= self.age:
            self.is_at_top = True
            #print("Top")
        elif self.pos_y >= HEIGHT - self.age:
            self.is_at_bottom = True
            #print("Bottom")
        else:
            self.is_at_top = self.is_at_bottom = self.is_at_left = self.is_at_right = False

    
    def draw(self,win):
        pos_x = self.pos_x
        pos_y = self.pos_y
        pygame.draw.circle(win, (255,0,0), (pos_x,pos_y), self.age)

    def move(self):
        self.check_boundary_col()
        if self.is_at_corner:
            self.eyes_vector_x *= -1
            self.eyes_vector_y *= -1
        elif self.is_at_left or self.is_at_right:
            self.eyes_vector_x *= -1
        elif self.is_at_top or self.is_at_bottom:
            self.eyes_vector_y *= -1
        
        self.pos_x += self.step_size * self.eyes_vector_x
        self.pos_y += self.step_size * self.eyes_vector_y
        self.trail.append((self.pos_x,self.pos_y))
        self.is_at_left = self.is_at_right = self.is_at_top = self.is_at_bottom = self.is_at_corner = False

    def wander(self):
        self.move()


    def near_food(self, bush):
        dx = bush.pos_x - self.pos_x
        dy = bush.pos_y - self.pos_y
        self.distance_to_nearest_bush = math.sqrt(dx**2 + dy**2)
        if self.distance_to_nearest_bush <= self.awareness_rad:
            self.is_near_food = True

    def move_towards_food(self,bush):
        dx = bush.pos_x - self.pos_x
        dy = bush.pos_y - self.pos_y
        distance = math.sqrt(dx**2 + dy**2)
        self.eyes_vector_x = dx / distance
        self.eyes_vector_y = dy / distance
        self.move()
        




def main():
    run = True
    clock = pygame.time.Clock()
    bushes = []
    
    george = Rabbit(100,100,5)
    harry = Rabbit(200,200,7)
    rabbits = [george,harry]
    
    while run:
        clock.tick(15)
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
                        if abs(rabbit.distance_to_nearest_bush) < 50:
                            bushes.remove(bush)
                            print("yum")
                            rabbit.is_near_food = False
                    else:
                        rabbit.wander()
                else:
                    rabbit.wander()

            rabbit.draw(WIN)


        pygame.display.update()
        
        
    pygame.quit()

main()
