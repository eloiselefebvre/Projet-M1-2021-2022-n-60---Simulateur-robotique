from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint
from discoverySimulator.Observable import Observable
from discoverySimulator.config import colors
from discoverySimulator.ressources.PathFinding import PathFinding
from discoverySimulator.ressources.PathFollowing import PathFollowing
from discoverySimulator.robots.Robot import Robot

import time

class Scene(QWidget,Observable):

    MINIMUM_TIME_STEP = 1/60

    def __init__(self,environment,zoomController):
        super().__init__()
        self.__environment = environment
        self.__zoomController = zoomController
        self.__dragObject=False
        self.__isSceneLocked=False
        self.__dragScene = False
        self.__dragSceneOrigin=QPoint(0, 0)
        self.__selectionOffset=(0, 0)
        self.__maximized = False
        self.__size=None
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)
        self.__selectedObj = None
        self.__objectMoved=True
        self.__selectedObjCollidedState=False
        self.__pathFinding=None
        self.setStyleSheet("background-color:"+colors['sceneBackground']+";")
        self._convertedMousePose=QPoint(0, 0)

    def updateLockedScene(self,sender):
        self.__isSceneLocked=sender.getLockState()

    def paintEvent(self,event):
        painter = QPainter(self)
        offset=self.__zoomController.getOffset()
        painter.translate(offset.x(), offset.y())
        painter.scale(self.__zoomController.getZoom(), self.__zoomController.getZoom())

        objects = self.__environment.getVirtualObjects().copy()
        objects.extend(self.__environment.getObjects())
        objects.sort(key=lambda obj: obj.getZIndex())

        for obj in objects:
            painter.save()
            obj.paint(painter)
            painter.restore()

        time.sleep(Scene.MINIMUM_TIME_STEP)
        self.update()

    def mousePressEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)
        self._convertedMousePose = (event.pos() - self.__zoomController.getOffset()) / self.__zoomController.getZoom()

        if event.button()==Qt.LeftButton:
            if self.__pathFollowing is not None:
                pathFinding = PathFinding(self.__environment,
                                          self.__pathFollowing.getRobot().getBoundingWidth() / 2 + PathFinding.SECURITY_MARGIN_OFFSET)
                pathFinding.findPath((self.__pathFollowing.getRobot().getPose().getX(),
                                      self.__pathFollowing.getRobot().getPose().getY()),
                                     (self._convertedMousePose.x(), self._convertedMousePose.y()),
                                     self.__pathFollowing.startFollowing)
                self.__pathFollowing = None
            else:
                self.__objectGrabbed()
                self.__dragObject = True

        if event.button() == Qt.MiddleButton:
            self.__dragScene = True
            self.__dragSceneOrigin = event.pos()

    def mouseReleaseEvent(self,event):
        if self.__pathFollowing is not None:
            self.setCursor(Qt.CrossCursor)
        else:
            self.setCursor(Qt.OpenHandCursor)
        self.__dragObject=False
        self.__dragScene=False
        if self.__selectedObj is not None:
            if not self.__objectMoved:
                self.__selectedObj.setCollidedState(self.__selectedObjCollidedState)
            else:
                self.__selectedObj.setCollidedState(False)
            self.__selectedObj=None

    def mousePose(self):
        return self._convertedMousePose

    def mouseMoveEvent(self, event):
        self._convertedMousePose = (event.pos() - self.__zoomController.getOffset()) / self.__zoomController.getZoom()
        self.notifyObservers("poseChanged")
        if self.__dragObject and self.__selectedObj is not None:
            for obj in self.__environment.getObjects():
                if self.__selectedObj.getIntersectionsWith(obj) and self.__selectedObj!=obj:
                    obj.setCollidedState(False)
            pose = self.__selectedObj.getPose()
            pose.move(self._convertedMousePose.x() - self.__selectionOffset[0], self._convertedMousePose.y() - self.__selectionOffset[1])
            self.__objectMoved=True
            self.__selectedObj.notifyObservers("stateChanged")
            if isinstance(self.__selectedObj, Robot):
                self.__selectedObj.deleteTrajectory()
                self.__selectedObj.deleteOdometry()
                self.__selectedObj.setOdometryPose(pose.copy())

        if self.__dragScene:
            current=event.pos()
            self.__zoomController.setOffset(self.__zoomController.getOffset() + (current - self.__dragSceneOrigin))
            self.__dragSceneOrigin=current

    def wheelEvent(self, event):
        if event.modifiers() and Qt.ControlModifier:
            dir=event.angleDelta().y()
            dir/=abs(dir)

            pos1 = (event.pos() - self.__zoomController.getOffset()) / self.__zoomController.getZoom()

            self.__zoomController.zoomIn() if dir > 0 else self.__zoomController.zoomOut()

            s = ((self.__size - self.__size * self.__zoomController.getZoom()) / 2)
            offset = QPoint(s.width(), s.height()) # pour centrer la fenêtre
            pos2 = (event.pos() - offset) / self.__zoomController.getZoom()
            # pos1 doit devenir pos1 transformée dans le nouveau zoom
            getEqualCoordinatesOffset = (pos1-pos2)*self.__zoomController.getZoom()
            self.__zoomController.setOffset(offset - getEqualCoordinatesOffset)

    def maximized(self):
        self.__maximized=True

    def resizeEvent(self,event):
        if self.__maximized:
            self.__size=self.size()
            self.__zoomController.setSceneSize(self.__size)

    def followPathSelected(self,sender):
        self.setCursor(Qt.CrossCursor)
        self.__pathFollowing=PathFollowing(sender.getRobotSelected())

    def __objectGrabbed(self):
        for obj in self.__environment.getObjects():
            obj.setSelected(False)

        objects = sorted(self.__environment.getObjects(), key=lambda obj:obj.getZIndex())
        objects.reverse()
        for obj in objects:
            if obj.getRepresentation().contains(self._convertedMousePose) and obj.isVisible():
                obj.setSelected(True)
                pose = obj.getPose()
                dx = self._convertedMousePose.x() - pose.getX()
                dy = self._convertedMousePose.y() - pose.getY()
                self.__selectionOffset = (dx, dy)
                if not self.__isSceneLocked:
                    self.__selectedObj = obj
                    self.__selectedObjCollidedState=self.__selectedObj.getCollidedState()
                    self.__objectMoved=False
                    self.__selectedObj.setCollidedState(True)
                break

