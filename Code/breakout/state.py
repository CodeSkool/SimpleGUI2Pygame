from ui import UI


class State:

    def __init__(self):
        """Create a reference to the UI, and establish the default nextState."""
        self.ui = UI(self)
        self.nextState = None

    def start(self):
        """Start the UI"""
        self.ui.start()
        self.ui = None

    def quit(self):
        """Perform any cleanup before exiting the current state."""
        pass

    def setup(self, screen):
        """Hook: Create objects that know how to draw themselves."""
        pass

    def update(self, screen):
        """Hook: Draw things on the screen that change with every draw loop
        (animations)."""
        pass

    def handle(self, event):
        """Hook: Handle event."""
        pass

    def get_next_state(self):
        """Return the state to which to transition."""
        return self.nextState

    def transition(self):
        """Transition to the next state."""
        self.quit()
        next_state = self.get_next_state()
        self.ui.transition()

def main():
    do_quit = False
    try:
        s = State()
        s.start()
        s.transition()
    except Exception as e:
        do_quit = True
        print e
    finally:
        if do_quit:
            s.ui.quit()


if __name__ == '__main__':
    main()
