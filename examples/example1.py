from zevents import Event
from zevents.dispatch import listener, Listener

# We create events by subsclassing the zevents.Event class
class TickEvent(Event):
    pass

class QuitEvent(Event):
    pass

# For a class to be able to listen at zevents, decorate it as listener
@listener
class KeyboardController:
    """Controller responsible to handle keyboard events."""

    # Available actions
    actions = {
        "quit": QuitEvent.send,
    }

    @TickEvent.listen
    def _on_tick(self, event):
        """Handles the Tick events."""
        user = input("Say something or enter quit: ")
        action = self.actions.get(
            user.lower().strip(), lambda: print(user)
        )
        action()


# For a class to be able to listen at zevents, you can also subclass Listener
class EchoApplication(Listener):
    """Represents the application itself."""

    def __init__(self):
        super().__init__()
        self.running = False
        self.controller = KeyboardController()

    @QuitEvent.listen
    def _on_quit(self, event):
        """Handles Quit events."""
        self.running = False

    def run(self):
        """Starts the application event loop."""
        self.running = True
        while self.running:
            # We send a Tick event in each loop
            TickEvent.send()

if __name__ == "__main__":
    app = EchoApplication()
    app.run()

