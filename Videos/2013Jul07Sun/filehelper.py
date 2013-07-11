import pickle

class FileHelper:
    def __init__(self, filename):
        self.filename = filename

    def open_file(self, file_name, mode):
        """Tries to open a file in the specified mode.
        If the file does not exist, opens it in a+ mode"""
        try:
            the_file = open(file_name, mode)
        except IOError:
            the_file = open(file_name, "a+")
        return the_file

    def save(self, object_to_save):
        """Pickle the object to the file"""
        with open(self.filename, "w") as file:
            pickle.dump(object_to_save, file)

    def load(self):
        """Unpickle the object from the file if it exists"""
        loaded_object = None
        file = self.open_file(self.filename, "r")
        if file.read(1) <> '':
           file.close()
           file = open(self.filename, "r")
           loaded_object = pickle.load(file)
        file.close()
        return loaded_object

def main():
    o = [1, 2, 3, {4:(5, 6, 7)}, "eight"]
    helper = FileHelper("test.pkl")
    helper.save(o)
    o2 = helper.load()
    assert o == o2, "invalid pickling"

if __name__ == '__main__':
    main()
