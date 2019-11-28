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

    def dollarsToDigits(self, s):
        """
        Converts the string representation of a budget into a float

        :param s: String to convert
        :return s: A float version of the string
        """
        try:
            s = s.replace('$', '')
        except AttributeError:
            # In the event that the value is NaN
            return(0)
        s = s.replace(',', '')
        return(float(s))

    def percents_to_floats(self, s):
        """
        Converts the string representation of a float into a decimal
        representation of a float

        :param s: string float to convert
        :return: A float version of the string

        >>> percents_to_floats('%9')
            0.09 # As float
        """
        try:
            s = s.replace('%', '')
        except AttributeError:
            # In the event that the value is NaN
            return(0)
        return(float(s) / 100)

    def imputer(self, col, miss_value=np.NaN, strat='median'):
        """
        Runs an imputation strategy of the user's choice and assigns that back
        to the column, replacing all missing values

        :param col: The column to do conduct imputation on
        :param miss_val: The missing value that will be replaced through
            imputation
        :param strat: The strategy to use to replace the missing value
        """
        imputed_col = SimpleImputer(missing_values=miss_value, strategy=strat)
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
