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
    group_cols = st.multiselect("グループ変数の選択",feature_cols)
    rank_cols = st.multiselect("頻度を表示させる役の選択",utils.rank_list)
    threshold = st.number_input(label="サンプルの閾値",min_value=0,max_value=100,value=10,step=1)
    action_threshold = st.number_input(label="アクションの閾値",min_value=0,max_value=10,value=2,step=1)
    submit = st.form_submit_button(label="実行")

if submit: 
    mean_cols = utils.get_rank_action_col(action_cols,rank_cols)

    dfg = aggregation.calculate_group_means(df,group_cols,mean_cols)
    dfg = dfg[dfg["count"] >= threshold]
    dfg = dfg.dropna(subset=mean_cols,how="all")
    dfg = dfg.round(1)

    filtered_dfg = aggregation.filter_below_threshold(dfg,mean_cols,2)
    
    dfg.columns = dfg.columns.str.replace("freq", "")
    filtered_dfg.columns = filtered_dfg.columns.str.replace("freq", "")

    st.subheader("グループ化データ")
    st.dataframe(dfg)

    st.subheader("低頻度アクション一覧")
    st.dataframe(filtered_dfg)