import pandas as pd
from db import get_all

def user_stats(user):
    data = get_all()

    if not data:
        return "No Data"

    # IMPORTANT FIX (avoid crash)
    df = pd.DataFrame(data)
    
    if df.shape[1] == 5:
        df.columns = ["user","exercise","reps","cal","date"]
    else:
        return "Database Error"

    df = df[df["user"] == user]

    if df.empty:
        return "No Data"

    return f"""
Workouts: {len(df)}
Reps: {df['reps'].sum()}
Calories: {df['cal'].sum()}
"""

def weekly(user):
    data = get_all()

    if not data:
        return pd.Series()

    df = pd.DataFrame(data)

    if df.shape[1] != 5:
        return pd.Series()

    df.columns = ["user","exercise","reps","cal","date"]

    df["date"] = pd.to_datetime(df["date"])
    df = df[df["user"] == user]

    return df.groupby(df["date"].dt.date)["cal"].sum()