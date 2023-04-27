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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QPushButton, QSizePolicy, QTextEdit, QWidget)

from boardWidget import BoardWidget
import img_rc

class Ui_gobangMainWidget(object):
    def setupUi(self, gobangMainWidget):
        if not gobangMainWidget.objectName():
            gobangMainWidget.setObjectName(u"gobangMainWidget")
        gobangMainWidget.resize(1027, 644)
        gobangMainWidget.setMinimumSize(QSize(450, 450))
        self.widget = QWidget(gobangMainWidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(630, 20, 361, 511))
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.comboBox_2 = QComboBox(self.widget)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gridLayout.addWidget(self.comboBox_2, 0, 1, 1, 1)

        self.textEdit = QTextEdit(self.widget)
        self.textEdit.setObjectName(u"textEdit")

        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 2)

        self.comboBox = QComboBox(self.widget)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 1)

        self.clearBtn = QPushButton(self.widget)
        self.clearBtn.setObjectName(u"clearBtn")

        self.gridLayout.addWidget(self.clearBtn, 2, 1, 1, 1)

        self.pushButton_4 = QPushButton(self.widget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.gridLayout.addWidget(self.pushButton_4, 2, 0, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout)

        self.boardWidget = BoardWidget(gobangMainWidget)
        self.boardWidget.setObjectName(u"boardWidget")
        self.boardWidget.setGeometry(QRect(10, 10, 610, 610))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.boardWidget.sizePolicy().hasHeightForWidth())
        self.boardWidget.setSizePolicy(sizePolicy)
        self.boardWidget.setStyleSheet(u"border-image:url(:/background/gobang.gif)")

        self.retranslateUi(gobangMainWidget)

        QMetaObject.connectSlotsByName(gobangMainWidget)
    # setupUi

    def retranslateUi(self, gobangMainWidget):
        gobangMainWidget.setWindowTitle(QCoreApplication.translate("gobangMainWidget", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("gobangMainWidget", u"PushButton", None))
        self.clearBtn.setText(QCoreApplication.translate("gobangMainWidget", u"\u6e05\u7a7a", None))
        self.pushButton_4.setText(QCoreApplication.translate("gobangMainWidget", u"PushButton", None))
        self.boardWidget.setText("")
    # retranslateUi

