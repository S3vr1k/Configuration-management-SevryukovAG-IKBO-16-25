import tkinter as tk

from src.config import parse_options
from src.gui import EmulatorWindow


def main():
    """Читает настройки, создаёт окно и планирует стартовый скрипт."""
    options = parse_options()

    root = tk.Tk()
    window = EmulatorWindow(root)

    root.after(0, window.run_startup, options)
    root.mainloop()


if __name__ == "__main__":
    main()