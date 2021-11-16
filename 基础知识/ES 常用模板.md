
查询 text 类型，使用 query_string 或 match_phrase，完全匹配关键字类型，用 term.  

查看索引字段  
`GET kejisousou`  

在所有索引中查询，就是不指定索引名查询  
`GET _search`  

查看数量  
`GET /kejisousou-testv5/_count`  

query_string 查询  

最常用的是这个  
```python 
GET test-zky/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "query_string": {
            "default_field": "url",
            "query": "\"http://kuaibao.qq.com/s/93560f119f336852\" 
            or \"https://finance.sina.com.cn/tech/2021-07-16/doc-ikqcfnca7213437.shtml\""
          }
        }
      ]
    }
  }
}
```

query_string 查多个 id，最开始和结束都有斜杠  
```python 
GET kejisousou-en-formal/_search
{
  "query": {
    "query_string": {
      "default_field": "entry_id",
      "query": "\"647520\" OR \"647521\" OR \"647522\" OR \"647542\""
    }
  }
}
```

```python 
GET kejisousou-en-testv3/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "query_string": {
            "fields": ["title", "text"],
            "query": "math"
          }
        }
      ]
    }
  }
}
```

```python 
GET /kejisousou-en-testv3/_search
{
  "query": {
    "query_string": {
      "fields": ["title", "text"],
      "query": "math"
    }
  }
}
```

多条件查询  

```python 
GET kejisousou-en-yuce-formal-v2/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "terms": {
            "url.raw": [
              "https://news.mit.edu/2021/automated-machine-learning-veeramachaneni-1006", 
              "https://oraclesinvestmentgroup.medium.com/oig-ama-with-darenft-50be70784ef4", 
              "https://www.nsf.gov/discoveries/disc_summ.jsp?cntn_id=303606&org=NSF&from=news",
              "https://news.mit.edu/2021/does-artificial-intelligence-play-well-others-1004"
            ]
          }
        }
      ]
    }
  }
}
```


在多个字段中查询  

```python 
GET test-zky/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "query_string": {
            "fields": ["title", "text"],
            "query": "\"拉曼研究所\""
          }
        }
      ]
    }
  },
  "_source": ["title", "url", "post_time", "text"]
}
```

title.keyword  
```python 
GET test-zky/_search 
{
  "query": {
    "term": {
      "title.keyword": {
        "value": "落户合肥"
      }
    }
  }, 
  "_source": ["title", "text"]
}
```

用 sort 排序实现查询第一条和最后一条
```python 
GET kejisousou-test/_search
{
  "size": 1,
  "_source": "post_time",
  "sort": [
    {
      "post_time": {
        "order": "asc"
      }
    }
  ]
}
```


#### 聚合  

按月份聚合  
```python 
GET /kejisousou-en-test/_search
{
  "size": 0,
  "aggs": {
    "time_aggs": {
      "date_histogram": {
        "field": "post_time",
        "time_zone": "+08:00",
        "interval": "month",
        "format": "yyyy-MM"
      }
    }
  }
}
```

按分类聚合  
```python 
GET /kejisousou-en-test/_search
{
  "size": 0,
  "aggs": {
    "category_aggs": {
      "terms": {
        "field": "category.keyword"
      }
    }
  }
}
```

先按月份聚合，然后每个月按分类聚合  
```python 
GET /kejisousou-en-test/_search
{
  "size": 0,
  "aggs": {
    "time_aggs": {
      "date_histogram": {
        "field": "post_time",
        "time_zone": "+08:00",
        "interval": "month",
        "format": "yyyy-MM"
      },
      "aggs": {
        "category_aggs": {
          "terms": {
            "field": "category.keyword"
          }
        }
      }
    }
  }
}
```

限定日期范围聚合查询  

```python 
GET /kejisousou-en-test/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "post_time": {
              "gte": "2020-01-01 00:00:00",
              "lte": "2021-09-09 00:00:00"
            }
          }
        }
      ]
    }
  },
  "size": 0,
  "aggs": {
    "time_aggs": {
      "date_histogram": {
        "field": "post_time",
        "interval": "month"
      }
    }
  }
}
```

聚合后根据聚合结果的数量排序  

```python 
GET page/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "include_time": {
              "gte": "2021-10-01 00:00:00",
              "lte": "2021-10-25 00:00:00"
            }
          }
        }
      ]
    }
  },
  "aggs": {
    "NAME": {
      "date_histogram": {
        "field": "include_time",
        "interval": "day",
        "order": {
          "_count": "asc"
        }
      }
    }
  },
  "size": 0
}
```

按 entry_id 聚合，这样可以看到都有哪些 entry_id。    

```python 
GET /kejisousou-en-testv1/_search
{
  "size": 0,
  "aggs": {
    "category_aggs": {
      "terms": {
        "field": "entry_id",
        "size": 1000    # 这个 size 是 agg 的类别条数，不是具体内容的条数
      }
    }
  },
  "size": 0
}
```

按照 id 筛选，再按照时间排序，就可以看到这个 id 下的按顺序排列的结果  

```python 
GET kejisousou-en-test/_search
{
  "query": {
    "match_phrase": {
      "entry_id": "647232"
    }
  }, 
  "size": 161,
  "_source": "post_time",
  "sort": [
    {
      "post_time": {
        "order": "desc"
      }
    }
  ]
}
```


### script  

```python 
GET kejisousou-yuce-formal-v3/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "script": {
            "script": "doc[\"point_text.raw\"].value.length()==0"
          }
        }
      ]
    }
  }
}
```

### 正则  

不用 raw，会分词，分词以后就不是正则了，就成了单个字和符号的匹配了  

```python 
GET kejisousou-zhili-formal-v3/_search
{
  "query": {
    "regexp": {
      "point_text.raw": ".*只是因为.*"
    }
  }
}
```

