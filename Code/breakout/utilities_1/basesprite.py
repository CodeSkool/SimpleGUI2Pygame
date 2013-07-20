import pygame
import point


class BaseSprite(pygame.sprite.Sprite):
    '''Base class to create image objects that expands the pygame class.'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = 0
        self.velocity = point.Point(0.0,0.0)

    # X property
    def _getx(self):
        return self.rect.x

    def _setx(self,value):
        self.rect.x = value

    X = property(_getx,_setx)

    # Y property
    def _gety(self):
        return self.rect.y

    def _sety(self,value):
        self.rect.y = value

    Y = property(_gety,_sety)

    # position property
    def _getpos(self):
        return self.rect.topleft

    def _setpos(self,pos):
        self.rect.topleft = pos

    position = property(_getpos,_setpos)

    def set_image(self, image, width=0, height=0, columns=1):
        self.image = image
        if width == 0 and height == 0:
            self.frame_width = image.get_width()
            self.frame_width = image.get_height()
        else:
            self.frame_width = width
            self.frame_height = height
            rect = self.image.get_rect()
            self.last_frame = (rect.width//width) * (rect.height//height) - 1
        self.rect = pygame.Rect(0, 0, self.frame_width, self.frame_height)
        self.columns = columns

    def update(self, rate=30):
        # Handles animation if applicable
        current_time = pygame.time.get_ticks()
        if self.last_frame > self.first_frame:
            if current_time > self.last_time + rate:
                self.frame += 1
                if self.frame > self.last_frame:
                    self.frame = self.first_frame
                self.last_time = current_time
        else:
            self.frame = self.first_frame

        # Change image if necessary
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = pygame.Rect(frame_x, frame_y, self.frame_width,
                               self.frame_height)
            self.image = self.image.subsurface(rect)
            self.old_frame = self.frame


def test():
    pass

if __name__ == '__main__':
    test()
