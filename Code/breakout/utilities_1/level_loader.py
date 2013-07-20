import re

__ = tuple('1' * 120)
DEMO_LEVEL = tuple([int(x) for x in __])

# Classes
class LevelLoader:
    '''Loads level info.'''
    def __init__(self, filename):
        self.filename = filename
        self.num_levels = 1

    def open_file(self):
        '''Tries to open the file. Reports file missing and runs with demo level
        if not found.'''
        try:
            with open(self.filename, 'r') as file:
                text = file.read()
                levels = self.extract_levels(text)
        except IOError:
            print 'Dependent file "' + self.filename + '" missing.'
            print 'Operating in demo mode.'
            levels = DEMO_LEVEL
        return levels

    def extract_levels(self, levels):
        '''Returns a tuple of levels, each level is a tuple of integers. Also
        updates self.num_levels with the correct number of levels.'''
        working_list = []
        # Split into lines
        step1 = levels.split("\n")
        for index, line in enumerate(step1):
            # Remove any comments
            if line[0:2] != '##':
                working_list.append(line)
        # Extract key information (total number of levels and lines per level)
        info = working_list[0].split(", ")
        #working_list.pop(0)
        self.num_levels = int(info[0])
        num_lines = int(info[1])
        # Create tuples of levels
        tuples = []
        for i in range(self.num_levels):
            level = ""
            for j in range(num_lines):
                next_line = working_list[10 * i + i + j + 1]
                if len(next_line) > 3:
                    level += next_line
            # Convert string to tuple
            t = tuple(int(v) for v in re.findall("[0-9]+", level))
            tuples.append(t)
        levels = tuple(tuples)
        return levels

    def get_num_levels(self):
        return self.num_levels


def test():
    levels = LevelLoader("resources\\levels.txt")
    levels.open_file()
    x = levels.get_num_levels()
    print x

if __name__ == '__main__':
    test()