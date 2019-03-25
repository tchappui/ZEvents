from zevents.events import TickEvent, QuitEvent
from zevents.dispatch import listener

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

@listener
class EchoApplication:
    """Represents the application itself."""

    def __init__(self):
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
