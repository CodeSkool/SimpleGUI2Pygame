#!/usr/local/bin/python

import camera

class Cameras(list):
    def __init__(self):
        list.__init__(self)
        
    def append(self, cam):
        assert isinstance(cam, camera.Camera), "camera must be a Camera object"
        list.append(self, cam)
        return self
    
    def extend(self, camera_list):
        for camera in camera_list:
            self.append(camera)
        return self
        
    def sort(self, cmp=None, key=None, reverse=False):
        # In-place sort: self is updated; return self
        list.sort(self, cmp, key, reverse)
        return self
    
    def sorted(self, cmp=None, key=None, reverse=False):
        return Cameras().extend(self).sort(cmp, key, reverse)
    
class CameraManager:
    def __init__(self, camera_list=None):
        if camera_list == None:
            camera_list = Cameras().append(camera.DefaultCamera())
        assert isinstance(camera_list, Cameras), "camera_list must be Cameras object"
        self.cameras = camera_list
        
    def update(self, source, target):
        for camera in self.cameras:
            camera.update(source, target)
            

def main():
    CameraManager()
    
if __name__ == '__main__':
    main()
