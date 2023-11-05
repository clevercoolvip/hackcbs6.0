import pandas as pd
import numpy as np
import seaborn as sns
import statistics as st
import matplotlib.pyplot as plt

#<-------------------------- Dataframe -------------------------->
def removenan(df):
    """
    Param1: pandas dataframe

    return: pandas dataframe
    """
    df.dropna(inplace=True)
    return df


def dropallunique(df):
    for col in df.columns:
        l = len(df[col])
        ll = len(pd.unique(df[col]))
        if l==ll:
            df.drop(columns=[col], inplace=True)
    return df


#<-------------------------- Columns -------------------------->
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


def check_dtype(col):
    """
    Param1: pandas series

    return: Boolean
    """
    df = pd.DataFrame(col)
    df = df.squeeze()
    dtype = col.dtype
    if dtype=="float64" or dtype=="int64":
        return True
    else:
        return False


def mean(col):
    """
    Param1: pandas series

    return: int
    """
    if check_dtype(col):
        return np.mean(col)
    return -1


def median(col):
    """
    Param1: pandas series

    return: int
    """
    if check_dtype(col):
        return np.median(col)
    return -1


def std(col):
    """
    Param1: pandas series

    return: int
    """
    if check_dtype(col):
        return st.stdev(col)
    return -1
    

def removeOutlier(col):
    """
    Param1: pandas series

    return: pandas dataframe
    """
    if check_dtype(col):
        init_thresh = mean(col) - 3*std(col)
        final_thresh = mean(col) + 3*std(col)
        print(init_thresh)
        print(final_thresh)
        df = pd.DataFrame(col, columns=["col1"])
        return df[(df.col1>init_thresh) & (df.col1<final_thresh)]
    return -1



def column_description(col):
    """
    Param1: pandas series

    return: dictionary/JSON
    """

    json = {
        "Datatype":{type(col)},
        "Description":pd.DataFrame(col).describe(),
    }
    return json


def domains(col):
    """
    Param1: pandas series

    return: dictionary/JSON
    """
    json = {
        "Minimum": min(col.to_list()),
        "Maximum":max(col.to_list())
    }
    return json


def correlation_between(col1, col2):
    """
    Param1: pandas.DataFrame/series
    Param2: panda.DataFrame/series

    return: correlation

    Interpretation: 
        0 - no correlation
        1 - directly proportional
        -1 - indirectly proportional
    """
    results = col1.corr(col2)
    return results


def diversity_in_percentage(col):
    """
    Param1: pd.DataFrame/series

    Return: {
        column_name: name of the column
        diverse: percentage of diversity (percentage of values in column having values between val_range)
        val_range: [mean-st, mean+st] 
    }

    Interpretation: % of values in col having values between [mean-std, mean+std]
    """
    x_bar = mean(col)
    st = std(col)
    n = len(col)
    count = 0
    for i in col:
        ab = abs(x_bar-i)
        if ab<=st:
            count+=1
    return {
        "diverse": int((count/n)*100),
        "val_range": [x_bar-st, x_bar+st]
    }


#<--------------------- Plot ------------------>
def regplot(df, col1, col2):
    sns.regplot(data=df, x=col1, y=col2)
    plt.show()


def uniques_bar_graph(col):
    """
    Param1: pandas series

    return: seaborn plot
    """

    # if check_dtype(col) == False:
    unq_len = len(pd.unique(col))
    print(f"Unique Values: {unq_len}")
    if unq_len<20:
        sns.countplot(data=col, x=col, hue=col, )
        plt.savefig("fig.svg", format="svg")
        plt.show()
    else:
        pass
    return -1


#<----------------------------- Main ------------------------>
if __name__=="__main__":
    path2 = "train.csv"
    df = pd.read_csv(path2)
    removenan(df)
    req=[]
    for col in df.columns:
        if check_dtype(df[col]):
            req.append(col)
    
    print(req)
    print(correlation_between(df[req[0]], df[req[1]]))
    print("<------------>")
    print(diversity_in_percentage(df.Age))
    print(df.head())