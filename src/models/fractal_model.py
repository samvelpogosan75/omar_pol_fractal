"""Математическая модель фрактального рисунка из зубочисток."""
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Segment:
    """Один отрезок фрактала в декартовых координатах."""

    x1: float
    y1: float
    x2: float
    y2: float
    level: int

    @property
    def horizontal(self) -> bool:
        """Вернуть True, если отрезок горизонтальный."""
        return self.y1 == self.y2


class FractalModel:
    """Генерирует самоподобный узор Омара Пола рекурсивно."""

    def __init__(self, iterations: int = 6, base_length: float = 120.0,
                 ratio: float = 0.5) -> None:
        self.base_length = base_length
        self.ratio = ratio
        self.iterations = 1
        self.set_iterations(iterations)

    def set_iterations(self, iterations: int) -> None:
        """Установить глубину построения от 1 до 8."""
        if not 1 <= iterations <= 8:
            raise ValueError("Количество итераций должно быть от 1 до 8")
        self.iterations = iterations

    def generate(self) -> list[Segment]:
        """Вернуть все отрезки текущего фрактала."""
        result: list[Segment] = []
        self._grow(0.0, 0.0, self.base_length, True, 1, result)
        return result

    def _grow(self, cx: float, cy: float, length: float, horizontal: bool,
              level: int, result: list[Segment]) -> None:
        """Добавить отрезок и рекурсивно породить четыре дочерних."""
        half = length / 2.0
        if horizontal:
            segment = Segment(cx - half, cy, cx + half, cy, level)
            endpoints = ((cx - half, cy), (cx + half, cy))
        else:
            segment = Segment(cx, cy - half, cx, cy + half, level)
            endpoints = ((cx, cy - half), (cx, cy + half))
        result.append(segment)
        if level >= self.iterations:
            return
        child_length = length * self.ratio
        # На каждом конце создаются две параллельные дочерние «зубочистки»
        # со смещением вдоль нового направления. Повторение формирует узор.
        offset = child_length / 2.0
        for ex, ey in endpoints:
            if horizontal:
                self._grow(ex, ey - offset, child_length, False,
                           level + 1, result)
                self._grow(ex, ey + offset, child_length, False,
                           level + 1, result)
            else:
                self._grow(ex - offset, ey, child_length, True,
                           level + 1, result)
                self._grow(ex + offset, ey, child_length, True,
                           level + 1, result)

    @staticmethod
    def bounds(segments: Iterable[Segment]) -> tuple[float, float, float, float]:
        """Вернуть минимальные и максимальные координаты набора отрезков."""
        items = list(segments)
        if not items:
            return (0.0, 0.0, 0.0, 0.0)
        xs = [value for s in items for value in (s.x1, s.x2)]
        ys = [value for s in items for value in (s.y1, s.y2)]
        return min(xs), min(ys), max(xs), max(ys)
