import pygame

class ImageLoader:
    '''Attempts to load image or any combination of sub-images.'''
    def __init__(self, filename):
        try:
            self.image = pygame.image.load(filename)
            self.rect = self.image.get_rect()
        except pygame.error, message:
            print 'Unable to load image:', filename
            #print message
            raise SystemExit

    # Load one sub-image from image given position as Rect object
    def load(self, rect=None):
        if rect == None:
            rect = self.rect
        image = pygame.Surface(rect.size)
        image.blit(self.image, (0, 0), rect)
        return image

    # Load images given positions as Rects, return as list of images
    def load_list(self, rects):
        return [self.load(rect) for rect in rects]

    # Load a strip of images given position of first image as Rect object
    # (Note: The images have to be the same size.)
    def load_strip(self, rect, image_count):
        tuples = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                  for x in range(image_count)]
        return self.load_list(tuples)


def test():
    pass

if __name__ == '__main__':
    test()
