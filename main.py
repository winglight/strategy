import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import requests
import base64

headers = {
    'User-Agent': 'PostmanRuntime/7.28.1',
    'Accept': '*/*',  # This is another valid field
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

import jqdatasdk
jqdatasdk.auth("15015987150", "XHy9Py9ELfzd")

#侧栏显示策略条件
selected_date = st.sidebar.date_input("选择日期")
creteria = st.sidebar.selectbox(
    '策略条件',
     ["{}9点30分成交金额；{}9点30分涨幅；{}9点31分成交金额；{}9点31分涨跌幅；{}9点31分涨跌幅>={}9点30分涨跌幅；非创业板；非科创板，非st股", 
        "{}9点30分成交金额；{}9点30分涨幅；{}9点31分成交金额；{}9点31分涨跌幅；非创业板；非科创板，非st股"])
# sort = st.sidebar.selectbox(
#     '排序字段',
#      ["9点30分成交额排序", "9点30分成交额反序"])

# st.dataframe(df)

def reshape(df):
    # print(df)
    return1 = (df["close"].iloc[1] - df["close"].iloc[0])/df["close"].iloc[0]
    return2 = (df["close"].iloc[2] - df["close"].iloc[1])/df["close"].iloc[1]
    # vol1 = (df["money"].iloc[1] - df["money"].iloc[0])/df["money"].iloc[0]
    # vol2 = (df["money"].iloc[2] - df["money"].iloc[1])/df["money"].iloc[1]
    # print(df["code"].iloc[0], return1, return2, vol1, vol2)
    res = pd.DataFrame({"code": df["code"].iloc[0], "9:30涨幅": return1, "9:31涨幅": return2, "9:30成交额": df["money"].iloc[1], "9:31成交额": df["money"].iloc[2]}, index=[0])
    res.set_index("code")
    return res

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    date = selected_date.strftime("%Y年%m月%d日")
    csv = df.to_csv(index=False, encoding='utf-8')
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="{date}.csv">导出csv文件</a>'

@st.cache 
def req_strategy(strategy):
    url = "http://m.iwencai.com/wap/search?w={}&source=phone&queryarea=all&tid=stockpick&perpage=1000"
    res = requests.get(url.format(strategy), headers=headers)
    return res.json()

@st.cache 
def get_stock_list(date):
    res = jqdatasdk.get_all_securities()
    res['code'] = res.index
    res = res.loc[
                (~res.display_name.str.contains('ST', na=False)) &
                (~res.display_name.str.contains("退", na=False)) &
                (~res.code.str.startswith("300", na=False)) &
                (~res.code.str.startswith("688", na=False))]
    return res['code'].tolist()

@st.cache 
def get_stats_by_date(date):
    last_date = jqdatasdk.get_trade_days(end_date=date, count=2)[0].strftime("%Y-%m-%d")
    stock_list = get_stock_list(date)
    df = jqdatasdk.get_price(stock_list, frequency="1m", start_date=last_date + " 15:0:00", end_date=date + " 09:32:00")
    # print(df)
    df = df.groupby("code").apply(reshape)
    return df

def get_stocks_by_strategy():
    date = selected_date.strftime("%Y-%m-%d")
    # strategy = creteria.format(date, date, date, date, date, date)
    # res = req_strategy(strategy)
    
    # df = pd.DataFrame((res.get("xuangu").get("blocks")[0]).get("data").get("result"))
    # columns = (res.get("xuangu").get("blocks")[0]).get("data").get("title")
    # df.columns = list(map(lambda col : str(col), columns))
    # try:
    #     df = df.iloc[:, [0,1,4,5]]
    # except Exception as error:
    #     print(error)
    # print(df)
    df = get_stats_by_date(date)

    st.title('策略')
    st.write('策略条件:', creteria)
    st.write('当前日期',  date)
    st.write(df)
    
    st.markdown(get_table_download_link(df), unsafe_allow_html=True)
    
    
st.sidebar.button('执行策略', on_click=get_stocks_by_strategy)




