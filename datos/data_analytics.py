import pandas as pd
import numpy as np
import statistics as st
import matplotlib.pyplot as plt
import seaborn as sns

path = "train.csv"
data = pd.read_csv(path)
print(data.head())
print()

def dropallunique(df):
    for col in df.columns:
        l = len(df[col])
        ll = len(pd.unique(df[col]))
        if l==ll:
            df.drop(columns=[col], inplace=True)
    return df


def mean(col):
    return st.mean(col)

def std(col):
    return st.stdev(col)

def skewness(col):
    """
    Param1: pandas dataframe

    return: int

    inference:
    return>0 -> rightly skewed(right distortion)
    return<0 -> left skewed(left distortion)
    """

    mn = mean(col)
    s = std(col)
    n = len(col)
    a=0
    for i in col:
        a+=(i-mn)**3
    return a/((n-1)*(s**3))


def kurtosis(col):
    """
    Used in finance:A large kurtosis is associated with a high risk for an investment because 
    it indicates high probabilities of extremely large and extremely small returns.
    """
    n=len(col)
    avg = mean(col)
    num = 0
    denom = 0
    for i in col:
        num+=(i-avg)**4
        denom+=(i-avg**2)**4

    return n*(num/denom)


def uniqueness(df, col):
    """
    Param1: dataframe
    Param2: column of dataframe

    return: matplotlib countplot
    """
    unique_values = len(pd.unique(col))
    if unique_values<20:
        print(col.value_counts())
        sns.countplot(data=df, x=col)
        plt.show()


def regplot(df, col1, col2):
    sns.regplot(data=df, x=col1, y=col2)
    plt.show()



df1 = dropallunique(data)
print(df1.head())

regplot(df1, df1.iloc[:, 1], df1.iloc[:, 0])