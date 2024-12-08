import pandas as pd

rank_list = ["straight flush","4 Cards","full house","flush","straight","3 Cards","2 pairs","over pair","top pair(GK)","top pair(LK)","middle pair","low pair","noting"]
eqb_list = ["EQB"]
exclude_list = rank_list + eqb_list

def get_action_columns(df, exclude_keywords=exclude_list):
    keywords = ["BET", "RAISE", "CALL", "FOLD", "CHECK"]
    exclude_keywords = [kw.lower() for kw in exclude_keywords]

    columns = []
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword.lower() in col_lower for keyword in keywords) and not any(exclude in col_lower for exclude in exclude_keywords):
            columns.append(col)
    
    return columns

def get_feature_columns(df):
    flop_features = ["Flop_high_card","Flop_middle_card","Flop_pair","Flop_suit","Flop_connect"]
    turn_features = ["Turn_card","Turn_pair","Turn_suit","Turn_connect"]
    river_features = ["River_card","River_pair","River_suit","River_connect"]
    
    if "River" in df.columns:
        return flop_features + turn_features + river_features
    if "Turn" in df.columns:
        return flop_features + turn_features
    
    return flop_features

def drop_low_freq_rows(df):
    if "River" in df.columns:
        df = df[df["Global %"] > 0.001]
    else:
        df = df[df["Global %"] > 1]
    return df

def get_rank_action_col(action_cols,rank_cols):
    cols = []
    for r in rank_cols:
        for a in action_cols:
            cols.append(r+a)
    return action_cols + cols