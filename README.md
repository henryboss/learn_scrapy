# learnScrapy
  该项目主要记录Scrapy的安装、学习及爬虫案例。

##1、运行环境
系统：win10(64位)
版本：python3.6  
框架：scrapy1.5.0  
##2、安装扩展
扩展下载地址：https://www.lfd.uci.edu/~gohlke/pythonlibs/ 需要根据自己的版本进行选择，分别下载。  
如运行环境一致，也可以通过extension目录进行安装  
```bash
pip3 install Twisted-17.9.0-cp36-cp36m-win_amd64.whl

``` 
然后运行根目录下的文件
```bash
pip3 instlal -r requirements.txt
```  
新建虚拟环境并激活虚拟环境：
```bash
virtualenv --no-site-packeages my_env
my_env/Scripts/activate
```
##3、创建项目
Scrapy文档地址：https://docs.scrapy.org/en/latest/  
在开始爬取之前，您必须创建一个新的Scrapy项目。 进入您打算存储代码的目录中，运行下列命令:  
```bash
scrapy startproject tutorial
``` 
该命令将会创建包含下列内容的 tutorial 目录:    
```bash
tutorial/  
    scrapy.cfg  
    tutorial/  
        __init__.py  
        items.py  
        pipelines.py  
        settings.py  
        spiders/  
            __init__.py  
            ...  
```
这些文件分别是:  

scrapy.cfg: 项目的配置文件  
tutorial/: 该项目的python模块。之后您将在此加入代码。  
tutorial/items.py: 项目中的item文件.  
tutorial/pipelines.py: 项目中的pipelines文件.  
tutorial/settings.py: 项目的设置文件.  
tutorial/spiders/: 放置spider代码的目录.  
##运行第一个spider
第一个项目官方提供的spider，在tutorial/tutorial/spiders下的quotes_spider.py  
```bash
cd tutorial/tutorial
scrapy crawl quotes
```
*如果windows下面没有安装pypiwin32会遇到报错：
```bash
ModuleNotFoundError: No module named 'win32api'
```  
当返回
```bash
2018-02-02 14:36:13 [scrapy.core.engine] INFO: Spider closed (finished)
```
表示成功。