# 五子棋人机

GUI使用了PySide6
## 项目文件说明

* main.py: 控制台交互
* mian_gui.py: GUI入口程序
* agent.py: 实现Agent类，含有人机落子算法
* gbboard2.py: 实现Board类，记录棋盘状态及实现判断胜负逻辑
* gbtypes.py: 实现Player枚举类
* gobangMainWidget.py: 针对整个窗口，主要写按钮等控件的槽函数。
* boardScene.py: 针对棋盘窗口，主要重写了鼠标点击、移动等函数

