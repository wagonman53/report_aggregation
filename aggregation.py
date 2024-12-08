import pandas as pd
from typing import List

def calculate_group_means(df: pd.DataFrame, group_cols: List[str], mean_cols: List[str]) -> pd.DataFrame:
    result = df.groupby(group_cols)[mean_cols].mean().reset_index()
    group_sizes = df.groupby(group_cols).size().reset_index(name="count")
    total_rows = len(df)
    group_sizes["frequency"] = (group_sizes["count"] / total_rows) * 100
    result = result.merge(group_sizes, on=group_cols)
    
    return result


def filter_below_threshold(df: pd.DataFrame, columns: list, threshold: float) -> pd.DataFrame:
    mask = df[columns].lt(threshold).any(axis=1)
    return df[mask]