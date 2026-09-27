
Enter file contents here
"""Command-line interface for gurdung.

Usage::

    gurdung note add "text"      add a note
    gurdung note list            list all notes
    gurdung note rm <id>         remove a note by id
    gurdung todo add "text"      add a todo
    gurdung todo list            list all todos
    gurdung todo done <id>       mark a todo as done
    gurdung todo rm <id>         remove a todo by id
    gurdung todo clear           clear all todos
    gurdung stats                show statistics
"""

import sys

from .storage import Storage

# Simple ANSI colors (safe to disable on non-TTY via --no-color)
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RED = "\033[31m"
CYAN = "\033[36m"


class Colors:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def paint(self, code: str, text: str) -> str:
        if not self.enabled:
            return text
        return f"{code}{text}{RESET}"

    def bold(self, text: str) -> str:
        return self.paint(BOLD, text)

    def green(self, text: str) -> str:
        return self.paint(GREEN, text)

    def yellow(self, text: str) -> str:
        return self.paint(YELLOW, text)

    def blue(self, text: str) -> str:
        return self.paint(BLUE, text)

    def red(self, text: str) -> str:
        return self.paint(RED, text)

    def cyan(self, text: str) -> str:
        return self.paint(CYAN, text)


def _print_notes(notes: list, colors: Colors) -> None:
    if not notes:
        print(colors.yellow("(no notes yet - try: gurdung note add \"your idea\")"))
        return
    for note in notes:
        print(f"{colors.blue(str(note['id'])):>4}. {note['text']}  {colors.cyan('· ' + note['created_at'])}")


def _print_todos(todos: list, colors: Colors) -> None:
    if not todos:
        print(colors.yellow("(no todos yet - try: gurdung todo add \"something to do\")"))
        return
    for todo in todos:
        status = colors.green("✔") if todo["done"] else colors.yellow("◌")
        text = todo["text"]
        print(f"{colors.blue(str(todo['id'])):>4}. {status} {text}")


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    colors = Colors(enabled=sys.stdout.isatty())
    if "--no-color" in argv:
        colors = Colors(enabled=False)
        argv.remove("--no-color")

    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__.strip())
        return 0

    if argv[0] in ("-v", "--version", "version"):
        from . import __version__

        print(f"gurdung {__version__}")
        return 0

    command, args = argv[0], argv[1:]
    storage = Storage()

    # ---- notes ----
    if command == "note":
        if not args:
            _print_notes(storage.list_notes(), colors)
            return 0
        action = args[0]
        rest = args[1:]
        if action == "add":
            if not rest:
                print(colors.red("error: missing note text - try: gurdung note add \"text\""))
                return 1
            note = storage.add_note(" ".join(rest))
            print(colors.green(f"note #{note['id']} saved"))
            return 0
        if action == "list":
            _print_notes(storage.list_notes(), colors)
            return 0
        if action == "rm":
            if not rest:
                print(colors.red("error: missing note id - try: gurdung note rm <id>"))
                return 1
            try:
                note_id = int(rest[0])
            except ValueError:
                print(colors.red("error: note id must be a number"))
                return 1
            if storage.remove_note(note_id):
                print(colors.green(f"note #{note_id} removed"))
            else:
                print(colors.red(f"note #{note_id} not found"))
                return 1
            return 0
        print(colors.red(f"error: unknown note action '{action}'"))
        return 1

    # ---- todos ----
    if command == "todo":
        if not args:
            _print_todos(storage.list_todos(), colors)
            return 0
        action = args[0]
        rest = args[1:]
        if action == "add":
            if not rest:
                print(colors.red("error: missing todo text - try: gurdung todo add \"text\""))
                return 1
            todo = storage.add_todo(" ".join(rest))
            print(colors.green(f"todo #{todo['id']} added"))
            return 0
        if action == "list":
            _print_todos(storage.list_todos(), colors)
            return 0
        if action == "done":
            if not rest:
                print(colors.red("error: missing todo id - try: gurdung todo done <id>"))
                return 1
            try:
                todo_id = int(rest[0])
            except ValueError:
                print(colors.red("error: todo id must be a number"))
                return 1
            if storage.mark_done(todo_id):
                print(colors.green(f"todo #{todo_id} marked done"))
            else:
                print(colors.red(f"todo #{todo_id} not found"))
                return 1
            return 0
        if action == "rm":
            if not rest:
                print(colors.red("error: missing todo id - try: gurdung todo rm <id>"))
                return 1
            try:
                todo_id = int(rest[0])
            except ValueError:
                print(colors.red("error: todo id must be a number"))
                return 1
            if storage.remove_todo(todo_id):
                print(colors.green(f"todo #{todo_id} removed"))
            else:
                print(colors.red(f"todo #{todo_id} not found"))
                return 1
            return 0
        if action == "clear":
            count = storage.clear_todos()
            print(colors.green(f"cleared {count} todo(s)"))
            return 0
        print(colors.red(f"error: unknown todo action '{action}'"))
        return 1

    # ---- stats ----
    if command == "stats":
        s = storage.stats()
        print(colors.bold("gurdung stats"))
        print(f"  notes:   {s['notes']}")
        print(f"  todos:   {s['todos_done']}/{s['todos_total']} done")
        return 0

    print(colors.red(f"error: unknown command '{command}' - use 'gurdung --help'"))
    return 1


if __name__ == "__main__":
    sys.exit(main())
