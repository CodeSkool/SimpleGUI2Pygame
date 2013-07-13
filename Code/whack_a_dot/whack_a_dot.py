# whack-a-dot

# Game starts with a logo "Whack-A-Dot", prompt "Click to begin".
#   After 10 seconds, display the high scores.
#   After 20 seconds return to the logo.
# User clicks. Player starts with 3 lives
# Game counts down: 3, 2, 1... GO!
# Several circles displayed
# A dot appears in one of the circles (chosen randomly)
# DO: A timer counts down from 5 seconds (in tenths of a second)
#   Either: If the player clicks on the dot, the timer stops. The remaining time
#           (x100) is added to the score.
#   OR: If the player does not click on the dot before the timer stops, they
#           lose one life, the game counts down from 3 again.
# LOOP until no more lives
# Display the final score, record the user's initials if they got a high score.
# Display the logo / high-score list loop

from utilities_1 import state, pgxtra, filehelper, ui
import pygame, pygame.event, pygame.time
import random, itertools, functools

class TimerEvents:
    base_event = 1
    ScreenSaver = pygame.USEREVENT + base_event + 1
    GameStart = pygame.USEREVENT + base_event + 2
    Playing = pygame.USEREVENT + base_event + 3
    GameOver = pygame.USEREVENT + base_event + 4
    def start(self, eventid, milliseconds=1000):
        pygame.time.set_timer(eventid, int(milliseconds))
    def stop(self, eventid):
        pygame.time.set_timer(eventid, 0)

class HighScores:
    high_scores = None
    def __init__(self):
        self.high_scores_file = "high_scores.pkl"
    def load(self):
        HighScores.high_scores = filehelper.FileHelper(self.high_scores_file).load()
        if HighScores.high_scores == None:
            keys = [i + 1 for i in range(10)]
            values = [("ACE", 100 * (i+1)) for i in range(10, 0, -1)]
            HighScores.high_scores = dict(itertools.izip(keys, values))
    def save(self):
        filehelper.FileHelper(self.high_scores_file).save(HighScores.high_scores)

# screen_saver
    # Game starts with a logo "Whack-A-Dot", prompt "Click to begin".
    #   After 10 seconds, display the high scores.
    #   After 20 seconds return to the logo.
    # User click >>> game_start
class ScreenSaver(state.State):
    def __init__(self, current=0):
        state.State.__init__(self)
        self.nextState = GameStart
        logo_duration = 5 * 1000
        scores_duration = 5 * 1000
        self.displays = [(logo_duration, self.draw_logo),
                        (scores_duration, self.draw_high_scores)]
        self.eventid = TimerEvents.ScreenSaver
        self.current = current
        self.draw = self.displays[self.current][1]

    def start(self):
        TimerEvents().start(eventid=self.eventid,
                            milliseconds=self.displays[self.current][0])
        state.State.start(self)

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            TimerEvents().stop(self.eventid)
            self.transition()
        elif event.type == self.eventid:
            self.increment_display()
            self.draw = self.displays[self.current][1]
            TimerEvents().start(eventid=self.eventid,
                                milliseconds=self.displays[self.current][0])
    def increment_display(self):
        self.current += 1
        if self.current >= len(self.displays):
            self.current = 0

    def update(self, screen):
        self.draw(screen)

    def draw_high_scores(self, screen):
        scores = HighScores.high_scores
        caption = "High Scores"
        with self.ui.newcontext(ui.UIContext(font_size=40)):
            self.ui.draw_text(screen, caption, location=(screen.get_width() / 2, screen.get_height() / 11), align=0)
        spacing = 40
        dots = "".join([" ." for i in range(spacing)])
        for key, (name, score) in sorted(scores.items()):
            txt = "".join([name, dots, str(score)])
            self.ui.draw_text(screen, txt, location=(screen.get_width() / 2, (key + 1) * screen.get_height() / 12), align=0)

    def draw_logo(self, screen):
        logo = "Whack-a-Dot"
        prompt = "Click to begin"
        with self.ui.newcontext(ui.UIContext(font_size=60, location=(screen.get_width() / 2, screen.get_height() / 3), align=0)):
            self.ui.draw_text(screen, logo)
        with self.ui.newcontext(ui.UIContext(font_size=40, location=(screen.get_width() / 2, screen.get_height() / 2), align=0)):
            self.ui.draw_text(screen, prompt)

