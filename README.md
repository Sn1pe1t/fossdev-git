# Simple Calculator: надёжные арифметические операции

Минималистичная Python‑библиотека для сложения, вычитания, умножения и деления с автоматизацией сборки и публикации на test.pypi.org.

## Быстрый старт (Автоматизация)

Все ключевые действия выполняются через `Makefile` из корня репозитория:

| Команда | Что делает |
|---------|-------------|
| `make venv` | Создаёт виртуальное окружение `.venv` |
| `make install` | Устанавливает зависимости и сам пакет в режиме `editable` |
| `make test` | Запускает pytest (все тесты в `tests/`) |
| `make lint` | Проверяет стиль кода (flake8) |
| `make typecheck` | Проверяет аннотации типов (mypy) |
| `make format` | Автоматически форматирует код (black) |
| `make build` | Собирает дистрибутивы (`.whl` и `.tar.gz`) в `dist/` |
| `make upload-test` | Публикует пакет на **test.pypi.org** (требуется API‑токен) |
| `make clean` | Удаляет `.venv`, `dist/`, `build/`, кэши |

## Установка из test.pypi.org

```bash
pip install -i https://test.pypi.org/simple/ simplecalc-pypi-test==0.1.0
```