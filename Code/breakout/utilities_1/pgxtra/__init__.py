from pgxtra_widget import PgxtraWidget
from button import Button
from input_field import InputField
from special_button import SpecialButton

import pygame, sys

class Tester():
    def print_clicked(self):
        print "Clicked"

    def enter_field(self, obj):
        print obj, "entered"

    def test(self):
        # Initialize pygame
        pygame.init()

        # Define the colors we will use in RGB format
        BLACK = pygame.Color('black')
        WHITE = pygame.Color('white')
        BLUE =  pygame.Color('blue')
        GREEN = pygame.Color('green')
        RED =   pygame.Color('red')

        # Set the height, width and caption of the screen
        size = [800, 500]
        global screen
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Example")

        # Loop until the user clicks the close button.
        done = False
        clock = pygame.time.Clock()

        # Create 2 buttons
        btn1 = Button('Play', BLACK, RED, (50, 25), (200, 50),
                      self.print_clicked)
        btn2 = Button('Load Save Point', WHITE, RED, (50, 125), (200, 50),
                      self.print_clicked, 24)

        # Create 1 input field
        inp_fld1 = InputField('Enter Name', BLUE, WHITE, (50, 225), (200, 50),
                             lambda obj: self.enter_field(obj), len_cap = 12,
                             focus=True)

        inp_fld2 = InputField('Enter Color', BLUE, WHITE, (50, 325), (200, 50),
                             lambda obj: self.enter_field(obj), len_cap = 12)

        response = ""

        # Create 4 special buttons if file is present
        try:
            button_pic = pygame.image.load('prettybuttons.png')

            spc_btn1 = SpecialButton(button_pic, (400, 25), (226, 75),
                                     (8, 92), self.print_clicked,
                                     hover_offset=(240, 0),
                                     press_offset=(480, 0),
                                     disable_offset=(720, 0))

            spc_btn2 = SpecialButton(button_pic, (400, 125), (226, 75),
                                     (8, 428), self.print_clicked,
                                     hover_offset=(240, 0),
                                     press_offset=(480, 0),
                                     disable_offset=(720, 0))

            spc_btn3 = SpecialButton(button_pic, (400, 225), (226, 75),
                                     (8, 680), self.print_clicked,
                                     hover_offset=(240, 0),
                                     press_offset=(480, 0),
                                     disable_offset=(720, 0))

            spc_btn4 = SpecialButton(button_pic, (400, 325), (226, 75),
                                     (8, 848), self.print_clicked,
                                     hover_offset=(240, 0),
                                     press_offset=(480, 0),
                                     disable_offset=(720, 0))

            spc_btn1.disable()

        except:
            print "Unable to test special buttons: 'prettybuttons.png' missing"



        while not done:
            # Limit fps to 30
            clock.tick(30)

            # Check for applicable events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                else:
                    for widg in PgxtraWidget._pgutility.get_widgets():
                        widg.check_event(event)

            # Iterate through all widgets and draw them
            for widg in PgxtraWidget._pgutility.get_widgets():
                widg.draw(screen)

            # Display all drawn items to the screen
            pygame.display.flip()

def main():
    Tester().test()



if __name__ == '__main__':
    main()