#!/usr/local/bin/python

#-------------------------------------------------------------------------------
# Name:        Test classes for React
# Purpose:
# Author:      Jules
# Created:     07/08/2013
# Copyright:   (c) Julie Ann Stoltz 2013
# Licence:     DBAD (refer to http://www.dbad-license.org/)
#-------------------------------------------------------------------------------
import pygame
import sys
import random

# CONSTANTS
W, H = 640, 480

COLORS = {'Name'  :('r','g','b','a'),
          'red'   :pygame.Color(255,  0,  0,255),
          'green' :pygame.Color(  0,255,  0,255),
          'blue'  :pygame.Color(  0,  0,255,255),
          'yellow':pygame.Color(255,255,  0,255),
          'ltblue':pygame.Color(  0,255,255,255),
          'purple':pygame.Color(255,  0,255,255),
          'lime'  :pygame.Color(  0,127,200,255),
          'violet':pygame.Color(127,127,255,255),
          'pink'  :pygame.Color(127,  0,200,255)}
color = ['red','green','blue','yellow','ltblue','purple','lime','violet','pink']


# Classes
class Square(pygame.sprite.Sprite):

    def __init__(self, surface, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.size = size
        self.color = color
        self.clickable = True

        # Get random start position and velocity
        xpos = random.randrange(size, W - size)
        ypos = random.randrange(size, H - size)
        self.pos = [xpos, ypos]

        xvel = random.randrange(-5, 5)
        yvel = random.randrange(-5, 5)
        self.vel = [xvel, yvel]

        # Create surface and draw square
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.square = pygame.draw.rect(self.image, self.color, self.rect)

    def draw(self):
        self.surface.blit(self.image, self.pos)

    def update(self, hitlist):
        # If collide with other object, switch velocities
        if self in hitlist:
            other_vel = hitlist[self][0].get_vel()
            self.vel, other_vel = other_vel, self.vel
            hitlist[self][0].change_vel(other_vel)

        # Update position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # If near edges, reverse direction
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.vel[0] = -self.vel[0]
        elif self.pos[0] > W - self.size:
            self.pos[0] = W - self.size
            self.vel[0] = -self.vel[0]
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.vel[1] = -self.vel[1]
        elif self.pos[1] > H - self.size:
            self.pos[1] = H - self.size
            self.vel[1] = -self.vel[1]

        # Update self.rect position
        self.rect.topleft = self.pos

    def check_event(self, pos):
        if self.clickable:
            if self.rect.collidepoint(pos):
                self.kill()
                return True

    def get_vel(self):
        return self.vel

    def change_vel(self, new_vel):
        self.vel = new_vel


class Circle(pygame.sprite.Sprite):

    def __init__(self, surface, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.radius = size / 2
        self.size = size
        self.color = color
        self.clickable = True

        # Get random start position and velocity
        xpos = random.randrange(size, W - size)
        ypos = random.randrange(size, H - size)
        self.pos = [xpos, ypos]

        xvel = random.randrange(-5, 5)
        yvel = random.randrange(-5, 5)
        self.vel = [xvel, yvel]

        # Find center point
        centerx = self.pos[0] + self.radius
        centery = self.pos[1] + self.radius
        self.center = (centerx, centery)

        # Create surface and draw circle
        self.image = pygame.Surface((self.size, self.size))
        self.rect = pygame.draw.circle(self.image, self.color,
                                         self.center, self.radius)

    def draw(self):
        self.surface.blit(self.image, self.pos)

    def update(self, hitlist):
        # If collide with other object, switch velocities
        if self in hitlist:
            other_vel = hitlist[self][0].get_vel()
            self.vel, other_vel = other_vel, self.vel
            hitlist[self][0].change_vel(other_vel)

        # Update position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # If near edges, reverse direction
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.vel[0] = -self.vel[0]
        elif self.pos[0] > W - self.size:
            self.pos[0] = W - self.size
            self.vel[0] = -self.vel[0]
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.vel[1] = -self.vel[1]
        elif self.pos[1] > H - self.size:
            self.pos[1] = H - self.size
            self.vel[1] = -self.vel[1]

        # Update self.rect position
        self.rect.topleft = self.pos

    def check_event(self, pos):
        if self.clickable:
            if self.rect.collidepoint(pos):
                self.kill()
                return True

    def get_vel(self):
        return self.vel

    def change_vel(self, new_vel):
        self.vel = new_vel


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption('Test')
    surface = pygame.Surface(screen.get_size())
    surface.convert()
    surface.fill(pygame.Color(0,0,0,0))

    shapes = pygame.sprite.Group()

    for i in range(len(color)):
        obj1 = Square(surface, 35, COLORS[color[i]])
        obj2 = Circle(surface, 35, COLORS[color[i]])
        shapes.add(obj1)

    while True:
        clock.tick(30)
        surface.fill(pygame.Color(0,0,0,0))

        shape_copy = pygame.sprite.Group(shapes)
        for shape in shapes:
            shape_copy.remove(shape)
            shape_one = pygame.sprite.GroupSingle(shape)
            collisions = pygame.sprite.groupcollide(shape_one, shape_copy,
                                                    False, False)
            shape.update(collisions)
            shape_one.empty()

        shapes.draw(surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for shape in shapes:
                    if shape.check_event(pos):
                        break

        screen.blit(surface, (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    main()
