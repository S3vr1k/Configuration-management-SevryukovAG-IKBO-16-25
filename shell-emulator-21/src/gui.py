import getpass
import socket
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from src.startup import run_script
from src.shell import execute_command

class EmulatorWindow:
    """Графический интерфейс эмулятора"""
    def __init__(self, root):
        """Создаёт элементы окна и заголовок из данных ОС"""
        self.root = root

        username = getpass.getuser()
        hostname = socket.gethostname()
        title = f"Эмулятор - [{username}@{hostname}]"
        root.title(title)

        self.history = ScrolledText(
            root,
            width=80,
            height=20,
            state=tk.DISABLED,
        )
        self.history.pack(fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(root)
        self.entry.pack(fill=tk.X)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus_set()

        self.write("Этап 2. Доступные команды: ls, cd, exit.")

    def write(self, text):
        """Добавляет строку в историю"""
        self.history.configure(state=tk.NORMAL)
        self.history.insert(tk.END, text + "\n")
        self.history.configure(state=tk.DISABLED)
        self.history.see(tk.END)

    def on_enter(self, event):
        """Читает ввод, выполняет команду и показывает результат"""
        text = self.entry.get()
        self.entry.delete(0, tk.END)

        if not text.strip():
            return "break"

        self.write(f"> {text}")

        try:
            output, should_exit = execute_command(text)
        except ValueError as error:
            self.write(f"Ошибка: {error}")
            return "break"

        if output:
            self.write(output)

        if should_exit:
            self.root.destroy()

        return "break"
    def run_startup(self, options):
        """Показывает параметры и выполняет стартовый скрипт."""
        self.write(f"Путь к VFS: {options.vfs!r}")
        self.write(f"Стартовый скрипт: {options.script!r}")

        if options.script is None:
            return

        should_exit = run_script(options.script, self.write)

        if should_exit:
            self.root.destroy()