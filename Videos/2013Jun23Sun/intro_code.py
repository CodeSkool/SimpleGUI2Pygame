import pygame, sys

def frame():
    title = "Hello Pygame"
    width = 640
    height = 480

    pygame.init()
    fpsClock = pygame.time.Clock()

    my_surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main():
    frame()

if __name__ == '__main__':
    main()