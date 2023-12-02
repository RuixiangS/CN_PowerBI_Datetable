# CN_PowerBI_Datetable
## Description
Through python, you can generate a PowerBI date table suitable for use in China, which not only supports the regular year, season, month, week and day dimensions, but also supports holidays (distinguishing legal holidays and regular weekends) and lunar calendar judgments.
## 中文简介
经过Python编程，可以自动生成适用于中国的PowerBI日期表，该表不仅支持常规的年、季、月、周和日维度，还能够准确区分法定假日和常规周末，并且能够进行农历判断。

目前支持2004——2024年的日期表的全面维度生成，2025年之后的节假日信息待后续chinesecalendar维护后会自动更新
## 安装依赖 Install requirements
```bash
pip install -r requirements.txt
```
## 运行 Run
```python
python BI日期表生成.py
```
接下来就可以把日期表.csv导入到PowerBI使用了
## 特别感谢 Special thanks
[pandas](https://github.com/pandas-dev/pandas)——强大的数据处理、分析库

[chinesecalendar](https://github.com/LKI/chinese-calendar)——中国专用日期库,支持节假日判断

[holidays](https://github.com/vacanza/python-holidays)——非常全面的日期库(甚至支持金融方向),但是不如chinesecalendar使用简单

[zhdate](https://github.com/CutePandaSh/zhdate)——中国农历库