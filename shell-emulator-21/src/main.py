import tkinter as tk

from src.gui import EmulatorWindow


def main():
    """Создаёт окно и запускает обработку событий"""
    root = tk.Tk()
    window = EmulatorWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()