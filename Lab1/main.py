import sys
from PyQt5.QtWidgets import *

from algo import algo
from interface import Interface


def main():
    result = algo('сеть')
    print(result)

    app = QApplication(sys.argv)
    window = Interface()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
