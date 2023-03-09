import pygame, random, math
pygame.init()

WIDTH, HEIGHT = 200,200
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Quadrant View")


#then I need to get the rabbit to be able to see the shrubs close to it

def count_bushes(bunny_x,bunny_aware,bunny_y,unique_bushes,bush_bunny_can_see):
    for x in range(int(bunny_x - bunny_aware), int(bunny_x + bunny_aware)):
            bunny_can_see_x = x
            bunny_can_see_pos_y = math.sqrt(bunny_aware**2 - (x - bunny_x)**2) + bunny_y
            bunny_can_see_neg_y = bunny_y - math.sqrt(bunny_aware**2 - (x - bunny_x)**2)

            for y in range (int(bunny_can_see_neg_y),int(bunny_can_see_pos_y)):
                for bush in unique_bushes:
                    if bush[0] == x and bush[1] == y:
                        bush_bunny_can_see.append(bush)


            # pygame.draw.circle(WIN, (0,0,255), (bunny_can_see_x,bunny_can_see_pos_y), 1)
            # pygame.draw.circle(WIN, (0,0,255), (bunny_can_see_x,bunny_can_see_neg_y), 1)
            print(len(bush_bunny_can_see))

def draw_line(bunny_x,bunny_y,bush_bunny_can_see):
    for bush in bush_bunny_can_see:
        pygame.draw.line(WIN,(255,0,0),(bunny_x,bunny_y),bush)


def main():
    run = True
    clock = pygame.time.Clock()
    numb_bushes = 400
    bush_rad = 2
    bush_coords = []
    i = 0
    bunny_x, bunny_y = WIDTH/2,HEIGHT/2
    speed = 10
    bunny_size = 10
    bunny_aware = 50
    bush_bunny_can_see = []

    while i < numb_bushes:
        bush_x = random.randint(0,200)
        bush_y = random.randint(0,200)
        bush_coords.append((bush_x,bush_y))
        i += 1

    unique_bushes = set(bush_coords)

    
    while run:
        clock.tick(15)
        WIN.fill((217,217,217))
        for bush in unique_bushes:
            pygame.draw.circle(WIN, (0,255,0), (bush[0],bush[1]), bush_rad)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bunny_aware += 5
                    count_bushes(bunny_x,bunny_aware,bunny_y,unique_bushes,bush_bunny_can_see)
                    print(bush_bunny_can_see)
                if event.key == pygame.K_DOWN:
                    bunny_aware -= 5
                    bush_bunny_can_see.clear()
                    count_bushes(bunny_x,bunny_aware,bunny_y,unique_bushes,bush_bunny_can_see)
                    print(bush_bunny_can_see)
                if event.key == pygame.K_w:
                    bush_bunny_can_see.clear()
                    bunny_y -= speed
                    count_bushes(bunny_x,bunny_aware,bunny_y,unique_bushes,bush_bunny_can_see)
                    print(bush_bunny_can_see)
                if event.key == pygame.K_a:
                    bush_bunny_can_see.clear()
                    bunny_x -= speed
                    count_bushes(bunny_x,bunny_aware,bunny_y,unique_bushes,bush_bunny_can_see)
                    print(bush_bunny_can_see)
                if event.key == pygame.K_s:
                    bush_bunny_can_see.clear()
                    bunny_y += speed
                    count_bushes(bunny_x,bunny_aware,bunny_y,unique_bushes,bush_bunny_can_see)
                    print(bush_bunny_can_see)
                if event.key == pygame.K_d:
                    bush_bunny_can_see.clear()
                    bunny_x += speed
                    count_bushes(bunny_x,bunny_aware,bunny_y,unique_bushes,bush_bunny_can_see)
                    print(bush_bunny_can_see)
            #if event.type == pygame.MOUSEBUTTONDOWN:
             #   pos_x,pos_y = pygame.mouse.get_pos()
             
       
        
        



        pygame.draw.circle(WIN, (255,0,0), (bunny_x,bunny_y), bunny_size)
        draw_line(bunny_x,bunny_y,bush_bunny_can_see)

        # draw line from bunny to all bushes it can see. 
        
        
        

        pygame.display.update()

    pygame.quit()

main()