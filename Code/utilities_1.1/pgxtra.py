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

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.enabled = True
        pygame.mouse.set_visible(True)

    def draw(self, screen):
        pass

    def is_active(self):
        return self.enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def mouse_release(self):
        pass

    def mouse_press(self):
        pass

    def mouse_hover(self):
        pass

    def check_event(self, event):
        pass


class Button(PgxtraWidget):
    '''Creates a button on a solid colored rectangular background.
        Attributes:
           label = string of text on widget
           text_color = rgb color value of label text
           bg_color = rgb color value of widget background
           position = top left corner of widget
           btn_size = size of button
           func_call = function that will handle widget event
           font_size = default set to 40
           len_cap = default set to 0, character cap on label

        Widget label text will be centered on the widget.
        If widget is enabled, upon left button press, colors of text & bg
        will reverse. Upon left button release, they will return to normal,
        and upon hovering, an outline box will appear.

        self.enabled = True if the widget is active, default is True
        '''

    def __init__(self, label, text_color, bg_color, position,
                 btn_size, func_call, font_size=40, len_cap=0):
        PgxtraWidget.__init__(self)
        self.label = label
        self.default_label = label
        self.text_color = text_color
        self.bg_color = bg_color
        self.orig_bg_color = bg_color
        self.pos = position
        self.inner_pos = position[0] + 2, position[1] + 2
        self.inner_size = btn_size[0] - 4, btn_size[1] - 4
        self.outer_size = btn_size
        self.func_call = func_call
        self.font_size = font_size
        self.len_cap = len_cap
        self.rect = pygame.Rect(self.inner_pos, self.inner_size)
        self.hover = False
        self.outline_rect = pygame.Rect(self.pos, self.outer_size)

        self.render_label()

        # add widget to master list
        pgutility.add_button(self)

    def render_label(self):
        font = pygame.font.Font(None, self.font_size)
        text = font.render(self.label, 1, self.text_color)
        text_press = font.render(self.label, 1, self.bg_color)
        size = font.size(self.label)
        textpos = ((self.inner_size[0] - size[0]) // 2 + self.inner_pos[0],
                   (self.inner_size[1] - size[1]) // 2 + self.inner_pos[1])
        self.text_norm = text
        self.text_press = text_press
        self.text = self.text_norm
        self.textpos = textpos

    def draw(self, screen):
        if self.hover:
            pygame.draw.rect(screen, self.bg_color, self.outline_rect, 1)
        else:
            pygame.draw.rect(screen, self.text_color, self.outline_rect, 1)

        pygame.draw.rect(screen, self.bg_color, self.rect)
        screen.blit(self.text, self.textpos)

    def is_active(self):
        return self.enabled

    def mouse_release(self):
        if self.enabled and self.pressed and self.hover:
            self.bg_color, self.text = self.orig_bg_color, self.text_norm
            self.pressed = False
            self.func_call()

    def mouse_press(self):
        if self.enabled and self.hover:
            self.bg_color, self.text = self.text_color, self.text_press
            self.pressed = True

    def mouse_hover(self, hover):
        if hover:
            self.hover = True
        if not hover:
            self.hover = False
            self.bg_color, self.text = self.orig_bg_color, self.text_norm

    def get_surface_rect(self):
        return self.outline_rect

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
        self.render_label()

    def call(self):
        self.func_call()

    def check_event(self, event):
        if self.is_active():
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect != None and surface_rect.collidepoint(pos):
                    self.mouse_hover(True)
                else:
                    self.mouse_hover(False)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect <> None and surface_rect.collidepoint(pos):
                    self.mouse_press()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect <> None and surface_rect.collidepoint(pos):
                    self.mouse_release()


class SpecialButton(PgxtraWidget):
    ''' Creates a button using an image file. Can accept additional button
        images for hovering, pressing, and disabled. To disable a button, call
        button.disable().

        Attributes:
            image = image of widget (pre-loaded)
            screen_position = top left corner where widget will reside on screen
            btn_size = size of button
            img_pos = top left corner of image segment
            func_call = function that will handle widget event
            offsets = x,y adjustments to img_pos for additional button images
                (any not provided will default to the normal image)

        If widget is enabled, upon left button press, image will use press image
        (if provided in sprite sheet). Upon left button release, image will
        return to normal, and upon hovering, if provided in sprite sheet, will
        use hover image.

        TODO: If images not provided for press and hover, alter image color to
        indicate changes. Also implement toggle switch to turn off this default
        behavior.

        self.enabled = True if the widget is active, default is True
        '''

    def __init__(self, image, screen_position, btn_size, img_pos,
                 func_call, hover_offset=(0,0), press_offset=(0,0),
                 disable_offset=(0,0)):
        PgxtraWidget.__init__(self)
        self.image = image
        self.pos = screen_position
        self.img_pos = img_pos
        self.size = btn_size
        self.func_call = func_call
        self.rect = pygame.Rect(self.img_pos, self.size)
        self.surface_rect = pygame.Rect(self.pos, self.size)
        self.hover = False
        self.pressed = False

        # add widget to master list
        pgutility.add_special_button(self)

        self.hover_image_pos = (self.img_pos[0] + hover_offset[0],
                                self.img_pos[1] + hover_offset[1])
        self.hover_rect = pygame.Rect(self.hover_image_pos, self.size)

        self.press_image_pos = (self.img_pos[0] + press_offset[0],
                                self.img_pos[1] + press_offset[1])
        self.press_rect = pygame.Rect(self.press_image_pos, self.size)

        self.disable_image_pos = (self.img_pos[0] + disable_offset[0],
                                  self.img_pos[1] + disable_offset[1])
        self.disable_rect = pygame.Rect(self.disable_image_pos, self.size)

    def draw(self, screen):
        if not self.enabled:
            screen.blit(self.image, self.pos, self.disable_rect)

        elif self.pressed and self.hover:
            screen.blit(self.image, self.pos, self.press_rect)

        elif self.hover:
            screen.blit(self.image, self.pos, self.hover_rect)

        else:
            screen.blit(self.image, self.pos, self.rect)

    def is_active(self):
        return self.enabled

    def mouse_release(self):
        if self.enabled and self.hover and self.pressed:
            self.func_call()
        spc_buttons = pgutility.get_special_buttons()
        for button in spc_buttons:
            button.pressed = False

    def mouse_press(self):
        if self.enabled:
            self.pressed = True

    def mouse_hover(self, hover):
        if hover:
            self.hover = True
        if not hover:
            self.hover = False

    def get_surface_rect(self):
        return self.surface_rect

    def call(self):
        self.func_call()

    def check_event(self, event):
        if self.is_active():
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect != None and surface_rect.collidepoint(pos):
                    self.mouse_hover(True)
                else:
                    self.mouse_hover(False)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect <> None and surface_rect.collidepoint(pos):
                    self.mouse_press()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect <> None and surface_rect.collidepoint(pos):
                    self.mouse_release()


class InputField(PgxtraWidget):
    ''' Creates an input field on a solid colored rectangular background.
        Attributes:
            label = string of text on widget
            text_color = rgb color value of label text
            bg_color = rgb color value of widget background
            position = top left corner of widget
            fld_size = size of input field
            func_call = function that will handle widget event
            font_size = default set to 40
            len_cap = default set to 0, character cap on label
            focus = sets keyboard focus to this widget, default is False
                (Can only type in an input field with focus, and only one
                input field should have focus at any given time. If 2 or more
                fields have True focus at the same time, any typing will occur
                in both, and any return presses will call both fields'
                function calls. As long as only 1 or fewer fields is set to
                True, the class method check_event will handle updating all
                fields as necessary.)

        Widget label text will be centered and gray on the widget initially.
        If widget is enabled, upon left button press, field will erase and
        focus will become True, if not already. Text color will become value
        passed when initialized. When return is pressed, contents of field are
        passed to function call and focus is removed. Focus can be re-
        established by clicking the field again. To avoid this, call disable()
        on the widget.

        self.enabled = True if the widget is active, default is True
        '''

    def __init__(self, label, text_color, bg_color, position,
                 fld_size, func_call, font_size=40, len_cap=0, focus=False):
        PgxtraWidget.__init__(self)
        self.label = label
        self.default_label = label[:]
        self.text_color = text_color
        self.bg_color = bg_color
        self.pos = position
        self.size = fld_size
        self.func_call = func_call
        self.font_size = font_size
        self.len_cap = len_cap
        self.rect = pygame.Rect(self.pos, self.size)
        self.cursor = '|'
        self.blink_rate = 500
        self.focused = focus

        self.render_text(self.label)

        # add widget to master list
        pgutility.add_input_field(self)

    def render_text(self, rend_text):
        font = pygame.font.Font(None, self.font_size)
        if self.default_label in rend_text:
            text = font.render(rend_text, 1, pygame.Color('gray'))
        else:
            text = font.render(rend_text, 1, self.text_color)
        size = font.size(self.label)
        textpos = ((self.size[0] - size[0]) // 2 + self.pos[0],
                   (self.size[1] - size[1]) // 2 + self.pos[1])
        self.text = text
        self.textpos = textpos

    def draw(self, screen):
        if self.focused:
            time = pygame.time.get_ticks()
            if time % (self.blink_rate * 2) < self.blink_rate:
                self.cursor = " "
            else:
                self.cursor = "|"
        else:
            self.cursor = ""

        text = self.label + self.cursor
        self.render_text(text)
        pygame.draw.rect(screen, self.bg_color, self.rect)
        screen.blit(self.text, self.textpos)

    def is_active(self):
        return self.enabled

    def mouse_release(self):
        if self.enabled and self.pressed:
            self.bg_color, self.text_color = self.text_color, self.bg_color
            self.pressed = False

    def mouse_press(self):
        if self.enabled:
            self.bg_color, self.text_color = self.text_color, self.bg_color
            self.pressed = True
            self.change_label("")

    def mouse_hover(self, hover):
        if hover:
            self.hover = True
        if not hover:
            self.hover = False

    def get_surface_rect(self):
        return self.rect

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

    def set_focus(self):
        self.focused = True

    def remove_focus(self):
        self.focused = False

    def check_event(self, event):
        if self.is_active():
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect != None and surface_rect.collidepoint(pos):
                    self.mouse_hover(True)
                else:
                    self.mouse_hover(False)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect <> None and surface_rect.collidepoint(pos):
                    self.mouse_press()
                    response = ""

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect <> None and surface_rect.collidepoint(pos):
                    self.mouse_release()
                    if self.enable:
                        fields = pgutility.get_input_fields()
                        for field in fields:
                            if field != self:
                                field.remove_focus()
                            else:
                                field.set_focus()

            if self.focused:
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
                        self.remove_focus()
                        #self.disable()

                    if label != response:
                        self.change_label(response)


class PGxtraUtility:
    def __init__(self):
        '''Creates collection of all pgxtra control widgets. To access lists
        from other locations, use pgutility.get_...() methods.'''

        self.widgets = []
        self.buttons = []
        self.input_fields = []
        self.special_buttons = []
        self.exists = True

    def add_button(self, button):
        self.buttons.append(button)
        self.widgets.append(button)

    def add_input_field(self, input_field):
        self.input_fields.append(input_field)
        self.widgets.append(input_field)

    def add_special_button(self, special_button):
        self.special_buttons.append(special_button)
        self.widgets.append(special_button)

    def get_widgets(self):
        return self.widgets

    def get_buttons(self):
        return self.buttons

    def get_input_fields(self):
        return self.input_fields

    def get_special_buttons(self):
        return self.special_buttons


def print_clicked():
    print "Clicked"

def enter_field(obj):
    print obj, "entered"

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
    size = [600, 450]
    global screen
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Example")

    # Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()

    # Create 2 buttons
    btn1 = Button('Play', BLACK, RED, (50, 25), (200, 50), print_clicked)
    btn2 = Button('Load Save Point', WHITE, RED, (50, 125), (200, 50),
                  print_clicked, 24)

    # Create 1 input field
    inp_fld1 = InputField('Enter Name', BLUE, WHITE, (50, 225), (200, 50),
                         enter_field, len_cap = 12, focus=True)

    inp_fld2 = InputField('Enter Color', BLUE, WHITE, (50, 325), (200, 50),
                         enter_field, len_cap = 12)

    response = ""

    # Create 4 special buttons if file is present
    try:
        button_pic = pygame.image.load('prettybuttons.png').convert_alpha()

        spc_btn1 = SpecialButton(button_pic, (300, 25), (226, 75),
                                 (8, 92), print_clicked, hover_offset=(240, 0),
                                 press_offset=(480, 0), disable_offset=(720, 0))

        spc_btn2 = SpecialButton(button_pic, (300, 125), (226, 75),
                                 (8, 428), print_clicked, hover_offset=(240, 0),
                                 press_offset=(480, 0), disable_offset=(720, 0))

        spc_btn3 = SpecialButton(button_pic, (300, 225), (226, 75),
                                 (8, 680), print_clicked, hover_offset=(240, 0),
                                 press_offset=(480, 0), disable_offset=(720, 0))

        spc_btn4 = SpecialButton(button_pic, (300, 325), (226, 75),
                                 (8, 848), print_clicked, hover_offset=(240, 0),
                                 press_offset=(480, 0), disable_offset=(720, 0))

        spc_btn1.disable()

    except:
        print "Unable to test special buttons. File 'prettybuttons.png' missing"



    while not done:
        # Limit fps to 30
        clock.tick(30)

        # Check for applicable events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            else:
                for widg in pgutility.get_widgets():
                    widg.check_event(event)

        # Iterate through all widgets and draw them
        for widg in pgutility.get_widgets():
            widg.draw(screen)

        # Display all drawn items to the screen
        pygame.display.flip()

def main():
    test()

global pgutility
pgutility = PGxtraUtility()

if __name__ == '__main__':
    main()