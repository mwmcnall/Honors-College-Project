import pandas as pd
import numpy as np

class DataContainer:
    """
    A wrapper class for the pandas DataFrame data type. Contains methods
    designed to explore a DataFrame
    """
    def __init__(self, df, **kwargs):
        """
        Constructor class for DataContainer
        """
        self.df = df

        return


    def data_object_col_merge(self, data_object, merge_col, on):
        """
        Merges one column from the self.dis.df DataFrame to the main self.df
        DataFrame
        """
        self.df = self.df.merge(right=pd.DataFrame(data_object.df[merge_col]),
            on=on)
        return


    def _column_bin(self, **kwargs):
        """
        Generates categorical columns based on numerical values, automatically
        splitting based on inputted bin size

        :param new_col: The new column to create
        :param bin_size: The number of bins to separate the data into
        :param labels: The labels to assign to each newly created bin
        """
        # assert len(kwargs['labels']) == kwargs['bin_size'], ("You must assign"
        #     "the same number of labels as the number of bins you are creating")
        self.df[kwargs['new_col']] = pd.cut(self.df[kwargs['cut_col']],
                                            kwargs['bin_size'],
                                            labels=kwargs['labels'])
        return

    def _column_div(self, **kwargs):
        """
        Generates columns through division based on a numerator and
        denominator column

        :param new_col: The new column to create
        :param div_top: The numerator of the division call
        :param div_bot: The denominator of the division call
        """
        self.df[kwargs['new_col']] = (self.df[kwargs['div_top']] /
                                      self.df[kwargs['div_bot']]).fillna(0)

        return

    def corr_one_col(self, col, low_bound = -1, high_bound = 1):
        """
        Returns the correlations between one column and the rest of the columns
        in the dataset
        :param col: The column to get the correlation of
        :param low_bound: Only returns correlations greater than this bound
        :param high_bound: Only returns correlations lower than this bound
        """
        corr = self.df.corr()[col].sort_values()
        corr = corr[corr > low_bound]
        corr = corr[corr < high_bound]
        return corr

    def nans(self, threshold=0, silence=False):
        """
        Shows the number of NaN values per column if the parameter silence is
        False. Will always return the columns that have more NaN values than
        the threshold

        :param threshold: The number of NaNs is compared to this and will will
            return / print the columns greater than this threshold
        :param silence: Whether or not to print the columns and number of NaNs
            to console
        :return: A list of columns that have more NaNs than the threshold

        >>> Data.nans(threshold = 100)
            # Lines printed
            Adjusted Grade: 1270 null values
            New?: 1245 null values
            Other Location Code in LCGMS: 1271 null values
            School Income Estimate: 396 null values

            # List returned
            ['Adjusted Grade',
             'New?',
             'Other Location Code in LCGMS',
             'School Income Estimate']
        """

        return_list = []
        for (col_name, col_data) in self.df.iteritems():
            nan = self.df[col_name].isnull().sum()
            if nan > threshold:
                if silence is False:
                    print(col_name + ": %d null values" % nan)
                return_list.append(col_name)
        return return_list

    def drop_cols(self, col_list):
        """
        Takes in a list of columns and drops them, in-place

        :param col_list: A list of columns to drop
        :return: Nothing, the operation happens in-place

        """
        # axis = 1 represents dropping from columns. 0 would be index
        self.df.drop(col_list, axis=1, inplace=True)

        return

    def dict_fun_run(self, dic, fun):
        """
        Iterates a function over a nested dictionary of dictionaries

        :param dict: Takes a nested dictionary in this form.
            {1:{'fizz':'buzz'}, 2:{'buzz':'fizz'}}
        :return: Nothing, just runs the given function over the items in the
            dictionary
        """
        for item in dic.items():
            fun(**item[1])

        return

    def lol_to_set(self, col, splitby):
        """
        Converts a column of list of lists to a set of unique values

        :param col: The column of the dataframe to reduce
        :splitby: The character
        """
        return set([j for sub in
                   [i.split(splitby) for i in
                    self.df[col].values.tolist()]
                    for j in sub])
