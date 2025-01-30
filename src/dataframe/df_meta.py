import pandas as pd
import numpy as np

def get_datatype_info(
        dataframe_col, dataframe_dtype, 
        statstype=['unique','max','min','sum','mean']):
    ''' collect stats of columns'''

    col_stats = np.full((len(statstype)),np.nan).tolist()
    # stats of numeric and float data types
    for idx, stat in enumerate(statstype):
        if dataframe_dtype in \
            ['object', 'bool']:
            if stat == 'unique': col_stats[idx] = dataframe_col.unique().size
        elif dataframe_dtype in \
            ['datetime64[ns]', 'timedelta64[ns]']:
            if stat == 'unique': col_stats[idx] = dataframe_col.unique().size
            if stat == 'min': col_stats[idx] = dataframe_col.min()
            if stat == 'max': col_stats[idx] = dataframe_col.max()
        elif dataframe_dtype in \
            ['float64', 'int64']:
            if stat == 'min': col_stats[idx] = dataframe_col.min()
            if stat == 'max': col_stats[idx] = dataframe_col.max()
            if stat == 'sum': col_stats[idx] = dataframe_col.sum()
            if stat == 'mean': col_stats[idx] = dataframe_col.mean() 

    return tuple(col_stats)


def get_dataframe_info(dataframe):
    '''
        function collects the dataframe info and results back dataframe with
        column stats, location of dataset and dataframe name
    '''

    # create empty data frame to save the stats and initialize with NA
    types_df = pd.DataFrame(dataframe.dtypes)
    nulls_df = dataframe.count()
    stats_df = pd.concat([types_df, nulls_df], axis=1).reset_index()
    stats_df.columns = ["COLUMNS","DTYPE","COUNT_NONNULL"]
    stats_df.loc[:, ['UNIQUE', 'MIN', 'MAX', 'SUM', 'MEAN']] = np.nan

    # collect the data frame column stats
    stats_df[['UNIQUE', 'MAX', 'MIN', 'SUM', 'MEAN']] = \
        stats_df.apply(
            lambda row: get_datatype_info(
                dataframe_col=dataframe[row['COLUMNS']],
                dataframe_dtype=row['DTYPE']
        ), axis=1, result_type="expand")

    return stats_df