"""Главное окно приложения."""
import tkinter as tk
from tkinter import messagebox
from src.models.fractal_model import FractalModel
from src.renderers.fractal_renderer import FractalRenderer
from src.widgets.controls import Controls


class OmarPolApp:
    """Связывает модель, renderer, управление и автоматический зум."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Фрактал Омара Пола — Погосян Самвел Арутюнович")
        self.root.geometry("900x720")
        self.model = FractalModel(iterations=6)
        self.canvas = tk.Canvas(self.root, background="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.renderer = FractalRenderer(self.canvas)
        self.controls = Controls(self.root, self.build, self.toggle_pause, self.reset_zoom)
        self.controls.pack(fill="x")
        self.segments = self.model.generate()
        self.zoom = 1.0
        self.zoom_direction = 1
        self.paused = False
        self.canvas.bind("<Configure>", lambda _event: self.redraw())
        self.root.after(40, self.animate_zoom)

    def build(self, iterations: int) -> None:
        """Перестроить фрактал с новой глубиной."""
        try:
            self.model.set_iterations(int(iterations))
        except (ValueError, TypeError) as exc:
            messagebox.showerror("Ошибка", str(exc))
            return
        self.segments = self.model.generate()
        self.zoom = 1.0
        self.redraw()

    def toggle_pause(self) -> None:
        """Поставить автоматический зум на паузу или продолжить."""
        self.paused = not self.paused
        self.controls.set_paused(self.paused)

    def reset_zoom(self) -> None:
        """Вернуть исходный масштаб."""
        self.zoom = 1.0
        self.zoom_direction = 1
        self.redraw()

    def animate_zoom(self) -> None:
        """Плавно менять масштаб без блокировки GUI."""
        if not self.paused:
            self.zoom += 0.004 * self.zoom_direction
            if self.zoom >= 1.55:
                self.zoom = 1.55
                self.zoom_direction = -1
            elif self.zoom <= 0.80:
                self.zoom = 0.80
                self.zoom_direction = 1
            self.redraw()
        self.root.after(40, self.animate_zoom)

    def redraw(self) -> None:
        """Перерисовать текущий набор сегментов."""
        self.renderer.draw(self.segments, self.zoom)

    def run(self) -> None:
        """Запустить цикл обработки событий tkinter."""
        self.root.mainloop()
