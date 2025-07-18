from qgis.PyQt.QtCore import QCoreApplication, QSettings
from qgis.PyQt.QtGui import QIcon, QColor, QPixmap
from qgis.PyQt.QtWidgets import QAction, QPushButton, QColorDialog
from qgis.utils import iface

import os.path


class BackgroundToggler:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = self.tr(u'&Background Toggler')

        # Load settings or use defaults
        saved_primary = QSettings().value("BackgroundToggler/primary_color", "#212830")
        saved_secondary = QSettings().value("BackgroundToggler/secondary_color", "#ffffff")
        self.primary_color = QColor(saved_primary)
        self.secondary_color = QColor(saved_secondary)
        self.use_primary = QSettings().value("BackgroundToggler/use_primary", "true") == "true"

        # Setup toolbar
        self.toolbar = self.iface.addToolBar(u'Background Toggler')
        self.toolbar.setObjectName(u'Background Toggler')

        self.add_primary_button()
        self.add_secondary_button()
        self.add_toggle_button()
        self.set_canvas_color()

    def tr(self, message):
        return QCoreApplication.translate('BackgroundToggler', message)

    def add_action(self, icon_path, text, callback, enabled_flag=True, add_to_menu=True, add_to_toolbar=True,
                   status_tip=None, whats_this=None, parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        if status_tip:
            action.setStatusTip(status_tip)
        if whats_this:
            action.setWhatsThis(whats_this)
        if add_to_toolbar:
            self.toolbar.addAction(action)
        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)
        self.actions.append(action)
        return action

    def add_primary_button(self):
        self.primary_button = QPushButton()
        self.primary_button.setToolTip("Pick primary background color")
        self.primary_button.clicked.connect(self.pick_primary_color)
        self.update_primary_icon()
        self.toolbar.addWidget(self.primary_button)

    def add_secondary_button(self):
        self.secondary_button = QPushButton()
        self.secondary_button.setToolTip("Pick secondary background color")
        self.secondary_button.clicked.connect(self.pick_secondary_color)
        self.update_secondary_icon()
        self.toolbar.addWidget(self.secondary_button)

    def add_toggle_button(self):
        self.toggle_button = QPushButton()
        self.toggle_button.setToolTip("Toggle background color")
        self.toggle_button.clicked.connect(self.toggle_background)
        self.update_toggle_icon()
        self.toolbar.addWidget(self.toggle_button)

    def pick_primary_color(self):
        selected = QColorDialog.getColor(self.primary_color, iface.mainWindow(), "Select Primary Background Color")
        if selected.isValid():
            self.primary_color = selected
            self.use_primary = True
            self.save_settings()
            self.set_canvas_color()
            self.update_primary_icon()
            self.update_toggle_icon()

    def pick_secondary_color(self):
        selected = QColorDialog.getColor(self.secondary_color, iface.mainWindow(), "Select Secondary Background Color")
        if selected.isValid():
            self.secondary_color = selected
            self.use_primary = False
            self.save_settings()
            self.set_canvas_color()
            self.update_secondary_icon()
            self.update_toggle_icon()

    def toggle_background(self):
        self.use_primary = not self.use_primary
        self.save_settings()
        self.set_canvas_color()
        self.update_toggle_icon()

    def update_primary_icon(self):
        self.primary_button.setIcon(self.make_color_icon(self.primary_color))
        self.primary_button.setToolTip(f"Primary: {self.primary_color.name()}")

    def update_secondary_icon(self):
        self.secondary_button.setIcon(self.make_color_icon(self.secondary_color))
        self.secondary_button.setToolTip(f"Secondary: {self.secondary_color.name()}")

    def update_toggle_icon(self):
        alt_color = self.secondary_color if self.use_primary else self.primary_color
        self.toggle_button.setIcon(self.make_color_icon(alt_color))
        self.toggle_button.setToolTip(f"Switch to: {alt_color.name()}")

    def make_color_icon(self, color):
        pixmap = QPixmap(40, 20)
        pixmap.fill(color)
        return QIcon(pixmap)

    def set_canvas_color(self):
        color = self.primary_color if self.use_primary else self.secondary_color
        canvas = self.iface.mapCanvas()
        canvas.setCanvasColor(color)
        canvas.refresh()

    def save_settings(self):
        QSettings().setValue("BackgroundToggler/primary_color", self.primary_color.name())
        QSettings().setValue("BackgroundToggler/secondary_color", self.secondary_color.name())
        QSettings().setValue("BackgroundToggler/use_primary", str(self.use_primary).lower())

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u'&Background Toggler'), action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self):
        pass

    def initGui(self):
        pass
