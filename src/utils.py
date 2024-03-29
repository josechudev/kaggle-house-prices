import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def preprocess_datasets(train, test):
    
    train.drop('Id', inplace=True, axis=1)
    train.drop('Id', inplace=True, axis=1)
    
def get_numeric_features(df):
    
    return pd.DataFrame(df.select_dtypes(np.number))

def get_cat_features(df):
    
    return pd.DataFrame(df.select_dtypes(include='object'))

def plot_violins(df, n_cols=2, n_rows=7, figsize=(12,8)):
    
    """
    df: DataFrame to plot
    n_cols: Number of columns of plots to display
    n_rows: Number of rows of plots to display
    figsize: figsize of the plots
    """
    cols = get_numeric_features(df).columns
    n_cols = 2
    n_rows = 7

    for i in range(n_rows):
        fg, ax = plt.subplots(nrows=1, ncols=n_cols, figsize=(12,8))

        for j in range(n_cols):
            sns.violinplot(y=cols[i*n_cols+j], data=df, ax=ax[j])
            
def get_high_correlations(df, size=15, threshold=0.5):
    data_corr = get_numeric_features(df).corr()
    cols = data_corr.columns
    corr_list = []

    #Search for the highly correlated pairs
    for i in range(0,size): #for 'size' features
        for j in range(i+1,size): #avoid repetition
            if (data_corr.iloc[i,j] >= threshold and data_corr.iloc[i,j] < 1) or (data_corr.iloc[i,j] < 0 and data_corr.iloc[i,j] <= -threshold):
                corr_list.append([data_corr.iloc[i,j],i,j]) #store correlation and columns index

    #Sort to show higher ones first            
    s_corr_list = sorted(corr_list,key=lambda x: -abs(x[0]))

    #Print correlations and column names
    for v,i,j in s_corr_list:
        print ("%s and %s = %.2f" % (cols[i],cols[j],v))
    
    return s_corr_list

def plot_high_correlations(df, size=15, threshold=0.5):
    
    data_corr = get_numeric_features(df).corr()
    cols = data_corr.columns
    s_corr_list = get_high_correlations(df, size=15, threshold=threshold)
    
    for v,i,j in s_corr_list:
        sns.pairplot(df, size=6, x_vars=cols[i],y_vars=cols[j] )
        plt.show()
        
def plot_categorical_hist(df, n_cols=4, n_rows=10, figsize=(12,8)):
    
    
    cols = df.select_dtypes(exclude=np.number).columns

    #Plot count plot for all attributes in a 29x4 grid
    for i in range(n_rows):
        fg,ax = plt.subplots(nrows=1,ncols=n_cols,sharey=True,figsize=figsize)
        for j in range(n_cols):
            sns.countplot(x=cols[i*n_cols+j], data=df, ax=ax[j])
            
def count_missing(df):
    
    total = df.isnull().sum().sort_values(ascending=False)
    percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
    missing_data = pd.concat([total, percent], keys=['Total', 'Percent'], axis=1)
    return missing_data