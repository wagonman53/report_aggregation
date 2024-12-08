import pandas as pd

def get_action_columns(df):
    keywords = ["BET","RAISE","CALL","FOLD","CHECK"]

    columns = []
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword.lower() in col_lower for keyword in keywords):
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