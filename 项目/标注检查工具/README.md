
标注框坐标含义：   
ocr 坐标：
```python 
self.left_upper, self.right_upper, self.right_bottom, self.left_bottom = self.position     
```  

处理标注框：   
```python 
xmin = min(zimu.left_upper[0], zimu.left_bottom[0])
ymin = min(zimu.left_upper[1], zimu.right_upper[1])
width = max(zimu.right_bottom[0] - zimu.left_upper[0], zimu.right_upper[0] - zimu.left_bottom[0])
height = max(zimu.left_bottom[1] - zimu.right_upper[1], zimu.right_bottom[1] - zimu.left_upper[1])
```

logo 和 breed 坐标：是左上角和右下角坐标。    

方法：坐标基本上就是两种形式：两个坐标点，或者是一个坐标点和 width height。判断方法就是看后面两个元素是不是有比前面对应的元素小的数，如果有小的就是 width height，如果都是大的数字，就应该是两个坐标点。           


## 需求   

目的：修订；标注  

字幕很多；不是每张图片都要修，不是每张图片都有文字；   

应该是一个单选框；要不要编辑按钮，还是说用输入框格式。   




素材库修订   

全部标记已修   

列表搜索：文件名、内容     

详细搜索：      

量太大：过滤   

已修未修   

标注框：花字框太多，选择显示，需要的显示；logo 多个；字幕；删除；   

漏字：加号加字；调整顺序；   

错误做标记，以后再修改      

筛选特定类型   

缩略图，一个页面显示多个   

标记一部分，同步整个视频品种，可以大幅提高效率   


画框   





