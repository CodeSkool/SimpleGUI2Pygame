import pygame
from pgxtra_widget import PgxtraWidget


class SpecialButton(PgxtraWidget):
    ''' Creates a button using an image file. Can accept additional button
        images for hovering, pressing, and disabled. To disable a button, call
        button.disable().

        Attributes:
            image = image of widget (pre-loaded)
            screen_position = top left corner position of widget
            btn_size = size of button
            img_pos = top left corner of image segment
            func_call = function that will handle widget event
            offsets = x,y adjustments to img_pos for additional button images
                (any not provided will default to the normal image)

        If widget is enabled, on left button press, image will use press image
        (if provided in sprite sheet). Upon left button release, image will
        return to normal, and upon hovering, if provided in sprite sheet, will
        use hover image.

        TODO: If images not provided for press and hover, alter image color to
        indicate changes. Also implement toggle switch to turn off this default
        behavior.

        self.enabled = True if the widget is active, default is True
        '''

    def __init__(self, image, screen_position, btn_size, img_pos,
                 func_call, hover_offset=(0, 0), press_offset=(0, 0),
                 disable_offset=(0, 0)):
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
        spc_buttons = self.pgutility().get_widgets(SpecialButton)
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
                if surface_rect != None and surface_rect.collidepoint(pos):
                    self.mouse_press()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                surface_rect = self.get_surface_rect()
                if surface_rect != None and surface_rect.collidepoint(pos):
                    self.mouse_release()


def main():
    ## Basic tests
    pygame.init()
    w = SpecialButton(None, (0, 0), (10, 10), (0, 0), lambda: None)
    print w

if __name__ == '__main__':
    main()
