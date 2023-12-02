import datetime
import re

import chinese_calendar
import holidays
import pandas as pd
from chinese_calendar import is_holiday
from zhdate import ZhDate

cn_holidays = dict()
for dt, name in sorted(
    holidays.CN(years=[2020, 2021, 2022, 2023, 2024], language="zh_CN").items()
):
    cn_holidays.update({dt: name})


def generate_calendar(start_date, end_date):
    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame({"日期": dates})

    df["年"] = df["日期"].dt.year
    df["季"] = df["日期"].dt.quarter
    df["月"] = df["日期"].dt.month
    df["日"] = df["日期"].dt.day

    df["年度名称"] = "Y" + df["日期"].dt.year.astype(str)
    df["季度名称"] = "Q" + df["季"].astype(str)
    df["年度季度"] = df["年度名称"] + df["季度名称"]
    df["年季编号"] = 10 * df["年"] + df["季"]

    df["月份名称"] = df["日期"].dt.month_name(locale="zh_CN")
    df["英文月份"] = df["日期"].dt.month_name(locale="en_US")
    df["年度月份"] = df["年"] * 100 + df["月"]

    df["年月编号"] = (df["年"] - df["年"].min()) * 12 + df["月"]
    df["年度第几日"] = df["日期"].dt.date.apply(
        lambda x: (x - datetime.date(x.year, 1, 1)).days + 1
    )

    days = {
        0: "星期一",
        1: "星期二",
        2: "星期三",
        3: "星期四",
        4: "星期五",
        5: "星期六",
        6: "星期日",
    }
    df["星期编号"] = df["日期"].dt.dayofweek.map(days)
    df["星期英文"] = df["日期"].dt.day_name(locale="en_US")

    df["年度第几周"] = df["日期"].dt.date.apply(lambda x: get_week_num(x))

    df["周编号"] = "W" + df["年度第几周"].astype(str)
    df["年周"] = df["年"].astype(str) + df["周编号"]
    df["日期编码"] = df["日期"].apply(lambda x: x.strftime("%Y%m%d"))

    df["CN节假日判断"] = df["日期"].dt.date.apply(
        lambda x: "是" if is_holiday(x) else "否"
    )
    # df["CN节假日名称1"] = df["日期"].dt.date.apply(
    #     lambda x: cn_holidays.get(x) if is_holiday(x) else "工作日"
    # )
    # on_holiday, holiday_name = calendar.get_holiday_detail(april_last)
    en_to_cn = {
        "New Year's Day": "元旦",
        "Spring Festival": "春节",
        "Tomb-sweeping Day": "清明节",
        "Labour Day": "劳动节",
        "Dragon Boat Festival": "端午节",
        "Mid-Autumn Festival": "中秋节",
        "National Day": "国庆节",
    }
    df["CN节假日名称"] = df["日期"].dt.date.apply(
        lambda x: en_to_cn.get(chinese_calendar.get_holiday_detail(x)[1], "周末")
        if is_holiday(x)
        else "工作日"
    )
    df["农历日期"] = df["日期"].dt.date.apply(
        lambda x: ZhDate.from_datetime(pd.to_datetime(x)).chinese()
    )
    df["农历年"] = df["农历日期"].apply(extract_year_content)
    df["农历月日"] = df["农历日期"].apply(extract_content)

    return df


def extract_year_content(text: str) -> str:
    pattern = re.compile(r"(\w+[零一二三四五六七八九]年)(.*?) ")
    result = pattern.search(text)
    if result:
        return result.group(1)
    else:
        return ""


# 定义提取函数
def extract_content(text: str) -> str:
    pattern = re.compile(r"(二零二[零一二三四五六七八九]年)(.*?) ")
    result = pattern.search(text)
    if result:
        return result.group(2)
    else:
        return ""


def get_week_num(date: datetime.date):
    """计算指定日期属于当年的第几周"""
    first_day = datetime.date(date.year, 1, 1)
    if first_day.weekday() <= date.weekday():
        return (date - first_day).days // 7 + 1
    else:
        return (date - first_day).days // 7 + 2


start_date = "2022-01-01"
end_date = "2024-12-31"

df = generate_calendar(start_date, end_date)
df.to_csv("日期表.csv", index=False)
# TO EXCEL
# df.to_excel("日期表处理/日期表.xlsx", index=False)
