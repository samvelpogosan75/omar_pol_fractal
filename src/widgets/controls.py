"""Панель управления приложением."""
import tkinter as tk
from tkinter import ttk
from collections.abc import Callable


class Controls(ttk.Frame):
    """Элементы управления итерациями и анимацией."""

    def __init__(self, parent: tk.Misc, on_build: Callable[[int], None],
                 on_pause: Callable[[], None], on_reset: Callable[[], None]) -> None:
        super().__init__(parent, padding=8)
        self.iterations = tk.IntVar(value=6)
        ttk.Label(self, text="Итерации:").pack(side="left")
        ttk.Spinbox(self, from_=1, to=8, width=5,
                    textvariable=self.iterations).pack(side="left", padx=5)
        ttk.Button(self, text="Построить",
                   command=lambda: on_build(self.iterations.get())).pack(side="left", padx=4)
        self.pause_button = ttk.Button(self, text="Пауза", command=on_pause)
        self.pause_button.pack(side="left", padx=4)
        ttk.Button(self, text="Сброс масштаба", command=on_reset).pack(side="left", padx=4)

    def set_paused(self, paused: bool) -> None:
        """Изменить подпись кнопки паузы."""
        self.pause_button.configure(text="Продолжить" if paused else "Пауза")
