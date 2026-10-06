import pandas as pd


def clean_matches(df):
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])

    return df


def clean_deliveries(df):
    df = df.copy()

    df["is_wicket"] = df["is_wicket"].astype(int)

    return df