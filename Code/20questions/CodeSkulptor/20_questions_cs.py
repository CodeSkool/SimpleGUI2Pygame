# 20 Questions - CodeSkulptor version
# http://www.codeskulptor.org/#user17_i8HWa3wyVE2X48y_5.py

import simplegui

class UI:
    def __init__(self, title="", width=640,
                 height=480, font=20,
                 bg_color="black",
                 fg_color="white"):
        self.title = title
        self.width = width
        self.height = height
        self.font = font
        self.bg_color = bg_color
        self.fg_color = fg_color

    def get_frame(self):
        frame = simplegui.create_frame(
                                            self.title,
                                            self.width,
                                            self.height)
        frame.set_canvas_background(self.bg_color)
        return frame

    def draw_text(self, canvas, text, location):
        canvas.draw_text(text, location, self.font, self.fg_color)

    def add_input(self, frame, text, handler, location=None):
        frame.add_input(text, handler, 150)

    def add_label(self, frame, text, location=None):
        frame.add_label(text)

    def add_button(self, frame, text, handler, location=None):
        frame.add_button(text, handler)

class State:
    def __init__(self):
        self.ui = UI("20 Questions")
        self.nextState = None

    def start(self):
        frame = self.ui.get_frame()
        frame.set_draw_handler(self.draw)
        frame.start()
        self.my_setup(frame)

    def my_setup(self, frame):
        pass

    def draw(self, canvas):
        pass

    def get_next_state(self):
        return self.nextState

    def transition(self):
        next_state = self.get_next_state()
        if next_state <> None:
            switch_to = next_state()
            switch_to.start()

class Playing(State):
    def __init__(self, tree):
        State.__init__(self)
        self.next_state = self.get_next_state
        self.next_state_type = None
        self.tree = tree

    def yes(self):
        self.next_state_type = GameOver.i_win
        if self.tree[1] <> None:
            self.next_state_type = lambda: Playing(self.tree[1][True])
        self.transition()

    def no(self):
        self.next_state_type = lambda: Learning.learn_name(self.tree)
        if self.tree[1] <> None:
            self.next_state_type = lambda: Playing(self.tree[1][False])
        self.transition()

    def my_setup(self, frame):
        self.ui.add_button(frame, "Yes", lambda: self.yes(),
                           (50, self.ui.font * 2.5))
        self.ui.add_button(frame, "No", lambda: self.no(),
                           (100, self.ui.font * 2.5))

    def draw(self, canvas):
        self.ui.draw_text(canvas, self.get_question(),
                          (50, self.ui.font))

    def get_question(self):
        return "Is it " + self.tree[0] + "?"

    def get_next_state(self):
        return self.next_state_type

class Learning(State):
    NAME_TEXT = "What is the name of the new animal?"
    DESCRIPTION_TEXT = "Enter an adjective that descibes the animal"

    messages = [NAME_TEXT,
                DESCRIPTION_TEXT]
    learn_name = lambda tree: Learning(tree, 0)

    def __init__(self, tree, index, answers=None):
        State.__init__(self)
        self.tree = tree
        self.index = index
        if answers == None:
            answers = []
        self.answers = answers

    def learn_next(self):
        if self.index < len(Learning.messages) - 1:
            self.nextState = lambda: Learning(self.tree, self.index + 1, self.answers)
        else:
            self.build_tree()
            self.nextState = GameOver.you_win
        self.transition()

    def build_tree(self):
        new_name = self.answers[0]
        descriptor = self.answers[1]
        false_branch = self.tree[0]
        self.tree[0] = descriptor
        self.tree[1] = {True:[new_name, None]}
        self.tree[1][False] = [false_branch, None]

    def input_text(self, text):
        self.answers.append(text)
        self.learn_next()

    def my_setup(self, frame):
        self.ui.add_input(frame,
                          Learning.messages[self.index],
                          lambda text: self.input_text(text),
                          (50, self.ui.font * 2.5))
        self.ui.add_label(frame,
                          "(Remember to press enter after typing your answer)",
                          (50, self.ui.font * 4))

    def draw(self, canvas):
        self.ui.draw_text(canvas,
                          Learning.messages[self.index],
                          (50, self.ui.font))

class GameOver(State):
    i_win = lambda: GameOver("I win!")
    you_win = lambda: GameOver("You win!")

    def __init__(self, message):
        State.__init__(self)
        self.nextState = lambda: Playing(question_tree)
        self.next_state_type = None
        self.message = message

    def play_again(self):
        self.transition()

    def my_setup(self, frame):
        self.ui.add_button(frame,
                           "Play Again",
                           lambda: self.play_again(),
                           (50, self.ui.font * 4))

    def draw(self, canvas):
        self.ui.draw_text(canvas,
                          self.message,
                          (50, self.ui.font))
        self.ui.draw_text(canvas,
                          "Play again?",
                          (50, self.ui.font * 2.5))

question_tree = ["human", None]
new_game = Playing(question_tree)
new_game.start()
