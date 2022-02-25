from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class ExplorerInfo(QWidget):

    def __init__(self,environment):
        super().__init__()
        self._environment = environment
        self.setStyleSheet("background-color: #21212F")

        self._layout=QVBoxLayout()
        self.setLayout(self._layout)
        self._layout.setSpacing(0)

        widget=QWidget()
        self._layout.addWidget(widget)

        self._layoutInfo = QVBoxLayout()
        self._layoutInfo.setSpacing(0)
        widget.setLayout(self._layoutInfo)