# game_start
    # Player starts with 3 lives
    # Prompt: Click when ready
    # Game counts down: 3, 2, 1... GO!
    # >>> playing
class GameStart(state.State):
    def __init__(self, lives=3, score=0):
        state.State.__init__(self)
        self.lives = lives
        self.score = score
        self.nextState = lambda: Playing(self.lives, self.score)
        self.prompt = "Ready?"
        self.countdown_step = 500
        self.count = 3
        self.text = self.prompt
        self.eventid = TimerEvents.GameStart

    def start(self):
        self.start_timer()
        state.State.start(self)

    def handle(self, event):
        if event.type == self.eventid:
            self.text = str(self.count)
            if self.count == 0:
                self.text = "GO!"
            elif self.count < 0:
                self.stop_timer()
            self.count -= 1

    def start_timer(self):
        TimerEvents().start(eventid=self.eventid,
                            milliseconds=self.countdown_step)
    def stop_timer(self):
        TimerEvents().stop(eventid=self.eventid)
        self.transition()

    def update(self, screen):
        with self.ui.newcontext(ui.UIContext(font_size=80)):
            self.ui.draw_text(screen, self.text, location=(screen.get_width() / 2, screen.get_height() / 2), align=0)
        lives = "Lives: " + str(self.lives)
        score = "Score: " + str(self.score)
        with self.ui.newcontext(ui.UIContext(font_size=40)):
            self.ui.draw_text(screen, lives, location=(10, screen.get_height() / 10), align=-1)
            self.ui.draw_text(screen, score, location=(screen.get_width(), screen.get_height() / 10), align=1)


# playing
    # Several circles displayed
    # A dot appears in one of the circles (chosen randomly)
    # DO: A timer counts down from 5 seconds (in tenths of a second)
    #   Either: If the player clicks on the dot, the timer stops.
    #           The remaining time (x100) is added to the score.
    #               >>> playing
    #   OR: If the player does not click on the dot before the timer stops, they lose one life, the game counts down from 3 again.
    #               >>> game_start
    # LOOP until no more lives
    # >>> GameOver
class Playing(state.State):
    def __init__(self, lives=3, score=0, misses=0):
        state.State.__init__(self)
        self.nextState = None
        self.eventid = TimerEvents.Playing
        self.score = score
        self.lives = lives
        self.misses = misses
        self.countdown = 1.0 * 1000
        self.circle_count = 5
        self.misses_per_life = 3
        self.start_time = pygame.time.get_ticks()

    def start(self):
        self.start_time = pygame.time.get_ticks()
        TimerEvents().start(eventid=self.eventid, milliseconds=self.countdown)
        state.State.start(self)

    def handle(self, event):
        if event.type == self.eventid:
            if self.misses >= self.misses_per_life:
                if self.lives > 1:
                    self.nextState = lambda: GameStart(
                                        lives=self.lives-1, score=self.score)
                else:
                    self.nextState = lambda: GameOver(score=self.score)
            else:
                self.nextState = lambda: Playing(lives=self.lives,
                                    score=self.score - 50,
                                    misses=self.misses + 1)
            self.transition()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.dot[3] <> None and self.dot[3].collidepoint(event.pos):
                self.nextState = lambda: Playing(lives=self.lives,
                                misses = self.misses,
                                score=self.score + int(self.get_time() * 100))
                self.transition()

    def setup(self, screen):
        self.circles = []
        dot = random.randrange(self.circle_count)
        for i in range(self.circle_count):
            (pos, radius, width, rect) = (((i + 1) * screen.get_width() / (self.circle_count + 1), screen.get_width() / 2),
                                            20, 1, None)
            if i == dot:
                self.dot = [pos, int(radius * 0.8), 0, rect]
            self.circles.append([pos, radius, width, rect])

    def get_time(self):
        return round(float(self.countdown - (pygame.time.get_ticks() - self.start_time)) / 1000, 1)

    def update(self, screen):
        # draw stats
        time = str(self.get_time())
        lives = "Lives: " + str(self.lives)
        misses = "Misses: " + str(self.misses) + " of " + str(self.misses_per_life)
        score = "Score: " + str(self.score)
        with self.ui.newcontext(ui.UIContext(font_size=40)):
            self.ui.draw_text(screen, lives, location=(10, screen.get_height() / 10), align=-1)
            self.ui.draw_text(screen, misses, location=(10, 2 * screen.get_height() / 10), align=-1)
            self.ui.draw_text(screen, score, location=(screen.get_width(), screen.get_height() / 10), align=1)
            self.ui.draw_text(screen, time, location=(screen.get_width(), 2 * screen.get_height() / 10), align=1)
        # draw cirles
        [pos, radius, width, rect] = self.dot
        screen.lock()
        try:
            self.dot[3] = self.ui.draw_circle(screen, location=pos, radius=radius)
            for circle in self.circles:
                [pos, radius, width, rect] = circle
                with self.ui.newcontext(ui.UIContext(line_width = circle[2])):
                    self.ui.draw_circle(screen, location=pos, radius=radius)
        finally:
            screen.unlock()



