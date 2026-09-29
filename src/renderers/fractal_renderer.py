"""Отрисовка фрактала на tkinter.Canvas."""
import tkinter as tk
from src.models.fractal_model import FractalModel, Segment


class FractalRenderer:
    """Масштабирует и рисует набор сегментов на Canvas."""

    def __init__(self, canvas: tk.Canvas) -> None:
        self.canvas = canvas

    def draw(self, segments: list[Segment], zoom: float = 1.0) -> None:
        """Очистить Canvas и нарисовать фрактал с заданным зумом."""
        self.canvas.delete("all")
        if not segments:
            return
        width = max(self.canvas.winfo_width(), 200)
        height = max(self.canvas.winfo_height(), 200)
        min_x, min_y, max_x, max_y = FractalModel.bounds(segments)
        fractal_w = max(max_x - min_x, 1.0)
        fractal_h = max(max_y - min_y, 1.0)
        base_scale = min((width - 50) / fractal_w, (height - 50) / fractal_h)
        scale = base_scale * zoom
        cx = (min_x + max_x) / 2.0
        cy = (min_y + max_y) / 2.0
        for segment in segments:
            x1 = width / 2 + (segment.x1 - cx) * scale
            y1 = height / 2 - (segment.y1 - cy) * scale
            x2 = width / 2 + (segment.x2 - cx) * scale
            y2 = height / 2 - (segment.y2 - cy) * scale
            line_width = max(1, 4 - segment.level // 2)
            self.canvas.create_line(x1, y1, x2, y2, width=line_width,
                                    fill="#1f3f8f")
