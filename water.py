import pygame, random, math
pygame.init()

WIDTH, HEIGHT = 200,200
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Quadrant View")



def look_new_dir(river_willing_to_turn,river_vector_x,river_vector_y,i):
    turn = random.randint(-(50+i),50+i) * math.pi / 50
    turn_x = math.cos(turn)
    turn_y = math.sin(turn)
    new_mag = math.sqrt((river_vector_x + turn_x) ** 2 + (river_vector_y + turn_y) ** 2)
    river_vector_x = (river_vector_x + turn_x) / new_mag
    river_vector_y = (river_vector_y + turn_y) / new_mag
    return river_vector_x, river_vector_y


def main():
    run = True
    clock = pygame.time.Clock()
    numb_bushes = 400
    bush_rad = 2
    bush_coords = []
    bush_i = 0


    unique_bushes = set(bush_coords)

    river_pos_x, river_pos_y = random.randint(0,WIDTH), random.randint(0,HEIGHT)
    river_trail = []
    river_willing_to_turn = 180

    river_vector_x = 0
    river_vector_y = -1

    length_of_river = 400
    water_rad = 10
    i = 0

    for i in range(length_of_river):
        river_vector_x, river_vector_y = look_new_dir(river_willing_to_turn,river_vector_x,river_vector_y,i)
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

    print(len(unique_bushes))

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

    print(len(unique_bushes))



    while run:
        clock.tick(30)
        WIN.fill((201,173,153))
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for point in river_trail:
            pygame.draw.circle(WIN, (153,177,201), point, water_rad)

        for bush in unique_bushes:
            pygame.draw.circle(WIN, (0,255,0), bush, bush_rad)

        pygame.display.update()

    pygame.quit()
    

main()