from controllers.controller import Controller
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

def main():
    """
    Entry point for the CLI Portfolio Tracker.
    Initializes MVC components and runs the command loop.
    """
    controller = Controller()

    print("a.s.r. Portfolio Tracker")
    print("Type 'exit' to quit., view the README for instructions.")

    while True:
        try:
            command = input("\nProvide a Command (ADD/DELETE/SHOW/GRAPH): ")
            if not command:
                continue
            if command.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            controller.handle_command(command)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()