from core.startup import startup
from app.cli.shell import CommandShell


def main():

    startup()

    shell = CommandShell()

    shell.start()


if __name__ == "__main__":
    main()