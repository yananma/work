

#### 1、国家文章列表第一页显示不够 10 条，但是第二页还有数据的问题 09.03  

不只是第一页显示不全，而是第一页显示的是最后一页的数据，显示的原因就是中间把 page 给改了，中间改 page 的原因是访问最后的一页的时候，可以跳转到真正的最后一页。  

核心应该是做一个页数的判定，如果访问的页数比真实的页数大，那么就显示到最后一页。如果页数比真实的页数少，但 limit > len(posts)，page 就不变。  

所以加了一个判断就解决了。  

```python 
if page > (all_post_count - 1) // 10:
    page = (all_post_count - 1) // 10 if all_post_count else 0
```

