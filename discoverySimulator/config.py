import os

from PyQt5.QtGui import QFont

fullpath = os.path.realpath(__file__)
path, filename = os.path.split(fullpath)
config = {"ressourcesPath": os.path.join(path, 'ressources', 'icons'), "real_update_time_step": 0}

colors = {
    "sceneBackground" : "#F0F0F0",
    "sceneOverviewBorder" : "#F9886A",
    "font" : "#F9F9F9",
    "explorerBackground" : "#151825",
    "buttonOver" : "#323247",
    "buttonPressed" : "#4C4C68",
    "explorerInfoBackground" : "#21212F",
    "widgetBorder" : "#444",
    "explorerTreeItem" : "#63656D",
    "crawlerColor" : "#DFE0E5",
    "borderColor" : "#25CCF7",
    "widgetBorderFooter" : "#C4C4C4",
    "painter" : "#675BB5",
    "white" : "#fff",
    "titleBorder" : "#4D4D6D",
    "borderScreen" : "#444",
    "trajectory" :"#F9886A",
    "odometry" : "#8B86AC",
    "LIDAR" : "#1C1E32",
    "sensor" : "#F00"
}

# FONTS
fontFamily = "Verdana" # Sanserif, Arial

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
# TODO : Revoir noms de couleurs et structure (ex : colors.view.... ou colors uniquement pour le dossier interface)