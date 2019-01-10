# album.py installery2app 

一键做画册，图片批量排版。
帮摄影师做的一个小工具。指定一个图片文件夹，可以输出排版后的画册。可以节省人力。

使用：
直接运行album_editor.py 或者用pyinstaller 打包成exe使用（mac系统可用py2app打包）

设置：

1、需要指定画册尺寸和上下左右留白。

2、如果某张图需要指定为画册封面，重命名图片，名字里面包含“封面”就行。封面排版是左侧空白的单独一页，封面图片会缩放为正文图片的70%大小。

3、如果想要指定图片的顺序，可以通过重命名，按数字01,02,03这样排。

4、只支持jpg格式，GGB模式。

