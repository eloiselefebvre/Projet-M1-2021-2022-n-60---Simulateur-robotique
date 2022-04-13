import os

from PyQt5.QtGui import QFont

fullpath = os.path.realpath(__file__)
path, filename = os.path.split(fullpath)
config = {
    "appname":"Discovery Simulator",
    "ressourcesPath": os.path.join(path, 'ressources', 'icons'),
    "real_update_time_step": 0}

# https://chir.ag/projects/name-that-color/
colors = {
    "white":"#fff",  # == zoom menu bar item selected fot color
    "alabaster":"#f9f9f9", # == explorer info/toolbar font color, footer background, scene overview background
    "gallery":"#f0f0f0",  # == scene background, toolbar font color
    "silver":"#c4c4c4",  # == footer border color
    "tuna": "#323247",  # == button hover
    "mulled-wine":"#4c4c68",  # == button pressed, toolbar border color
    "mischka":"#dfe0e5",  # == explorer tree item selected font color
    "tundora":"#444",  # == explorer info border color, footer font color, environment border color
    "mid-gray":"#63656d", # == explorer tree item font color
    "steel-gray":"#21212f",  # == toolbar background, explorer info background
    "mirage":"#151825",  # == wheel color, explorer background
    "picton-blue":"#26bee5",  # == explorer filter item hover color, explorer tree item selected background, footer zoom menu hover item background
    "blue-violet":"#675bb5",  # == scene overview window border color
    "salmon":"#f9886a",  # == scene overview border color
    "red":"#f00",
    "green":"#0f0",
    "blue":"#00f",
    "yellow":"#ff0"
}

# FONTS
fontFamily = "Verdana" # Available : Sanserif, Arial

smallSize=10
small = QFont(fontFamily,smallSize)
smallBold = QFont(fontFamily,smallSize)
smallBold.setBold(True)

normalSize=12
normal = QFont(fontFamily,normalSize)
normalBold = QFont(fontFamily,normalSize)
normalBold.setBold(True)

fonts={
    "small": small,
    "small_bold": smallBold,
    "normal":normal,
    "normal_bold":normalBold
}