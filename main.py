import pandas as pd
import streamlit as st
import db
import aggregation
import utils
import categorical_feature

st.set_page_config(layout="wide")

table_list = db.get_table_names()
table_name = st.sidebar.selectbox("テーブルの選択",table_list)

# CSVファイルの読み込み
@st.cache_data
def load_data(table_name):
    df = db.get_table_data(table_name)
    return df
df = load_data(table_name)

df = utils.drop_low_freq_rows(df)

feature_cols = utils.get_feature_columns(df)
action_cols = utils.get_action_columns(df)

df = categorical_feature.get_categorical_feature(df)

with st.sidebar.form(key="form"):
    group_cols = st.multiselect("グループ変数の選択",feature_cols,default=feature_cols[:3])
    mean_cols = st.multiselect("平均値をとるアクションの選択",action_cols,default=action_cols[:3])
    threshold = st.number_input(label="アクションの閾値",min_value=0,max_value=10,value=2,step=1)
    submit = st.form_submit_button(label="更新")

if submit:
    dfg = aggregation.calculate_group_means(df,group_cols,mean_cols)
    dfg = dfg.dropna(subset=mean_cols,how="all")
    dfg = dfg.round(1)

    st.subheader("グループ化データ")
    st.dataframe(dfg)

    st.subheader("低頻度アクション一覧")
    filtered_dfg = aggregation.filter_below_threshold(dfg,mean_cols,2)
    st.dataframe(filtered_dfg)