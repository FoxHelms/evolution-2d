import pygame, random, math
from water import look_new_dir as river_wander
pygame.init()

WIDTH, HEIGHT = 200,200
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Quadrant View")



class Rabbit:
    def __init__(self,pos_x,pos_y,age):
        self.pos_x = int(pos_x)
        self.pos_y = int(pos_y)
        self.age = age


        self.is_hungry = True
        self.is_horny = False
        self.is_near_food = False
        self.is_at_top = False
        self.is_at_bottom = False
        self.is_at_left = False
        self.is_at_right = False
        self.is_at_corner = False
        self.is_at_water = False
        #self.trail = []
        self.distance_to_bushes = []
        self.distance_to_nearest_bush = 0
        self.awareness_rad = 20
        self.step_size = 2
        self.internal_timer = random.randint(1,age)
        self.starve_timer = 0
        self.willing_to_turn = 180
        self.bushes_eaten = 0
        self.bush_bunny_can_see = []
        self.hot_single_rabbits = []
        self.bush_distances = []
        self.color = (255,0,0)
        self.hunger_level = 0
        

        self.eyes_vector_x = 0
        self.eyes_vector_y = -1

    def check_boundary_col(self):
        if (self.pos_x <= self.age and self.pos_y <= self.age) or (self.pos_x <= self.age and self.pos_y >= HEIGHT - self.age) or (self.pos_x >= WIDTH - self.age and self.pos_y <= self.age) or (self.pos_x >= WIDTH - self.age and self.pos_y >= HEIGHT - self.age):
            self.is_at_corner = True
        elif self.pos_x <= self.age:
            self.is_at_left = True
        elif self.pos_x >= WIDTH - self.age:
            self.is_at_right = True
        elif self.pos_y <= self.age:
            self.is_at_top = True
        elif self.pos_y >= HEIGHT - self.age:
            self.is_at_bottom = True
        else:
            self.is_at_top = self.is_at_bottom = self.is_at_left = self.is_at_right = False

    def check_water_col(self):
        for river in river_trail:
            rabbit_to_water = math.sqrt((self.pos_x - river[0])**2 + (self.pos_y - river[1])**2)
            if rabbit_to_water <= water_rad //2:
                self.is_at_water = True

    def draw(self,win):
        pos_x = self.pos_x
        pos_y = self.pos_y
        pygame.draw.circle(win, self.color, (pos_x,pos_y), self.age)

    def move(self):
        self.check_boundary_col()
        self.check_water_col()
        if self.is_at_corner or self.is_at_water:
            self.eyes_vector_x *= -1
            self.eyes_vector_y *= -1
        elif self.is_at_left or self.is_at_right:
            self.eyes_vector_x *= -1
        elif self.is_at_top or self.is_at_bottom:
            self.eyes_vector_y *= -1
        
        self.pos_x += self.step_size * self.eyes_vector_x
        self.pos_y += self.step_size * self.eyes_vector_y
        #self.trail.append((self.pos_x,self.pos_y))
        self.is_at_left = self.is_at_right = self.is_at_top = self.is_at_bottom = self.is_at_corner = self.is_at_water = False

    def look_new_dir(self):
        turn = random.randint(-self.willing_to_turn,0) * math.pi / 180
        turn_x = math.cos(turn)
        turn_y = math.sin(turn)
        new_mag = math.sqrt((self.eyes_vector_x + turn_x) ** 2 + (self.eyes_vector_y + turn_y) ** 2)
        self.eyes_vector_x = (self.eyes_vector_x + turn_x) / new_mag
        self.eyes_vector_y = (self.eyes_vector_y + turn_y) / new_mag

    def check_hunger(self):
        if self.internal_timer % 50 == 0:
            self.is_hungry = True
            self.color = (0,0,255)
            #print("{} is hungry again".format(self))
        if self.is_hungry and (self.hunger_level % 15 == 0):
            self.step_size = 1
            self.color = (0,0,0)
            self.starve_timer += 1

    def wander(self):
        if self.internal_timer % 15 == 0:
            #print("{} turning".format(self))
            self.look_new_dir()
            #print(self.eyes_vector_x,self.eyes_vector_y)
        self.move()


    
        

    def hunt(self,unique_bushes):
        self.count_bushes(unique_bushes)
        if self.bush_bunny_can_see:
            self.closest_bush_index, self.min_distance = self.get_closest_dist()
            if self.min_distance <= self.awareness_rad//4:
                try:
                    unique_bushes.remove(self.bush_bunny_can_see[self.closest_bush_index])
                    del self.bush_bunny_can_see[self.closest_bush_index]
                    self.bushes_eaten += 1
                    self.is_hungry = False
                    self.is_horny = True
                    self.starve_timer -= 1
                    self.hunger_level -= 1
                    self.color = (255,0,0)
                    self.step_size = 2
                except Exception:
                    #print("the index is: {}, the coordinates are {}".format(self.closest_bush_index,self.bush_bunny_can_see[self.closest_bush_index]))
                    pass
            if self.is_hungry:
                #pygame.draw.line(WIN,(0,0,255),(self.pos_x,self.pos_y),self.bush_bunny_can_see[self.closest_bush_index])
                food_x = self.bush_bunny_can_see[self.closest_bush_index][0] - self.pos_x
                food_y = self.bush_bunny_can_see[self.closest_bush_index][1] - self.pos_y
                self.eyes_vector_x = food_x / math.sqrt(food_x**2 + food_y**2)
                self.eyes_vector_y = food_y / math.sqrt(food_x**2 + food_y**2)
        self.move()

    def get_closest_dist(self):
        self.bush_distances.clear()
        for bush in self.bush_bunny_can_see:
            current_distance = math.sqrt((bush[0] - self.pos_x)**2 + (bush[1] - self.pos_y)**2)
            self.bush_distances.append(current_distance)
            
        min_distance = min(self.bush_distances)
        closest_bush_index = self.bush_distances.index(min_distance)
        return closest_bush_index, min_distance

    def count_bushes(self,unique_bushes):
        points = []
        self.bush_bunny_can_see.clear()
        for x in range(int(self.pos_x - self.awareness_rad),int(self.pos_x + self.awareness_rad)):
            for y in range(int(self.pos_y - int(math.sqrt(self.awareness_rad**2 - (x - int(self.pos_x))**2))),int(math.sqrt(self.awareness_rad**2 - (x - int(self.pos_x))**2) + int(self.pos_y))):
                points.append((x, y))
        for bush in unique_bushes:
            if bush in points:
                self.bush_bunny_can_see.append(bush)

    def find_mate(self,rabbits):
        points = []
        self.hot_single_rabbits.clear()
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if math.sqrt((x - self.pos_x)**2 + (y - self.pos_y)**2) < self.awareness_rad:
                    points.append((x, y))
        for rabbit in rabbits:
            if (rabbit.pos_x,rabbit.pos_y) in points:
                self.hot_single_rabbits.append(rabbit)
                print("I wanna mate with {}".format(rabbit))


    def repro(self,rabbits):
        self.find_mate(rabbits)

