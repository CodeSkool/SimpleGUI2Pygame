import pygame
import point


class BaseSprite(pygame.sprite.Sprite):
    '''Base class to create image objects that expands the pygame class.'''
    def __init__(self, filename=None, width=0, height=0, columns=1,
                 expire=False):
        pygame.sprite.Sprite.__init__(self)

        self.original_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = 0
        self.velocity = point.Point(0.0, 0.0)
        self.expire = expire

        if filename != None:
            import imageloader
            image = imageloader.ImageLoader(filename).load()
            self.set_image(image, width, height, columns)

    # X property
    def _getx(self):
        return self.rect.x

    def _setx(self, value):
        self.rect.x = value

    X = property(_getx, _setx)

    # Y property
    def _gety(self):
        return self.rect.y

    def _sety(self, value):
        self.rect.y = value

    Y = property(_gety, _sety)

    # position property
    def _getpos(self):
        return self.rect.topleft

    def _setpos(self, pos):
        self.rect.topleft = pos

    position = property(_getpos, _setpos)

    def set_image(self, image=None, width=0, height=0, columns=1):
        if image != None:
            self.original_image = image
        if width == 0 and height == 0:
            self.frame_width = image.get_width()
            self.frame_height = image.get_height()
        else:
            self.frame_width = width
            self.frame_height = height
            rect = self.original_image.get_rect()
            self.last_frame = (rect.width // width) * (rect.height // height)
            self.last_frame -= 1
        self.rect = pygame.Rect(0, 0, self.frame_width, self.frame_height)
        self.columns = columns

    def update(self, rate=30):
        # Handles animation if applicable
        current_time = pygame.time.get_ticks()

        # Change image if necessary
        if self.frame != self.old_frame:
            frame_x = self.frame % self.columns * self.frame_width
            frame_y = self.frame // self.columns * self.frame_height
            rect = pygame.Rect(frame_x, frame_y, self.frame_width,
                               self.frame_height)
            self.image = self.original_image.subsurface(rect)
            self.old_frame = self.frame

        # # Handles animation if applicable
        if self.columns > 1:
            if current_time > self.last_time + rate:
                self.frame += 1
                if self.expire and self.frame > self.last_frame:
                    self.kill()
                else:
                    self.frame %= (self.last_frame + 1)
                    self.last_time = current_time
                    
    def get_frame_y(self, frame, columns, height):
        """
        >>> bs = BaseSprite()
        >>> bs.get_frame_y(0, 30, 32)
        0
        >>> bs.get_frame_y(1, 30, 32)
        0
        >>> bs.get_frame_y(6, 5, 32)
        32
        """
        return (frame / columns) * height



def test():
    import doctest
    failed = 0
    result = doctest.testmod()
    # result returns a tuple (failed=0, attempted=0)
    print result
    if result[failed]:
        pass
    else:
        pass



if __name__ == '__main__':
    test()
