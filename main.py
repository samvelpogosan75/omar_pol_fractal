"""Точка входа в приложение «Фрактал Омара Пола»."""
from src.app import OmarPolApp


def main() -> None:
    """Запустить графическое приложение."""
    app = OmarPolApp()
    app.run()


if __name__ == "__main__":
    main()
