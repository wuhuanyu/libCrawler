# ISee 爬虫

为ISee项目提供数据支持，使用了scrapy框架。

抓取BBC，CNN，Reuters,Medium,TheMillionBooks，丢进Mongodb数据库。后期将优化爬虫，增加更多的东西，让整个项目变得有趣。

## 运行
### 技术支持

```
git clone https://github.com/wuhuanyu/libCrawler.git
```
机器需要安装Mongodb

### 安装
一些依赖，推荐virtualenv
```
pip install scrapy 
pip install pymongo
```

## 运行
```
scrapy crawl bbc
scrapy crawl medium
scrapy crawl cnn
scrapy crawl mbook
scrapy crawl reuters
```


## Acknowledgments
欢迎Issue，pull,更欢迎加入这个项目！


