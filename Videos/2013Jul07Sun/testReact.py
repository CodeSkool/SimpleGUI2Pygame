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

RED    = pygame.Color(255,  0,  0,255)
GREEN  = pygame.Color(  0,255,  0,255)
BLUE   = pygame.Color(  0,  0,255,255)
YELLOW = pygame.Color(255,255,  0,255)
LTBLUE = pygame.Color(  0,255,255,255)
PURPLE = pygame.Color(255,  0,255,255)
LIME   = pygame.Color(  0,127,200,255)
VIOLET = pygame.Color(127,127,255,255)
PINK   = pygame.Color(127,  0,200,255)
BLACK  = pygame.Color(  0,  0,  0,255)
WHITE  = pygame.Color(255,255,255,255)

COLORS = [RED, GREEN, BLUE, YELLOW, LTBLUE, PURPLE, LIME, VIOLET, PINK]

class Square:
    def __init__(self, ui, surface, location, size, color, spawn_time)
        self.ui = ui
        self.surface = surface
        self.location = location
        self.size = size
        self.color = color
        self.spawn_time = spawn_time
        self.rect = self.ui.draw_rect(surface, location, size, color)

    def get_spawn_time(self):
        return self.spawn_time

    def handler(self, pos):
        if self.rect.collidepoint(pos):




# Classes
class Squares(pygame.sprite.Sprite):

    def __init__(self, surface, size, color, shapes):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.size = size
        self.color = color
        self.clickable = True

        # Create surface and fill
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)

        # Get unique random position and random velocity
        self.rand_pos(self.size, shapes)
        self.rand_vel()
        self.last_vel = [0,0]

        # Get rect for surface and update with position
        self.rect = self.image.get_rect()
        self.rect.center = self.get_pos()

        # Draw square
        self.square = pygame.draw.rect(self.image, self.color, self.rect)

    def rand_pos(self, size, shapes):
        '''Selects random start position.'''
        xpos = random.randrange(size, W - size)
        ypos = random.randrange(size, H - size)
        pos = [xpos, ypos]
        rect = pygame.Rect(0,0,size, size)
        rect.center = pos
        unique = self.is_unique(rect, shapes)
        if not unique:
            self.rand_pos(size, shapes)
        else:
            self.pos = pos
            return pos

    def rand_vel(self):
        '''Selects random start velocity.'''
        xvel = random.choice([-3,-2,-1,1,2,3])
        yvel = random.choice([-3,-2,-1,1,2,3])
        self.vel = [xvel, yvel]
        return self.vel

    def is_unique(self, rect, shapes):
        '''Verifies start position is unique.'''
        if shapes.sprites() == None:
            return True
        for shape in shapes:
            if rect.colliderect(shape):
                return False
        return True

    def draw(self):
        self.surface.blit(self.image, self.pos)

    def update(self, hitlist):
        # If collide with other object, switch velocities
        if self in hitlist:
            for other in hitlist[self]:
                other_vel = other.get_vel()

                # Check that both objects have different velocities
                if self.vel != other_vel:
                    next_vel, other_vel = other_vel, self.vel

                # If the objects are the same velocity, make both have new
                # velocities
                else:
                    next_vel = self.rand_vel()
                    other_vel = self.rand_vel()

                # If the next_vel isn't the last vel, update
                if next_vel != self.last_vel:
                    self.vel, self.last_vel = next_vel, self.vel

                # Update the other objects velocity
                other.change_vel(other_vel)

        # Update position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # If near edges, reverse direction
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.vel[0] *= -1
        elif self.pos[0] > W - self.size:
            self.pos[0] = W - self.size
            self.vel[0] *= -1
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.vel[1] *= -1
        elif self.pos[1] > H - self.size:
            self.pos[1] = H - self.size
            self.vel[1] *= -1

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

    def get_pos(self):
        return self.pos


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption('Test')
    surface = pygame.Surface(screen.get_size())
    surface.convert()
    surface.fill(BLACK)

    shapes = pygame.sprite.Group()

    while len(shapes) < 30:
        for i in range(len(COLORS)):
            obj1 = Square(surface, 35, COLORS[i], shapes)

            #obj2 = Circle(surface, 35, COLORS[i], shapes)
            shapes.add(obj1)

    while True:
        clock.tick(30)
        surface.fill(BLACK)

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
