这是一个小的python程序，功能是实现命令行对于火车票余票的查询
--------
```python
Usage:
    ticket [-gkzdt] <from> <to> <date>

Options:
    -h,-help: 显示帮助菜单
    -g: 高铁
    -k: 普快
    -z: 直达
    -d: 动车
    -t: 特快
Example:
   ticket -g 北京 上海 2017-1-20
