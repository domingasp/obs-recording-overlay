## Development

`.vscode` contains the settings for this project, specifically enabling import suggestions for `PySide6`.

### Compiling Resources (`qrc`)

To use `.qrc` with PySide6 you must create the qrc file, then using `pyside6-rcc` compile the file.

The following compiliations will need to be completed before you can begin development:

```
pyside6-rcc qml/qml.qrc -o qml/qml_rc.py
pyside6-rcc assets/assets.qrc -o assets/assets_rc.py
pyside6-rcc src/stylesheets.qrc -o src/stylesheets_rc.py
```
