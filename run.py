r"""
Одновременный запуск бэкенда (FastAPI) и фронтенда (Next.js)

Запуск:
    # С активированным venv
    venv\Scripts\activate
    python run.py

    # Или без активации (скрипт сам найдёт venv)
    python run.py

Бэкенд:  http://localhost:8000  (API + Swagger UI на /docs)
Фронтенд: http://localhost:3000  (веб-интерфейс)
"""

import subprocess
import sys
import os
import time
import threading

# Принудительно UTF-8 для вывода (фикс UnicodeEncodeError на Windows)
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
os.environ.setdefault('PYTHONUTF8', '1')
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def get_venv_python():
    """Получить путь к Python из venv, если он существует"""
    venv_python = os.path.join('venv', 'Scripts', 'python.exe')
    if os.path.exists(venv_python):
        return venv_python
    return sys.executable


def check_node():
    """Проверяем наличие Node.js"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def install_frontend_deps():
    """Установка зависимостей фронтенда при необходимости"""
    node_modules = os.path.join('frontend', 'node_modules')
    if not os.path.exists(node_modules):
        print("📦 Установка зависимостей фронтенда...")
        subprocess.run(['npm', 'install'], cwd='frontend', shell=True)
        print("✓ Зависимости установлены\n")


def stream_output(proc, prefix):
    """Чтение вывода процесса в отдельном потоке (неблокирующее)"""
    try:
        for line in proc.stdout:
            try:
                print(f"[{prefix}] {line.rstrip()}")
            except UnicodeEncodeError:
                print(f"[{prefix}] (строка с неподдерживаемыми символами)")
    except Exception:
        pass


def main():
    print("\n" + "=" * 60)
    print("  🚀 Инвестиционный помощник — запуск")
    print("=" * 60)

    # Проверяем Node.js
    if not check_node():
        print("❌ Node.js не найден. Установите с https://nodejs.org")
        sys.exit(1)

    # Устанавливаем зависимости фронтенда если нужно
    install_frontend_deps()

    # Запускаем бэкенд (используем venv если есть)
    python_exe = get_venv_python()
    print(f"▶  Запуск бэкенда (FastAPI :8000)...")
    print(f"   Python: {python_exe}")
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    backend = subprocess.Popen(
        [python_exe, '-m', 'src.api.server'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding='utf-8',
        env=env,
    )

    # Ждём пока бэкенд поднимется
    time.sleep(4)

    # Проверяем, не упал ли бэкенд сразу
    if backend.poll() is not None:
        print("\n❌ Бэкенд упал при запуске. Вывод:")
        output = backend.stdout.read()
        print(output)
        sys.exit(1)

    # Запускаем потоки чтения вывода
    backend_thread = threading.Thread(
        target=stream_output, args=(backend, 'backend'), daemon=True
    )
    backend_thread.start()

    # Запускаем фронтенд
    print("▶  Запуск фронтенда (Next.js :3000)...")
    frontend = subprocess.Popen(
        ['npm', 'run', 'dev'],
        cwd='frontend',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding='utf-8',
        env=env,
    )

    frontend_thread = threading.Thread(
        target=stream_output, args=(frontend, 'frontend'), daemon=True
    )
    frontend_thread.start()

    print("\n" + "=" * 60)
    print("  ✅ Серверы запущены!")
    print("=" * 60)
    print("\n  🌐 Веб-интерфейс:  http://localhost:3000")
    print("  📡 API:           http://localhost:8000")
    print("  📚 Swagger UI:    http://localhost:8000/docs")
    print("\n  ⏹  Нажмите Ctrl+C для остановки\n")

    try:
        # Мониторинг — проверяем, что оба процесса живы
        while True:
            if backend.poll() is not None:
                print(f"\n❌ Бэкенд остановился (код {backend.returncode})")
                break
            if frontend.poll() is not None:
                print(f"\n❌ Фронтенд остановился (код {frontend.returncode})")
                break
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n⏹  Остановка серверов...")

    # Останавливаем оба процесса
    for proc, name in [(backend, 'бэкенд'), (frontend, 'фронтенд')]:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
                print(f"✓ {name} остановлен")
            except subprocess.TimeoutExpired:
                proc.kill()
                print(f"✓ {name} принудительно остановлен")


if __name__ == "__main__":
    main()
