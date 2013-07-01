# 20 Questions - Pygame version

import pygame
import os, sys, pickle
import pgxtra

#The default question tree
question_tree = ["human", None]
#The location of the question tree file
question_file = "questions.txt"

class FileHelper:
    def open_file(self, file_name, mode):
        """Tries to open a file in the specified mode.
        If the file does not exist, opens it in a+ mode"""
        try:
            the_file = open(file_name, mode)
        except IOError:
            the_file = open(file_name, "a+")
        return the_file

    def save_questions(self):
        """Save the question tree to a file"""
        file = open(question_file, "w")
        pickle.dump(question_tree, file)
        file.close()

    def load_questions(self):
        """Load the question tree from a file if it exists"""
        global question_tree
        file = self.open_file(question_file, "r")
        if file.read(1) <> '':
           file.close()
           file = open(question_file, "r")
           question_tree = pickle.load(file)
        #print question_tree
        file.close()

class UI:
    def __init__(self, target, title="", width=640,
                 height=480, font=20,
                 bg_color="black",
                 fg_color="white"):
        self.target = target
        self.title = title
        self.width = width
        self.height = height
        self.font = font
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.buttons = []
        self.textinputs = []

        pygame.init()
        self.clock = self.fpsClock = pygame.time.Clock()

        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.screen = pygame.Surface((self.width, self.height))

    def start(self):
        self.target.my_setup(self.screen)
        self.surface.blit(self.screen, (0,0))

        while True:
            self.screen.fill(pygame.Color(self.bg_color))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   self.quit()
                else:
                    for field in self.textinputs:
                        field.check_event(event)
                    for button in self.buttons:
                        button.check_event(event)

            for field in self.textinputs:
                field.draw()
            for button in self.buttons:
                button.draw()

            self.target.draw(self.screen)
            self.surface.blit(self.screen, (0,0))

            pygame.display.flip()

            #pygame.display.update()
            self.fpsClock.tick(30)

    def quit(self):
        self.target.quit()
        pygame.quit()
        sys.exit()

    def draw_text(self, screen, text, location):
        if pygame.font:
            font = pygame.font.Font(None, self.font)
            text = font.render(text, 1, pygame.Color(self.fg_color))
            textpos = text.get_rect()
            textpos.centerx = location[0]
            textpos.centery = location[1]
            screen.blit(text, textpos)

    def add_input(self, screen, text, handler, location=None, size=None):
        if location == None:
            location = (50, 50)
        if size == None:
            size = (200, 50)
        textinput = pgxtra.InputField(screen, text, self.bg_color, self.fg_color, location, size, handler, self.font)
        textinput.enabled = True
        textinput.draw()
        self.textinputs.append(textinput)

    def add_label(self, screen, text, location=None):
        self.draw_text(screen, text, location)

    def add_button(self, screen, text, handler, location=None, size=None):
        if location == None:
            location = (50, 50)
        if size == None:
            size = (50, 50)
        button = pgxtra.Button(screen, text, self.bg_color, self.fg_color, location, size, handler, self.font)
        button.enabled = True
        button.draw()
        self.buttons.append(button)

class State:
    def __init__(self):
        self.ui = UI(self, "20 Questions")
        self.nextState = None

    def start(self):
        self.ui.start()

    def quit(self):
        pass

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

class GameStart(State):
    def __init__(self):
        State.__init__(self)
        self.nextState = lambda: Playing(question_tree)
        self.next_state_type = None
        self.message = "Load previous question tree?"

    def yes(self):
        FileHelper().load_questions()
        self.transition()

    def no(self):
        self.transition()

    def my_setup(self, frame):
        self.ui.add_button(frame, "Yes", lambda btn: self.yes(),
                           (50, self.ui.font * 2.5))
        self.ui.add_button(frame, "No", lambda btn: self.no(),
                           (110, self.ui.font * 2.5))
    def draw(self, canvas):
        self.ui.draw_text(canvas,
                          self.message,
                          (150, self.ui.font))


class Playing(State):
    def __init__(self, tree):
        State.__init__(self)
        self.next_state = self.get_next_state
        self.next_state_type = None
        self.tree = tree

    def yes(self):
        self.next_state_type = lambda: GameOver("I win!")
        if self.tree[1] <> None:
            self.next_state_type = lambda: Playing(self.tree[1][True])
        self.transition()

    def no(self):
        self.next_state_type = lambda: Learning(self.tree, 0)
        if self.tree[1] <> None:
            self.next_state_type = lambda: Playing(self.tree[1][False])
        self.transition()

    def my_setup(self, frame):
        self.ui.add_button(frame, "Yes", lambda btn: self.yes(),
                           (50, self.ui.font * 2.5))
        self.ui.add_button(frame, "No", lambda btn: self.no(),
                           (110, self.ui.font * 2.5))

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
            self.nextState = lambda: GameOver("You win!")
        self.transition()

    def build_tree(self):
        new_name = self.answers[0]
        descriptor = self.answers[1]
        false_branch = self.tree[0]
        self.tree[0] = descriptor
        self.tree[1] = {True:[new_name, None]}
        self.tree[1][False] = [false_branch, None]
        FileHelper().save_questions()

    def input_text(self, text):
        self.answers.append(text)
        self.learn_next()

    def my_setup(self, frame):
        left = 200
        top = self.ui.font
        width = 200
        height = 50
        self.ui.add_input(frame,
                          Learning.messages[self.index],
                          lambda text: self.input_text(text),
                          (left, top * 2.5),
                          (400, 50),
                          )

    def draw(self, canvas):
        left = 300
        top = self.ui.font
        width = 200
        height = 50
        self.ui.draw_text(canvas,
                          Learning.messages[self.index],
                          location=(left, top))
        self.ui.add_label(canvas,
                          "(Remember to press enter after typing your answer)",
                          location=(left, top * 6))

class GameOver(State):
    def __init__(self, message):
        State.__init__(self)
        self.nextState = lambda: Playing(question_tree)
        self.next_state_type = None
        self.message = message

    def yes(self):
        self.transition()

    def no(self):
        self.ui.quit()

    def my_setup(self, frame):
        self.ui.add_button(frame, "Yes", lambda btn: self.yes(),
                           (50, self.ui.font * 3.5))
        self.ui.add_button(frame, "No", lambda btn: self.no(),
                           (110, self.ui.font * 3.5))


    def draw(self, canvas):
        self.ui.draw_text(canvas,
                          self.message,
                          (50, self.ui.font))
        self.ui.draw_text(canvas,
                          "Play again?",
                          (50, self.ui.font * 2.5))

question_tree = ["human", None]
new_game = GameStart()
new_game.start()
