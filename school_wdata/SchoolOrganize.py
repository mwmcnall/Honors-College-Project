from wdata import Data
import numpy as np

class SchoolOrganize(Data):
    """
    A Data Class to store organizational methods for SchoolData and free up
    some space in the SchoolData class
    """
    def __init__(self, df, **kwargs):
        super().__init__(df,**kwargs)
        self._sum_dict = {
            1: {'new_col': 'Students Tested Total', 'subject': 'both',
                'students': 'All Students', 'test': True},
            2: {'new_col': 'Student Tested 4s', 'subject': 'both',
                'students': 'All Students', 'test': False},
            3: {'new_col': 'Math Tested Total', 'subject': 'Math',
                'students': 'All Students', 'test': True},
            4: {'new_col': 'Math Tested 4s', 'subject': 'Math',
                'students': 'All Students', 'test': False},
            5: {'new_col': 'ELA Tested Total', 'subject': 'ELA',
                'students': 'All Students', 'test': True},
            6: {'new_col': 'ELA Tested 4s', 'subject': 'ELA',
                'students': 'All Students', 'test': False},
            7: {'new_col': 'White Students Total', 'subject': 'both',
                'students': 'White', 'test': False},
            8: {'new_col': 'Asian / Pacific Islanders Students Total',
                'subject': 'both', 'students': 'Asian', 'test': False},
            9: {'new_col': 'Black Students Total', 'subject': 'both',
                'students': 'Black', 'test': False},
            10: {'new_col': 'Hispanic / Latino Students Total',
                 'subject': 'both', 'students': 'Hispanic', 'test': False},
            11: {'new_col': 'American Indian / Alaska Native Students Total',
                 'subject': 'both', 'students': 'American', 'test': False},
            12: {'new_col': 'Multiracial Students Total', 'subject': 'both',
                 'students': 'Multiracial', 'test': False},
            13: {'new_col': 'Limited English Students Total',
                 'subject': 'both', 'students': 'Limited', 'test': False},
            14: {'new_col': 'Economically Disadvantaged Students Total',
                 'subject': 'both', 'students': 'Economically', 'test': False}
               }
        # A collection of columns to be generated and the columns that need to
        # be divided to get that value
        self._div_dict = {
            1: {'new_col': 'Total 4 %', 'div_top': 'Student Tested 4s',
                'div_bot': 'Students Tested Total'},
            2: {'new_col': 'Math Prop 4', 'div_top': 'Math Tested 4s',
                'div_bot': 'Math Tested Total'},
            3: {'new_col': 'ELA Prop 4', 'div_top': 'ELA Tested 4s',
                'div_bot': 'ELA Tested Total'},
            4: {'new_col': 'White Students %',
                'div_top': 'White Students Total',
                'div_bot': '4 Tested Total'},
            5: {'new_col': 'Asian / Pacific Islanders Students %',
                'div_top': 'Asian / Pacific Islanders Students Total',
                'div_bot': '4 Tested Total'},
            6: {'new_col': 'Black Students %',
                'div_top': 'Black Students Total',
                'div_bot': '4 Tested Total'},
            7: {'new_col': 'Hispanic / Latino Students %',
                'div_top': 'Hispanic / Latino Students Total',
                'div_bot': '4 Tested Total'},
            8: {'new_col': 'American Indian / Alaska Native Students %',
                'div_top': 'American Indian / Alaska Native Students Total',
                'div_bot': '4 Tested Total'},
            9: {'new_col': 'Multiracial Students %',
                'div_top': 'Multiracial Students Total',
                'div_bot': '4 Tested Total'},
            10: {'new_col': 'Limited English Students %',
                 'div_top': 'Limited English Students Total',
                 'div_bot': '4 Tested Total'},
            11: {'new_col': 'Economically Disadvantaged Students %',
                 'div_top': 'Economically Disadvantaged Students Total',
                 'div_bot': '4 Tested Total'}
           }
           # Collection of columns to be categorically split with pd.cut()
        self._bin_dict = {
            1: {'new_col': 'Income Bin',
                'cut_col': 'School Income Estimate', 'bin_size': 4,
                'labels': ['low', 'medium', 'high', 'highest']},
            2: {'new_col': 'ENI Bin',
                'cut_col': 'Economic Need Index', 'bin_size': 4,
                'labels': ['lowest', 'low', 'medium', 'high']},
            3: {'new_col': 'Total % Bin',
                'cut_col': 'Total 4 %', 'bin_size': 3,
                'labels': ['low', 'medium', 'high']}
           }
        # Collection of column names to convert to percentages from objects
        self._perc_cols = ['Percent ELL', 'Percent Asian', 'Percent Black',
                            'Percent Hispanic', 'Percent Black / Hispanic',
                            'Percent White', 'Student Attendance Rate',
                            'Percent of Students Chronically Absent',
                            'Rigorous Instruction %',
                            'Collaborative Teachers %',
                            'Supportive Environment %',
                            'Effective School Leadership %',
                            'Strong Family-Community Ties %', 'Trust %']
        # Collection of columns that require imputation for missing values
        self._impute_dict = {
            1: {'col': 'Economic Need Index', 'miss_value': np.NaN,
                'strat': 'median'},
            2: {'col': 'Average ELA Proficiency', 'miss_value': np.NaN,
                'strat': 'median'},
            3: {'col': 'Average Math Proficiency', 'miss_value': np.NaN,
                'strat': 'median'}
            }
        # Collection of categorical columns for imputation
        self._cat_impute = ['Rigorous Instruction Rating',
                             'Collaborative Teachers Rating',
                             'Supportive Environment Rating',
                             'Effective School Leadership Rating',
                             'Strong Family-Community Ties Rating',
                             'Trust Rating', 'Student Achievement Rating',
                             'ENI Bin']

    def _init_grade_data_list(self):
        """
        Instantiates a df_groupby() by grades dataframe for plotting
        """
        self.grade_data_list = [
            self.df_groupby('SE'),
            self.df_groupby('PK'),
            self.df_groupby('K'),
            self.df_groupby('01'),
            self.df_groupby('02'),
            self.df_groupby('03'),
            self.df_groupby('04'),
            self.df_groupby('05'),
            self.df_groupby('06'),
            self.df_groupby('07'),
            self.df_groupby('08'),
            self.df_groupby('09'),
            self.df_groupby('10'),
            self.df_groupby('11'),
            self.df_groupby('12')
        ]
        return

    def df_groupby(self, col, update_dict = None):
        """
        Group the data by the given column, and it will return an aggregated
        copy of the dataframe stored within a Data class so the information can
        be utilized with Data methods

        :param col: The column to group the dataframe by
        :param update_dict: If there are any columns not being aggregated, send
        them as an argument here to be able to aggregate more information
        """
        agg_dict = {
           'School Name':'count',
           'City': self.com_fun,
           'Economic Need Index': 'mean',
           'School Income Estimate': 'mean',
           'Percent ELL': 'mean',
           'Percent Asian': 'mean',
           'Percent Hispanic': 'mean',
           'Percent Black / Hispanic': 'mean',
           'Percent White': 'mean',
           'Percent of Students Chronically Absent': 'mean',
           'Student Attendance Rate': 'mean',
           'Rigorous Instruction %': 'mean',
           'Rigorous Instruction Rating': self.com_fun,
           'Collaborative Teachers %': 'mean',
           'Collaborative Teachers Rating': self.com_fun,
           'Supportive Environment %': 'mean',
           'Supportive Environment Rating': self.com_fun,
           'Effective School Leadership %': 'mean',
           'Effective School Leadership Rating': self.com_fun,
           'Strong Family-Community Ties %': 'mean',
           'Strong Family-Community Ties Rating':self.com_fun,
           'Trust %': 'mean',
           'Trust Rating': self.com_fun,
           'Student Achievement Rating': self.com_fun,
           'Average ELA Proficiency': 'mean',
           'Average Math Proficiency': 'mean',
           'White Students Total': 'sum',
           'Asian / Pacific Islanders Students Total': 'sum',
           'Black Students Total': 'sum',
           'Hispanic / Latino Students Total': 'sum',
           'American Indian / Alaska Native Students Total': 'sum',
           'Multiracial Students Total': 'sum',
           'Limited English Students Total': 'sum',
           'Economically Disadvantaged Students Total': 'sum',
           'Students Tested Total': 'sum',
           'Student Tested 4s': 'sum',
           'Math Tested Total': 'sum',
           'Math Tested 4s': 'sum',
           'ELA Tested Total': 'sum',
           'ELA Tested 4s': 'sum',
           'Total 4 %': 'mean',
           'Math Prop 4': 'mean',
           'ELA Prop 4': 'mean',
           '4 Tested Total': 'sum',
           'Grocery Store Count': 'mean',
           'Closest Metro Station': 'mean',
           'Car Crash Count': 'mean',
           'Ethnicity Tested Total': 'sum',
           'Nonreported Ethnicity Total': 'sum',
           'White Students %': 'mean',
           'Asian / Pacific Islanders Students %': 'mean',
           'Black Students %': 'mean',
           'Hispanic / Latino Students %': 'mean',
           'American Indian / Alaska Native Students %': 'mean',
           'Multiracial Students %': 'mean',
           'Limited English Students %': 'mean',
           'Economically Disadvantaged Students %': 'mean',
           'Nonreported Ethnicity %': 'mean',
           'Income Bin': self.com_fun,
           'ENI Bin': self.com_fun,
           'Total % Bin': self.com_fun
        }

        if update_dict != None:
            agg_dict.update(update_dict)

        return_df = self.df.groupby(col).agg(agg_dict)

        # TODO: This isn't working and idk why tbh
        return_df = return_df.rename(columns={'School Name': 'Count'})

        return Data(return_df, self.figwidth, self.figheight)

    def _init_dis(self):
        """
        Instantiates the df_groupby() based on the District column

        Also creates categorical sorting bins and then merges those to the main
        DataFrame
        """
        self.dis = self.df_groupby('District')
        labels = ['lowest', 'low', 'medium', 'high']
        bin_size = 4
        self.dis._column_bin(new_col = 'Total 4 % District Bin',
            cut_col='Total 4 %', bin_size= bin_size,
            labels=labels)
        self.dis._column_bin(new_col = 'School Income District Bin',
            cut_col='School Income Estimate',
            bin_size= bin_size, labels=labels)
        del bin_size
        del labels
        self.data_object_col_merge(self.dis, 'Total 4 % District Bin',
            on='District')
        self.data_object_col_merge(self.dis, 'School Income District Bin',
            on='District')
        return

    def _init_cit(self):
        """
        Instantiates a df_groupby() City dataframe for plotting
        """
        self.cit = self.df_groupby('City')

        labels = ['lowest', 'low', 'medium', 'high']
        bin_size = 4
        self.cit._column_bin(new_col = 'Total 4 % City Bin',
            cut_col='Total 4 %', bin_size= bin_size,
            labels=labels)
        self.cit._column_bin(new_col = 'School Income City Bin',
            cut_col='School Income Estimate',
            bin_size= bin_size, labels=labels)
        self.cit._column_bin(new_col = 'ENI City Bin',
            cut_col='Economic Need Index',
            bin_size= bin_size, labels=labels)
        del bin_size
        del labels
        self.data_object_col_merge(self.cit, 'Total 4 % City Bin',
            on='City')
        self.data_object_col_merge(self.cit, 'School Income City Bin',
            on='City')
        self.data_object_col_merge(self.cit, 'ENI City Bin',
            on='City')

        self.cit.df = self.cit.df[self.cit.df['Count'] > 7]
        self.city_names = self.cit.df.index.values.tolist()
        return
