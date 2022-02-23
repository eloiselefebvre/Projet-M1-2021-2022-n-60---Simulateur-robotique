from PyQt5.QtWidgets import QWidget, QTextEdit, QHBoxLayout, QVBoxLayout


class ToolsBar(QHBoxLayout):

    def __init__(self,environment):
        super().__init__()
        self._environment=environment
        self.addLayout(self.layoutTimeElapsed(),20)
        self.addLayout(self.layoutModifyTime(),20)
        self.addLayout(self.layoutModifyAcceleration(),20)


    def layoutTimeElapsed(self):
        layoutTimeElapsed=QVBoxLayout()

        self._timeElapsedWidget=QWidget()

        layoutTimeElapsed.addWidget(self._timeElapsedWidget)
        self._timeElapsedWidget.setStyleSheet("background-color: #21212F")
        self._timeElapsedWidget.setFixedHeight(60)

        return layoutTimeElapsed

    def layoutModifyTime(self):
        layoutModifyTime=QVBoxLayout()

        self._layoutModifyTimeWidget=QWidget()

        layoutModifyTime.addWidget(self._layoutModifyTimeWidget)
        self._layoutModifyTimeWidget.setStyleSheet("background-color: #21212F")
        self._layoutModifyTimeWidget.setFixedHeight(60)

        return layoutModifyTime

    def layoutModifyAcceleration(self):
        layoutModifyAcceleration=QVBoxLayout()

        self._layoutModifyAccelerationWidget=QWidget()

        layoutModifyAcceleration.addWidget( self._layoutModifyAccelerationWidget)
        self._layoutModifyAccelerationWidget.setStyleSheet("background-color: #21212F")
        self._layoutModifyAccelerationWidget.setFixedHeight(60)

        return layoutModifyAcceleration


