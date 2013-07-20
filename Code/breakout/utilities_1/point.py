
class Point:
    '''Creates coordinate point with X and Y properties.'''
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    # X property
    def getx(self):
        return self.__x

    def setx(self, x):
        self.__x = x

    x = property(getx, setx)

    # Y property
    def gety(self):
        return self.__y

    def sety(self, y):
        self.__y = y

    y = property(gety, sety)


def test():
    pass

if __name__ == '__main__':
    test()
