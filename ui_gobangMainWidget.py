# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gobangMainWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGraphicsView, QGridLayout,
    QHBoxLayout, QPushButton, QSizePolicy, QTextEdit,
    QWidget)
import img_rc

class Ui_GobangMainWidget(object):
    def setupUi(self, GobangMainWidget):
        if not GobangMainWidget.objectName():
            GobangMainWidget.setObjectName(u"GobangMainWidget")
        GobangMainWidget.resize(1200, 950)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GobangMainWidget.sizePolicy().hasHeightForWidth())
        GobangMainWidget.setSizePolicy(sizePolicy)
        GobangMainWidget.setMinimumSize(QSize(450, 450))
        self.widget = QWidget(GobangMainWidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(910, 10, 280, 600))
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.comboBox_2 = QComboBox(self.widget)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gridLayout.addWidget(self.comboBox_2, 0, 1, 1, 1)

        self.textEdit = QTextEdit(self.widget)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 2)

        self.comboBox = QComboBox(self.widget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setEditable(False)

        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 1)

        self.retractBtn = QPushButton(self.widget)
        self.retractBtn.setObjectName(u"retractBtn")

        self.gridLayout.addWidget(self.retractBtn, 3, 0, 1, 1)

        self.clearBtn = QPushButton(self.widget)
        self.clearBtn.setObjectName(u"clearBtn")

        self.gridLayout.addWidget(self.clearBtn, 2, 1, 1, 1)

        self.startBtn = QPushButton(self.widget)
        self.startBtn.setObjectName(u"startBtn")

        self.gridLayout.addWidget(self.startBtn, 2, 0, 1, 1)

        self.resignBtn = QPushButton(self.widget)
        self.resignBtn.setObjectName(u"resignBtn")

        self.gridLayout.addWidget(self.resignBtn, 3, 1, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout)

        self.boardView = QGraphicsView(GobangMainWidget)
        self.boardView.setObjectName(u"boardView")
        self.boardView.setGeometry(QRect(10, 10, 900, 900))
        self.boardView.setStyleSheet(u"border-image:url(:/imgs/grid_board.jpg)")

        self.retranslateUi(GobangMainWidget)

        QMetaObject.connectSlotsByName(GobangMainWidget)
    # setupUi

    def retranslateUi(self, GobangMainWidget):
        GobangMainWidget.setWindowTitle(QCoreApplication.translate("GobangMainWidget", u"\u4e94\u5b50\u68cb", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("GobangMainWidget", u"\u4eba", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("GobangMainWidget", u"\u673a", None))

        self.comboBox.setItemText(0, QCoreApplication.translate("GobangMainWidget", u"\u4eba", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("GobangMainWidget", u"\u673a", None))

        self.retractBtn.setText(QCoreApplication.translate("GobangMainWidget", u"\u6094\u68cb", None))
        self.clearBtn.setText(QCoreApplication.translate("GobangMainWidget", u"\u6e05\u7a7a", None))
        self.startBtn.setText(QCoreApplication.translate("GobangMainWidget", u"\u5f00\u59cb", None))
        self.resignBtn.setText(QCoreApplication.translate("GobangMainWidget", u"\u8ba4\u8f93", None))
    # retranslateUi

