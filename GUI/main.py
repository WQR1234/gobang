from PySide6.QtWidgets import QApplication

from GUI.gobangMainWidget import GobangMainWidget


if __name__ == '__main__':
    app = QApplication()
    w = GobangMainWidget()
    w.show()
    app.exec()
