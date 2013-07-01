import simplegui


class State:
    def __init__(self):
        self.title = "The Simplest Game"
        self.width = 500
        self.height = 300
        self.message = ""
        self.location = (20, 150)
        self.font = 40
        self.color = "White"
        self.nextState = None


    def start(self):
        self.frame = simplegui.create_frame(self.title,
                                       self.width,
                                       self.height)
        self.frame.set_draw_handler(self.draw)
        self.frame.start()
        self.my_setup()

    # allow subclasses to override their gui:
    def my_setup(self):
        self.frame.add_button(self.btn, self.transition)

    def draw(self, canvas):
        canvas.draw_text(self.message, self.location,
                         self.font, self.color)

    # transition is a base-class method
    def transition(self):
        # derived classes provide their own "nextState". Default is None.
        if self.nextState <> None:
            switch_to = self.nextState()
            switch_to.start()

class StartState(State):
    def __init__(self):
        State.__init__(self)
        self.message = "Press the button to play"
        self.btn = "Click to Play"
        self.nextState = GameState

    # demonstrate overriding my_setup
    def my_setup(self):
        self.frame.add_label("Start-specific label")
        # demonstrate calling base-class method
        # demonstrate that each state can augment the gui
        State.my_setup(self)

class GameState(State):
    def __init__(self):
        State.__init__(self)
        self.message = "Click the button to win"
        self.btn = "Click to Win"
        self.nextState = EndState

    def my_setup(self):
        # demonstrate that the order in which the base-class method
        # is called can vary from state to state
        State.my_setup(self)
        self.frame.add_label("Game-specific label")

class EndState(State):
    def __init__(self):
        State.__init__(self)
        self.message = "Congratulations! You won!"
        self.btn = "Play again"
        self.message2 = "Would you like to play again?"
        self.location = (20, 120)
        self.location2 = (20, 180)
        self.nextState = StartState

    def draw(self, canvas):
        canvas.draw_text(self.message, self.location,
                         self.font, self.color)
        canvas.draw_text(self.message2, self.location2,
                         self.font, self.color)

    # demonstrate that some states need not override my_setup()


new_game = StartState()
new_game.start()
