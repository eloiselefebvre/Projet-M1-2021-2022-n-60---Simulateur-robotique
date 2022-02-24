from PyQt5.QtWidgets import QWidget, QTextEdit, QHBoxLayout, QVBoxLayout, QMenuBar

from robotSimulator.interface.MenuBar import MenuBar


class ToolsBar(QVBoxLayout):

    TOOLS_BAR_FIXED_HEIGHT = 60

    def __init__(self,environment):
        super().__init__()
        self._environment=environment


        self._searchBarLayout=QHBoxLayout()
        self._displayBarLayout=QHBoxLayout()
        # self.addLayout(self.layoutTimeElapsed(),20)
        # self.addLayout(self.layoutModifyTime(),20)
        # self.addLayout(self.layoutModifyAcceleration(),20)

        self.addLayout(self._searchBarLayout,30)
        self.addLayout(self._displayBarLayout,70)

        self._menuBarWidget = MenuBar()

        self._searchBarLayout.addWidget(self._menuBarWidget)




    def layoutTimeElapsed(self):
        layoutTimeElapsed=QVBoxLayout()

        self._timeElapsedWidget=QWidget()

        layoutTimeElapsed.addWidget(self._timeElapsedWidget)
        self._timeElapsedWidget.setStyleSheet("background-color: #21212F")
        self._timeElapsedWidget.setFixedHeight(self.TOOLS_BAR_FIXED_HEIGHT)

        return layoutTimeElapsed

    def layoutModifyTime(self):
        layoutModifyTime=QVBoxLayout()

        self._layoutModifyTimeWidget=QWidget()

        layoutModifyTime.addWidget(self._layoutModifyTimeWidget)
        self._layoutModifyTimeWidget.setStyleSheet("background-color: #21212F")
        self._layoutModifyTimeWidget.setFixedHeight(self.TOOLS_BAR_FIXED_HEIGHT)

        return layoutModifyTime

    def layoutModifyAcceleration(self):
        layoutModifyAcceleration=QVBoxLayout()

        self._layoutModifyAccelerationWidget=QWidget()

        layoutModifyAcceleration.addWidget( self._layoutModifyAccelerationWidget)
        self._layoutModifyAccelerationWidget.setStyleSheet("background-color: #21212F")
        self._layoutModifyAccelerationWidget.setFixedHeight(self.TOOLS_BAR_FIXED_HEIGHT)

        return layoutModifyAcceleration

    def getHeight(self):
        return self.TOOLS_BAR_FIXED_HEIGHT


