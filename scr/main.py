from cli import cli
from threading import Thread
from core.auto_check import auto_check

if __name__ == "__main__":
    Thread(target=auto_check, daemon=True).start()
    cli()