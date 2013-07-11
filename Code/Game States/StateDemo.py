import pygame,  sys


class State:
    def __init__(self):
        self.title = "The Simplest Game"
        self.width = 640
        self.height = 480
        self.message = ""
        self.location = (20, 150)
        self.font = 40
        self.color = "White"
        self.nextState = None


    def start(self):
        pygame.init()
        self.fpsClock = pygame.time.Clock()


        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.screen = pygame.Surface((self.width, self.height))

        self.main_loop()

    def main_loop(self):
        while True:
            self.screen.fill(pygame.Color(self.color))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   self.quit()
                elif event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_q:
                        self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.transition()

            self.draw()
            self.surface.blit(self.screen, (0,0))
            pygame.display.flip()

            #pygame.display.update()
            self.fpsClock.tick(30)

    def quit(self):
        pygame.quit()
        sys.exit()

    def draw_text(self, text, y_position=36):
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render(text, 1, (10, 10, 10))
            textpos = text.get_rect()
            textpos.centerx = self.screen.get_rect().centerx
            textpos.centery = y_position
            self.screen.blit(text, textpos)


    def draw(self):
        self.draw_text(self.message)
        self.draw_text(self.btn, 72)

    # transition is a base-class method
    def transition(self):
        # derived classes provide their own "nextState". Default is None.
        if self.nextState <> None:
            switch_to = self.nextState()
            switch_to.start()

class StartState(State):
    def __init__(self):
        State.__init__(self)
        self.message = "No buttons in Pygame (yet). Click anywhere to play"
        self.btn = "Click to Play"
        self.nextState = GameState

    # demonstrate overriding my_setup
    def draw(self):
        self.draw_text("Start-specific label", 144)
        # demonstrate calling base-class method
        # demonstrate that each state can augment the gui
        State.draw(self)

class GameState(State):
    def __init__(self):
        State.__init__(self)
        self.message = "No buttons in Pygame (yet). Click anywhere to win"
        self.btn = "Click to Win"
        self.nextState = EndState

    def draw(self):
        # demonstrate that the order in which the base-class method
        # is called can vary from state to state
        State.draw(self)
        self.draw_text("Game-specific label", 144)

class EndState(State):
    def __init__(self):
        State.__init__(self)
        self.message = "Congratulations! You won!"
        self.btn = "No buttons in Pygame (yet)."
        self.message2 = "Click anywhere to Play again"
        self.location = (20, 120)
        self.location2 = (20, 180)
        self.nextState = StartState

    def draw(self):
        State.draw(self)
        self.draw_text(self.message)
        self.draw_text(self.message2, 144)

    # demonstrate that some states need not override my_setup()


new_game = StartState()
new_game.start()
