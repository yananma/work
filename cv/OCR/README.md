
### 展示识别框  

参考 github 的 quickstart：https://github.com/PaddlePaddle/PaddleOCR/blob/95c670faf6cf4551c841764cde43a4f4d9d5e634/doc/doc_ch/quickstart.md    

```python 
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # need to run only once to download and load model into memory
img_path = 'a.png'
result = ocr.ocr(img_path, cls=True)
print(result)
for line in result:
    print(line)
image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores)
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')
```

