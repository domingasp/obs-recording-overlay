from PySide6.QtCore import QFile


def load_stylesheet(stylesheet_path: str) -> str:
    stylesheet = ""
    stylesheet_file = QFile(stylesheet_path)
    if stylesheet_file.open(QFile.OpenModeFlag.ReadOnly):
        stylesheet = stylesheet_file.readAll().toStdString()
        stylesheet_file.close()

    return stylesheet
