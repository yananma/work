
用这个 [video-to-text-ocr-demo](https://github.com/HenryLulu/video-to-text-ocr-demo) 项目的代码出了很多的问题  

1. 这个项目用的是 Python2，所以要先给 print 加上括号  
2. 导包有问题，cv2 就是 opencv-python 
3. aip 要用命令 `pip install baidu-aip -i https://pypi.douban.com/simple --trusted-host pypi.douban.com` 安装  
4. 如果安装 aip 的时候 pygit2 包报错了，就是版本不对，要用 `pip install pip install pygit2==0.26.4` 安装  
5. 参数不是在 pycharm 的命令行里配置的，是在 index.py 文件里配置的  
6. getframe.py 要单独运行才会切成图片 
7. getframe.py 文件运行不成功，要把保存图片那一行，改成 `cv2.imencode('.jpg', frame)[1].tofile(outputDir + str(count).zfill(10) + '.jpg')`  
8. 
