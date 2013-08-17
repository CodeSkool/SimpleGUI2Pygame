#!/usr/local/bin/python

# import the module(s) to test
import camera
import camera_manager

# import pyunit
import unittest


# create a test class
class Test_DefaultCamera(unittest.TestCase):
    """Test the camera base class"""
    def setUp(self):
        self.target = camera.DefaultCamera()

    # Tests:
    # camera.update(source, target)
    def test_DefaultCamera_update(self):
        s1 = Mock_Surface("source")
        s2 = Mock_Surface("target")
        expected = "source blitted onto target"
        self.target.update(s1, s2)
        actual = s1.output
        self.assertEqual(expected, actual)


class Mock_Surface():
    def __init__(self, name):
        self.name = name
        self.output = None

    def blit(self, target):
        self.output = self.name + " blitted onto " + target.name
        
        
class Test_CameraManager(unittest.TestCase):
    '''
    Test the camera manager.
    '''
        
    # Tests:
    # CameraManager(emptylist)
    # CameraManager.update(source, target) with 1 camera passed in list
    # CameraManager.update(source, target) with no camera list passed
    # CameraManager.update(source, target) with 5 cameras passed in list
    def test_CameraManager_emptylist(self):
        cam_list = []
        self.assertRaises(AssertionError, lambda:
                          camera_manager.CameraManager(cam_list))
    
    def test_CameraManager_update_1(self):
        s1, s2 = "source", "target"
        mock_cam1 = Mock_Camera("cam1")
        cam1 = camera_manager.Cameras().append(mock_cam1)
        camera_manager.CameraManager(cam1).update(s1, s2)
        expected = "updated cam1"
        actual = mock_cam1.output
        self.assertEqual(expected, actual)
        
    def test_CameraManager_update_0(self):
        s1 = Mock_Surface("s1")
        s2 = Mock_Surface("s2")
        camera_manager.CameraManager().update(s1, s2)
        expected = "s1 blitted onto s2"
        actual = s1.output
        self.assertEqual(expected, actual)
        
    def test_CameraManager_update_5(self):
        s1, s2 = "source", "target"
        mock_cam_list = [Mock_Camera(str(i)) for i in range(5)]
        cam_list = camera_manager.Cameras().extend(mock_cam_list)
        camera_manager.CameraManager(cam_list).update(s1, s2)
        expected = ["updated " + str(i) for i in range(5)]
        actual = [cam.output for cam in cam_list]
        self.assertEqual(expected, actual)
                    

class Mock_Camera(camera.Camera):
    # COMMENT: Mock_Camera
    def __init__(self, name):
        self.name = name
        self.output = None
        
    def update(self, source, target):
        self.output = "updated " + self.name


if __name__ == '__main__':
    # run the unit tests
    unittest.main()
    