def draw_line(rabbit,bush_bunny_can_see):
    for bush in bush_bunny_can_see:
        pygame.draw.line(WIN,(255,0,0),(rabbit.pos_x,rabbit.pos_y),bush)


    


def main():
    run = True
    clock = pygame.time.Clock()
    numb_bushes = 400
    bush_rad = 2
    bush_coords = []
    bush_i = 0

    while bush_i < numb_bushes:
        bush_x = random.randint(0,WIDTH)
        bush_y = random.randint(0,HEIGHT)
        bush_coords.append((bush_x,bush_y))
        bush_i += 1

    unique_bushes = set(bush_coords)

    river_pos_x, river_pos_y = random.randint(0,WIDTH), random.randint(0,HEIGHT)
    global river_trail 
    river_trail= []
    river_willing_to_turn = 180

    river_vector_x = 0
    river_vector_y = -1

    length_of_river = 400
    global water_rad
    
    water_rad = 10
    i = 0

    for i in range(length_of_river):
        river_vector_x, river_vector_y = river_wander(river_willing_to_turn,river_vector_x,river_vector_y,i)
        river_pos_x += 4 * river_vector_x
        river_pos_y += 4 * river_vector_y
        river_trail.append((river_pos_x,river_pos_y))
        i += 1

    river_trail = set(river_trail)

    while bush_i < numb_bushes:
        bush_x = random.randint(0,WIDTH)
        bush_y = random.randint(0,HEIGHT)
        bush_coords.append((bush_x,bush_y))
        bush_i += 1

    unique_bushes = set(bush_coords)
    wet_bush = []

    for river in river_trail:
        for bush in unique_bushes:
            bush_to_water = math.sqrt((bush[0] - river[0])**2 + (bush[1] - river[1])**2)
            if bush_to_water <= water_rad:
                wet_bush.append(bush)

    for bush in wet_bush:
        try:
            unique_bushes.remove(bush)
        except:
            pass

    george = Rabbit(3*WIDTH / 4,3*HEIGHT / 4,5)
    harry = Rabbit(WIDTH / 4,HEIGHT / 4,3)
    barnum = Rabbit(1.5 * WIDTH / 4,1.5 * HEIGHT / 4,4)
    louis = Rabbit(WIDTH / 4,HEIGHT / 4,3)
    george1 = Rabbit(3*WIDTH / 4,3*HEIGHT / 4,5)
    harry1 = Rabbit(WIDTH / 4,HEIGHT / 4,3)
    barnum1 = Rabbit(1.5 * WIDTH / 4,1.5 * HEIGHT / 4,4)
    louis1 = Rabbit(WIDTH / 4,HEIGHT / 4,3)
    george2 = Rabbit(3*WIDTH / 4,3*HEIGHT / 4,5)
    harry2 = Rabbit(WIDTH / 4,HEIGHT / 4,3)
    barnum2 = Rabbit(1.5 * WIDTH / 4,1.5 * HEIGHT / 4,4)
    louis2 = Rabbit(WIDTH / 4,HEIGHT / 4,3)
    rabbits = [george,harry,barnum,louis,george1,harry1,barnum1,louis1,george2,harry2,barnum2,louis2]

    
    while run:
        clock.tick(30)
        WIN.fill((217,217,217))
        for bush in unique_bushes:
            pygame.draw.circle(WIN, (0,255,0), bush, bush_rad)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    george.awareness_rad += 5
                if event.key == pygame.K_DOWN:
                    george.awareness_rad -= 5
                    

        for point in river_trail:
            pygame.draw.circle(WIN, (153,177,201), point, water_rad)
        
        for rabbit in rabbits:
            if rabbit.starve_timer == 30:
                rabbits.remove(rabbit)
                print("dead wabbit")
            elif rabbit.is_hungry:
                rabbit.hunt(unique_bushes)
            #elif not rabbit.is_hungry and rabbit.is_horny:
                #rabbit.repro(rabbits)
            else:
                rabbit.wander()

            if rabbit.is_hungry:
                rabbit.hunger_level += 1
            rabbit.internal_timer += 1
                
            
            rabbit.check_hunger()
            rabbit.draw(WIN)
            #draw_line(rabbit,rabbit.bush_bunny_can_see)

        
        

        pygame.display.update()

    pygame.quit()
    for rabbit in rabbits:
        print("{} ate {} bushes".format(rabbit,rabbit.bushes_eaten))

main()