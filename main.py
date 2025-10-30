from controllers.controller import Controller
import warnings

def main():
    """
    Entry point for the CLI Portfolio Tracker.
    Initializes MVC components and runs the command loop.
    """
    warnings.filterwarnings("ignore", category=FutureWarning)

    controller = Controller()
    print("a.s.r. Portfolio Tracker")
    print("View the README for instructions. C^ (CTRL + C) at any point to quit.")

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