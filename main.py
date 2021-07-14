import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import requests

headers = {
    'User-Agent': 'PostmanRuntime/7.28.1',
    'Accept': '*/*',  # This is another valid field
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}
global df
df = pd.DataFrame()
st.title('策略')

#侧栏显示策略条件
selected_date = st.sidebar.date_input("选择日期")
creteria = st.sidebar.selectbox(
    '策略条件',
     ["9点30分成交额；开盘涨幅"])
# sort = st.sidebar.selectbox(
#     '排序字段',
#      ["9点30分成交额排序", "9点30分成交额反序"])
'策略条件:', creteria
'当前日期',  selected_date
# st.dataframe(df)

@st.cache 
def req_strategy(strategy):
    url = "http://m.iwencai.com/wap/search?w={}&source=phone&queryarea=all&tid=stockpick&perpage=20"
    res = requests.get(url.format(strategy), headers=headers)
    return res.json()

def get_stocks_by_strategy():
    strategy = selected_date.strftime("%Y-%m-%d") + " " + creteria
    res = req_strategy(strategy)
    print(res)
    
    global df
    df = pd.DataFrame((res.get("xuangu").get("blocks")[0]).get("data").get("result"))
    columns = (res.get("xuangu").get("blocks")[0]).get("data").get("title")
    df.columns = list(map(lambda col : str(col), columns))
    # print(df)
    # global stdf
    st.write(df, )
    
st.sidebar.button('执行策略', on_click=get_stocks_by_strategy)




