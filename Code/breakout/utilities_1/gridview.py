#!/usr/local/bin/python


def get_grid_points(source_size, columns, rows):
    '''source_size = 2 element list or tuple of width and height
       columns and rows must be >= 1
    Returns list of point locations in the format:
    points[row][column][(location), (size)]'''
    size = source_size[0] // columns, source_size[1] // rows
    return [[[(col * size[0], row * size[1]), size] for col in range(columns)]
              for row in range(rows)]        


def main():
    x = get_grid_points((300, 300), 2, 2)
    for row in x:
        print row
    
if __name__ == '__main__':
    main()
