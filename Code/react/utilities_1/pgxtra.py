#!/usr/local/bin/python

#-------------------------------------------------------------------------------
# Name:        pgxtra
# Purpose:     Provides extra controls for pygame.
# Author:      Jules
# Created:     06/29/2013
# Copyright:   (c) Julie Ann Stoltz 2013
# Licence:     DBAD (refer to http://www.dbad-license.org/)
#-------------------------------------------------------------------------------

import pygame, sys

LEGAL_KEYS = {pygame.K_q: 'q', pygame.K_w: 'w', pygame.K_e: 'e',
              pygame.K_r: 'r', pygame.K_t: 't', pygame.K_y: 'y',
              pygame.K_u: 'u', pygame.K_i: 'i', pygame.K_o: 'o',
              pygame.K_p: 'p', pygame.K_a: 'a', pygame.K_s: 's',
              pygame.K_d: 'd', pygame.K_f: 'f', pygame.K_g: 'g',
              pygame.K_h: 'h', pygame.K_j: 'j', pygame.K_k: 'k',
              pygame.K_l: 'l', pygame.K_z: 'z', pygame.K_x: 'x',
              pygame.K_c: 'c', pygame.K_v: 'v', pygame.K_b: 'b',
              pygame.K_n: 'n', pygame.K_m: 'm', pygame.K_SPACE: ' '}


class PgxtraWidget(pygame.sprite.Sprite):
    def __init__(self, screen, label, text_color, bg_color, location,
                 size, func_call, font_size = 40, len_cap = 0):
        '''
        Attributes:
           screen = display screen
           label = string of text on widget
           text_color = rgb color value of label text
           bg_color = rgb color value of widget background
           x_location = x coord of top left corner of widget
           y_location = y coord of top left corner of widget
           width, height = size of widget
           func_call = function that will handle widget event
           font_size = default set to 40
           len_cap = default set to 0, character cap on label

        Widget label text will be centered on the widget.
        If widget is clickable, upon left button press, colors of text & bg
        will reverse. Upon left button release, they will return to normal.

        self.enabled = True if the widget is clickable
        '''

        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.label = label
        self.default_label = label
        self.text_color = text_color
        self.bg_color = bg_color
        self.location = location
        self.size = size
        self.func_call = func_call
        self.font_size = font_size
        self.len_cap = len_cap

        self.image = pygame.Surface(self.size)
        self.image.fill(bg_color)

        rect = self.image.get_rect()
        self.rect = (rect[0]+location[0], rect[1]+location[1], rect[2], rect[3])
        self.surface_rect = None
        self.enabled = True
        pygame.mouse.set_visible(True)

    def draw(self):
        rect = pygame.draw.rect(self.screen, self.bg_color, self.rect)
        self.surface_rect = rect
        font = pygame.font.Font(None, self.font_size)
        text = font.render(self.label, 1, self.text_color)
        size = font.size(self.label)
        textpos = ((self.size[0] - size[0]) // 2 + self.location[0],
                   (self.size[1] - size[1]) // 2 + self.location[1])
        self.screen.blit(text, textpos)

    def is_clickable(self):
        return self.enabled

    def click_release(self):
        if self.enabled and self.pressed:
            self.bg_color, self.text_color = self.text_color, self.bg_color
            self.pressed = False
            self.func_call(self)

    def click_press(self):
        self.bg_color, self.text_color = self.text_color, self.bg_color
        self.pressed = True

    def get_surface_rect(self):
        return self.surface_rect

    def get_label(self):
        return self.label

    def get_default_label(self):
        return self.default_label

    def change_label(self, new_label):
        if self.len_cap:
            if len(new_label) <= self.len_cap:
                self.label = new_label
        else:
            self.label = new_label

    def call(self):
        self.func_call(self.label)

    def disable(self):
        self.enabled = False

    def check_event(self, event):
        if self.is_clickable():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect <> None and surface_rect.collidepoint(pos):
                    self.click_press()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect <> None and surface_rect.collidepoint(pos):
                    self.click_release()


class Button(PgxtraWidget):
    pass


class InputField(PgxtraWidget):
    def click_release(self):
        if self.enabled and self.pressed:
            self.bg_color, self.text_color = self.text_color, self.bg_color
            self.pressed = False

    def click_press(self):
        self.bg_color, self.text_color = self.text_color, self.bg_color
        self.pressed = True
        self.change_label("")

    def check_event(self, event):
        if self.is_clickable():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect <> None and surface_rect.collidepoint(pos):
                    self.click_press()
                    response = ""
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect <> None and surface_rect.collidepoint(pos):
                    self.click_release()

            label = self.get_label()
            default_label = self.get_default_label()
            response = label[:]
            if event.type == pygame.KEYDOWN:
                if label == default_label:
                    self.change_label('')
                    response = self.label[:]

                if event.key in LEGAL_KEYS:
                    response += LEGAL_KEYS[event.key]

                elif event.key == pygame.K_BACKSPACE:
                    response = response[:-1]

                elif event.key == pygame.K_RETURN:
                    self.call()
                    #self.disable()

                if label != response:
                    self.change_label(response)


def print_name(obj):
    print obj, "clicked"

def test():
    # Initialize pygame
    pygame.init()

    # Define the colors we will use in RGB format
    BLACK = pygame.Color('black')
    WHITE = pygame.Color('white')
    BLUE =  pygame.Color('blue')
    GREEN = pygame.Color('green')
    RED =   pygame.Color('red')

    # Set the height, width and caption of the screen
    size = [400, 300]
    global screen
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Example")

    # Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()

    # Create 2 buttons
    btn1 = Button(screen, 'Play', WHITE, RED, (50, 25), (200, 50), print_name)
    btn2 = Button(screen, 'Load Save Point', WHITE, RED, (50, 125), (200, 50),
                  print_name, 24)

    # Create 1 input field
    inp_fld = InputField(screen, 'Enter Name', BLUE, WHITE, (50, 225), (200, 50),
                         print_name, len_cap = 12)

    pgxtra_widgets = [btn1, btn2, inp_fld]
    response = ""

    while not done:
        # Limit fps to 30
        clock.tick(30)

        # Check for applicable events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            else:
                for widg in pgxtra_widgets:
                    widg.check_event(event)

        # Iterate through all widgets and draw them
        for widg in pgxtra_widgets:
            widg.draw()

        # Display all drawn items to the screen
        pygame.display.flip()

def main():
    test()

if __name__ == '__main__':
    main()
