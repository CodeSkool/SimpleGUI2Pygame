#!/usr/local/bin/python

#import pygame


class Camera(object):
    
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
    
    # topleft position property
    def _getpos(self):
        return self.rect.topleft
    
    def _setpos(self, pos):
        self.rect.topleft = pos
        
    topleft = property(_getpos, _setpos)
    
    # center position property
    def _getcenter(self):
        return self.rect.center
    
    def _setcenter(self, pos):
        self.rect.center = pos
        
    center = property(_getcenter, _setcenter)
    
    # width property
    def _getwidth(self):
        return self.rect.width
    
    def _setwidth(self, value):
        self.rect.width = value
        
    width = property(_getwidth, _setwidth)
    
    # height property
    def _getheight(self):
        return self.rect.height
    
    def _setheight(self, value):
        self.rect.height = value
        
    height = property(_getheight, _setheight)
    
    def update(self, source, target):
        pass


class DefaultCamera(Camera):
    def update(self, source, target):
        source.blit(target)
    
       

def main():
    camera = Camera()
    print type(camera)
    def_cam = DefaultCamera()
    print type(def_cam)

if __name__ == '__main__':
    main()
