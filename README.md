<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
![Downloads][downloads-shield]
[![Stargazer][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Latest Version][latest-version-shield]][latest-version-url]
[![Latest Build][latest-build-shield]][latest-build-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <img src="https://github.com/user-attachments/assets/f2386a32-59c9-44e7-809f-7a6daf12b600" alt="OBS Recording Overlay" height="84px"/>
  
  <h3 align="center">OBS Recording Overlay</h3>

  <p align="center"><em>Am I recording? Am I not?</em> <strong>Now</strong> you'll know!</p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

An app for the 1 monitor users out there, simply shows an overlay in the bottom left of your screen indicator your `OBS` recording status.

The app has 2 overlays; recording 🔴, and paused ⏸️.

<div align="center">
  <img src="https://github.com/user-attachments/assets/bc8553c2-7d44-40bb-9bf6-741e13a510b8" width="45%"/>
  <img src="https://github.com/user-attachments/assets/59ce107e-7823-44f4-8a10-2cfae58fdbf5" width="45%" />
</div>

<br />

> [!IMPORTANT]  
> You'll need to ensure your games are running in `Borderless fullscreen`.
> <br /><br />Have a look at [Borderless Gaming](https://github.com/Codeusa/Borderless-Gaming) if your game doesn't have this option... *MINECRAFT* 🤦



After installation, launch the app, you should see the icon in the system tray.

<div align="center">
  <img src="https://github.com/user-attachments/assets/55bdb6c0-e1a5-4380-96d8-7997eebc3a6e" alt="Windows system tray with app icon" height="100px" />
</div>

Right-click the icon to see the connection status and **most importantly** configure the connection settings for your OBS WebSocket.

<div align="center">
  <img src="https://github.com/user-attachments/assets/12c03606-c89c-4a54-a452-49c7830e9330" alt="System tray menu: Connected. Options: Configure connection, Quit." />
</div>

<br />
<p align="center">
  Once the correct details have been configured your work is done 😮‍💨 The app takes care of the rest!
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![PySide6][PySide6]][pyside6-url]

# Development

`.vscode` contains the settings for this project, specifically enabling import suggestions for `PySide6`.

## Compiling Resources (`qrc`)

To use `.qrc` with PySide6 you must create the qrc file, then using `pyside6-rcc` compile the file.

The following compiliations will need to be completed before you can begin development:

```
pyside6-rcc qml/qml.qrc -o qml/qml_rc.py
pyside6-rcc assets/assets.qrc -o assets/assets_rc.py
pyside6-rcc src/stylesheets.qrc -o src/stylesheets_rc.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[downloads-shield]: https://img.shields.io/github/downloads/domingasp/obs-recording-overlay/total?label=Downloads
[stars-shield]: https://img.shields.io/github/stars/domingasp/obs-recording-overlay?style=flat&label=Stars
[stars-url]: https://github.com/domingasp/obs-recording-overlay/stargazers
[issues-shield]: https://img.shields.io/github/issues/domingasp/obs-recording-overlay
[issues-url]: https://github.com/domingasp/obs-recording-overlay/issues
[latest-version-shield]: https://img.shields.io/github/v/tag/domingasp/obs-recording-overlay?label=Latest
[latest-version-url]: https://github.com/domingasp/obs-recording-overlay/releases
[latest-build-shield]: https://github.com/domingasp/obs-recording-overlay/actions/workflows/main.yml/badge.svg
[latest-build-url]: https://github.com/domingasp/obs-recording-overlay/actions/workflows/main.yml
[system-tray-icon-screenshot]: https://github.com/user-attachments/assets/55bdb6c0-e1a5-4380-96d8-7997eebc3a6e
[context-menu-screenshot]: https://github.com/user-attachments/assets/12c03606-c89c-4a54-a452-49c7830e9330
[PySide6]: https://img.shields.io/badge/PySide6-%2341CD52?style=flat&logo=qt&logoColor=white
[PySide6-url]: https://pypi.org/project/PySide6/
