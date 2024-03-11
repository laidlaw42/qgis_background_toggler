from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon, QColor, QPixmap
from qgis.PyQt.QtWidgets import QAction, QPushButton, QColorDialog
from qgis.utils import iface

import os.path

# Import the code for the DockWidget
from .background_toggler_dockwidget import BackgroundTogglerDockWidget


class BackgroundToggler:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Background Toggler')
        self.colors = []  # Store colors
        self.current_color_index = 0

        # Settings keys
        self.settings = QSettings()
        self.settings.beginGroup('BackgroundToggler')
        self.settings_key = 'colors'

        # Load colors from settings or set defaults
        self.load_colors()

        # Create toolbar
        self.toolbar = self.iface.addToolBar(u'Background Toggler')
        self.toolbar.setObjectName(u'Background Toggler')

        # Add toggle button
        self.add_toggle_button()

        # Set initial canvas color
        self.set_canvas_color()

    def tr(self, message):
        """Get the translation for a string using Qt translation API."""
        return QCoreApplication.translate('BackgroundToggler', message)

    def add_action(self, icon_path, text, callback, enabled_flag=True, add_to_menu=True, add_to_toolbar=True,
                   status_tip=None, whats_this=None, parent=None):
        """Add a toolbar icon to the toolbar."""
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    def add_toggle_button(self):
        """Add a button to toggle background color."""
        # Create a QPushButton widget
        self.toggle_button = QPushButton()

        # Set the initial icon and color
        self.update_button_icon()

        # Connect the clicked signal to the toggle_color method
        self.toggle_button.clicked.connect(self.toggle_color)

        # Add the button to the toolbar
        self.toolbar.addWidget(self.toggle_button)

    def update_button_icon(self):
        """Update the button icon based on the current color."""
        color = self.colors[self.current_color_index]
        icon = self.create_icon(color)
        self.toggle_button.setIcon(icon)

    def create_icon(self, color):
        """Create an icon with a colored box."""
        pixmap = QPixmap(40, 20)
        pixmap.fill(color)
        return QIcon(pixmap)

    def load_colors(self):
        """Load colors from settings or set defaults."""
        saved_colors = self.settings.value(self.settings_key, None)
        if saved_colors is not None:
            self.colors = [QColor(color) for color in saved_colors]
        else:
            # Set default colors if not saved
            self.colors = [QColor("black"), QColor("white"), QColor("grey")]
        # Ensure current_color_index is within bounds
        self.current_color_index = min(self.current_color_index, len(self.colors) - 1)

    def toggle_color(self):
        """Toggle the background color when the button is clicked."""
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)
        self.update_button_icon()
        self.set_canvas_color()

    def set_canvas_color(self, color=None):
        """Set the canvas background color to the current color or the provided color."""
        if color is None:
            color = self.colors[self.current_color_index]
        canvas = self.iface.mapCanvas()
        canvas.setCanvasColor(color)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.save_colors()  # Save colors before unloading

        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u'&Background Toggler'), action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that loads and starts the plugin"""
        pass

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        pass  # No need for initGui since we removed the menu and toolbar logic
