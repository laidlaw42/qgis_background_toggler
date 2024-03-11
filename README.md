# Background Toggler Plugin for QGIS

## Description:

First attempt at a QGIS plugin using Plugin Builder.
This QGIS plugin allows users to toggle the background colour of the map canvas between different predefined colours. The plugin adds a toolbar button to the QGIS interface, which, when clicked, cycles through a set of predefined background colours for the map canvas.

## Features:

- Adds a toolbar button to toggle the background colour of the map canvas.
- Allows users to cycle through predefined background colours.
- Will eventually add a way to set and remove specific colours

## Implementation Details:

- The plugin is implemented using the QGIS plugin framework.
- It uses PyQt for GUI elements and interactions.
- The plugin maintains a list of predefined background colours, which users can cycle through using the toolbar button.
- colours are saved and loaded using QSettings for persistence between QGIS sessions.
- The plugin includes methods for adding toolbar buttons, updating button icons, setting canvas colours, and handling user interactions.

## Usage:

1. Download a zip of this repo.
2. In QGIS, go to Plugins > Manage and Install Plugins... > Install from zip
3. Activate the plugin from the Plugins menu.
4. A toolbar button labeled "Background Toggler" will appear.
5. Clicking the button will cycle through predefined background colours (black, white, grey) for the map canvas.

## Requirements:

- QGIS 3.x
- PyQt5

## License:

- GNU General Public License version 2 or later
