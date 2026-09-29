"""Тесты математической модели."""
import unittest
from src.models.fractal_model import FractalModel


class FractalModelTests(unittest.TestCase):
    def test_one_iteration_has_one_segment(self) -> None:
        self.assertEqual(len(FractalModel(iterations=1).generate()), 1)

    def test_two_iterations_have_five_segments(self) -> None:
        self.assertEqual(len(FractalModel(iterations=2).generate()), 5)

    def test_first_segment_is_horizontal(self) -> None:
        first = FractalModel(iterations=2).generate()[0]
        self.assertTrue(first.horizontal)

    def test_second_level_is_vertical(self) -> None:
        segments = FractalModel(iterations=2).generate()
        self.assertTrue(all(not segment.horizontal for segment in segments[1:]))

    def test_child_length_is_reduced(self) -> None:
        model = FractalModel(iterations=2, base_length=100, ratio=0.5)
        segments = model.generate()
        child = segments[1]
        self.assertAlmostEqual(abs(child.y2 - child.y1), 50.0)

    def test_invalid_iterations(self) -> None:
        with self.assertRaises(ValueError):
            FractalModel(iterations=0)
        with self.assertRaises(ValueError):
            FractalModel(iterations=9)

    def test_bounds_are_symmetric(self) -> None:
        model = FractalModel(iterations=3)
        min_x, min_y, max_x, max_y = model.bounds(model.generate())
        self.assertAlmostEqual(abs(min_x), abs(max_x))
        self.assertAlmostEqual(abs(min_y), abs(max_y))

    def test_every_level_is_present(self) -> None:
        segments = FractalModel(iterations=5).generate()
        self.assertEqual({s.level for s in segments}, {1, 2, 3, 4, 5})


if __name__ == "__main__":
    unittest.main()
