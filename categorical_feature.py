import collections
import pandas as pd
from pandas.api.types import CategoricalDtype

card_num = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

def flop_high_card(x):
    f = list(x.replace(" ", ""))
    cn = [card_num[f[0]], card_num[f[2]], card_num[f[4]]]
    qt = [12,11,10]
    if max(cn) == 14:
        return "A"
    elif max(cn) == 13:
        return "K"
    elif max(cn) in qt:
        return "Q-T"
    else:
        return "9-2"
    

def flop_middle_card(x):
    f = list(x.replace(" ", ""))
    cn = [card_num[f[0]], card_num[f[2]], card_num[f[4]]]
    cns = sorted(cn, reverse=True)
    cn = cns[1]
    qt = [12,11,10]
    if cn == 14:
        return "A"
    elif cn == 13:
        return "K"
    elif cn in qt:
        return "Q-T"
    else:
        return "9-2"


def turn_card(x):
    f = list(x.replace(" ", ""))
    cn = card_num[f[6]]
    qt = [12,11,10]
    if cn == 14:
        return "A"
    elif cn == 13:
        return "K"
    elif cn in qt:
        return "Q-T"
    else:
        return "9-2"


def river_card(x):
    f = list(x.replace(" ", ""))
    cn = card_num[f[8]]
    qt = [12,11,10]
    if cn == 14:
        return "A"
    elif cn == 13:
        return "K"
    elif cn in qt:
        return "Q-T"
    else:
        return "9-2"


def flop_pair_card(x):
    x = list(x.replace(" ", ""))
    n = [card_num[x[0]], card_num[x[2]], card_num[x[4]]]
    nc = collections.Counter(n).most_common()
    pc = nc[0][0]
    qt = [12,11,10]
    
    if nc[0][1] >= 2:
        if pc == 14:
            return "A"
        if pc == 13:
            return "K"
        if pc in qt:
            return "Q-T"
        return "9-2"
    return "No pair"


def turn_pair_card(x):
    x = list(x.replace(" ", ""))
    n = [card_num[x[0]], card_num[x[2]], card_num[x[4]], card_num[x[6]]]
    nc = collections.Counter(n).most_common()
    pc = nc[0][0]
    qt = [12,11,10]
    
    if nc[0][1] >= 2:
        if pc == 14:
            return "A"
        if pc == 13:
            return "K"
        if pc in qt:
            return "Q-T"
        return "9-2"
    return "No pair"


def river_pair_card(x):
    x = list(x.replace(" ", ""))
    n = [card_num[x[0]], card_num[x[2]], card_num[x[4]], card_num[x[6]], card_num[x[8]]]
    nc = collections.Counter(n).most_common()
    pc = nc[0][0]
    qt = [12,11,10]
    
    if nc[0][1] >= 2:
        if pc == 14:
            return "A"
        if pc == 13:
            return "K"
        if pc in qt:
            return "Q-T"
        return "9-2"
    return "No pair"
    

def get_categorical_feature(df):
    df["Flop_high_card"] = df["Community card"].map(flop_high_card)
    df["Flop_middle_card"] = df["Community card"].map(flop_middle_card)
    df["Flop_pair"] = df["Community card"].map(flop_pair_card)

    rank_order = ["A","K","Q-T","9-2"]
    rank_order = CategoricalDtype(categories=rank_order, ordered=True)
    pair_order = ["A","K","Q-T","9-2","No pair"]
    pair_order = CategoricalDtype(categories=pair_order, ordered=True)

    df["Flop_high_card"] = df["Flop_high_card"].astype(rank_order)
    df["Flop_middle_card"] = df["Flop_middle_card"].astype(rank_order)
    df["Flop_pair"] = df["Flop_pair"].astype(pair_order)

    df["Flop_connect"] = df["Flop_connect"].replace({0: 'No connect', 1: 'connect'})

    if "Turn" in df.columns:
        df["Turn_card"] = df["Community card"].map(turn_card)
        df["Turn_pair"] = df["Community card"].map(turn_pair_card)
        df["Turn_card"] = df["Turn_card"].astype(rank_order)
        df["Turn_pair"] = df["Turn_pair"].astype(pair_order)
        df["Turn_connect"] = df["Turn_connect"].replace({0: 'No connect', 1: 'connect'})
    if "River" in df.columns:
        df["River_card"] = df["Community card"].map(river_card)
        df["River_pair"] = df["Community card"].map(river_pair_card)
        df["River_card"] = df["River_card"].astype(rank_order)
        df["Turn_pair"] = df["Turn_pair"].astype(pair_order)
        df["River_connect"] = df["River_connect"].replace({0: 'No connect', 1: 'connect'})

    return df
