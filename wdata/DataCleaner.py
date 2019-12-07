from .DataContainer import DataContainer
from sklearn.impute import SimpleImputer
import numpy as np

class DataCleaner(DataContainer):
    """
    A class that inherits from DataContainer, designed to use methods to help
    clean data
    """
    def __init__(self, df,**kwargs):
        super().__init__(df, **kwargs)
        # An anonymous function that can be used to get back the most
        # common value in a categorical column
        self.com_fun = lambda x:x.value_counts().index[0]

    def dollarsToDigits(self, string):
        """
        Converts the string representation of a budget into a float

        :param s: String to convert
        :return s: A float version of the string
        """
        try:
            string = string.replace('$', '')
        except AttributeError:
            # In the event that the value is NaN
            return(0)
        string = string.replace(',', '')
        return(float(string))

    def normalize_column(self, col, invert=False):
        """
        Takes a column for the self.df DataFrame and returns the normalized
        column for it from 0 to 1

        :param col: Column in df to normalize
        :param invert: Return 1 - the normalized values
        :return: Normalized column values
        """
        col_min = self.df[col].min()
        temp = (self.df[col].values - col_min) / \
            (self.df[col].max() - col_min)
        if not invert:
            return temp
        return 1 - temp

    def normalize_column_filter(self, col, greater_than=None,
        less_than=None, invert = False, subset=None):
        """
        Takes a column for the self.df DataFrame and returns the normalized
        column for it from 0 to 1

        :param col: Column in df to normalize
        :param invert: Return 1 - the normalized values
        :param greater_than: Normalizes values greater than or equal to
            this value
        :param less_than: Normalizes values less than or equal to this value
        :return: Normalized column values
        """
        greater_than, less_than = self._set_greater_less_than(col, greater_than,
            less_than)
        if subset==None:
            subset = self.df[(self.df[col] >= greater_than )& \
                (self.df[col] <= less_than)][col]
        col_min = subset.min()
        temp = (subset.values - col_min) / \
            (subset.max() - col_min)
        if not invert:
            return temp
        return 1 - temp

    def _set_greater_less_than(self, col, greater_than=None, less_than=None):
        """
        Sets greater than / less than bounds
        """
        if greater_than == None:
            greater_than = self.df[col].max()
        if less_than == None:
            less_than = self.df[col].max()
        return greater_than, less_than

    def percents_to_floats(self, string):
        """
        Converts the string representation of a float into a decimal
        representation of a float

        :param s: string float to convert
        :return: A float version of the string

        >>> percents_to_floats('%9')
            0.09 # As float
        """
        try:
            string = string.replace('%', '')
        except AttributeError:
            # In the event that the value is NaN
            return(0)
        return(float(string) / 100)

    def imputer(self, col, miss_value=np.NaN, strat='median'):
        """
        Runs an imputation strategy of the user's choice and assigns that back
        to the column, replacing all missing values

        :param col: The column to do conduct imputation on
        :param miss_val: The missing value that will be replaced through
            imputation
        :param strat: The strategy to use to replace the missing value
        """
        imputed_col = SimpleImputer(missing_values=miss_value,
                                    strategy=strat)
        imputed_col.fit(self.df[[col]])
        self.df[col] = imputed_col.transform(self.df[[col]])

        return

    def cat_impute(self, col):
        """
        Imputes a categorical value with the most likely candidate

        :param col: The categorical column to replace with the most
            likely value
        """
        self.df[col] = self.df[col].fillna(self.df[col].mode().iloc[0])

        return
