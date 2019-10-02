
def check_column_is_consistent_type(series):
    '''
    test, colType = check_column_is_consistent_type(df[col])
    '''
    row1Type = type(series[0])
    for item in series:
        if type(item) != row1Type:
            return False, None
    return True, row1Type


def split_date_to_bins(df, col, nbins):
    '''
    groupings = split_date_to_bins(df,col,nbins)
    '''
    df['epochDate'] = df[col].apply(lambda x: time.mktime(x))
    df = df.sort_values('epochDate', ascending=False)
    split = np.array_split(df, nbins)
    return split


# split on the col
def sig_crawl(df, col, colsList, max_bins=4):
    '''
    results_df = sig_crawl(df,col,colsList)
    '''
    results_df = pd.DataFrame()
    for testCol in colsList:
        population_mean = df[testCol].mean()
        for n in range(2, max_bins)+[max_bins]:
            groupings = split_date_to_bins(df, col, n)
            sample_means = [grouping[testCol].mean() for grouping in groupings]
            sample_delta = [population_mean-grouping[testCol].mean()
                            for grouping in groupings]
            f_value, p_value = stats.f_oneway(
                *[groupings[X][testCol] for X in range(len(groupings))])
            if p_value < alpha:
                print "Significance at:  Bin=" + str(n) + " p=" + str(p_value) + " comparing="+col + " ; " + testCol
            results_df.loc[n, testCol] = p_value
    return results_df
