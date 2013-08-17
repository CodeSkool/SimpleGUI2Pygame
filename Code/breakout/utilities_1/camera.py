#!/usr/local/bin/python

#import pygame


class Camera(object):
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
