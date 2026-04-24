from setup import setup
from messenger import server


def main():
    setup()
    server.run()

if __name__ == '__main__':
    main()