# game_over
    # Display the final score, record the user's initials if they got a high score.
    # >>> screen_saver
class GameOver(state.State):
    def __init__(self, score):
        state.State.__init__(self)
        self.nextState = lambda: ScreenSaver(current=1)
        self.eventid = TimerEvents.GameOver
        self.score = score
        self.countdown = 5 * 1000
        for key, (name, value) in sorted(HighScores.high_scores.items()):
            if score > value:
                self.replace = key
                break
        else:
            self.replace = None

    def start(self):
        if self.replace == None:
            TimerEvents().start(self.eventid, self.countdown)
        state.State.start(self)

    def handle(self, event):
        if event.type == self.eventid:
            self.transition()

    def transition(self):
        TimerEvents().stop(self.eventid)
        state.State.transition(self)

    def input_text(self, text):
        new_scores = {}
        text = text.upper()
        old_scores = sorted(HighScores.high_scores.keys())
        index = old_scores.index(self.replace)
        for key in old_scores[:index]:
            new_scores[key] = HighScores.high_scores[key]
        new_scores[self.replace] = (text, self.score)
        for index in xrange(index + 1, len(HighScores.high_scores)):
            new_scores[old_scores[index]] = HighScores.high_scores[old_scores[index - 1]]
        HighScores.high_scores = new_scores
        high_scores.save()
        self.transition()

    def setup(self, screen):
        if self.replace == None:
            pass
        else:
            size = (75, 50)
            location = ((screen.get_width() / 2) - (size[0] / 2),
                        6 * screen.get_height() / 10)
            with self.ui.newcontext(ui.UIContext(font_size=30, len_cap=3)):
                self.ui.add_input(screen, "___",
                                  lambda text: self.input_text(text),
                                  location=location, size=size)

    def update(self, screen):
        if self.replace == None:
            with self.ui.newcontext(ui.UIContext(font_size=40)):
                self.ui.draw_text(screen, "Game Over", location=(screen.get_width() / 2, screen.get_height() / 10), align=0)
                self.ui.draw_text(screen, "Your Score: " + str(self.score), location=(screen.get_width() / 2, 3 * screen.get_height() / 10), align=0)
        else:
            with self.ui.newcontext(ui.UIContext(font_size=40)):
                self.ui.draw_text(screen, "Game Over", location=(screen.get_width() / 2, screen.get_height() / 10), align=0)
                self.ui.draw_text(screen, "New High Score!", location=(screen.get_width() / 2, 3 * screen.get_height() / 10), align=0)
                self.ui.draw_text(screen, "Your Score: " + str(self.score), location=(screen.get_width() / 2, 4 * screen.get_height() / 10), align=0)
                self.ui.draw_text(screen, "Enter your initials:", location=(screen.get_width() / 2, 5 * screen.get_height() / 10), align=0)



class Game:
    def __init__(self):
        global high_scores
        high_scores = HighScores()
        high_scores.load()

    def start(self, init_state):
        current_state = init_state()
        while current_state <> None:
            current_state.start()
            current_state = current_state.get_next_state()()


def main():
    Game().start(ScreenSaver)
    #ScreenSaver().start()
    #Playing().start()
    #GameOver(0).start()




if __name__ == '__main__':
    main()

