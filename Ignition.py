import sys
from PyQt6.QtWidgets import QApplication
from main_window import App
from qt_material import apply_stylesheet

def main():
    app = QApplication(sys.argv)

    window = App()
    window.show()

    apply_stylesheet(app, theme="dark_teal.xml")

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
