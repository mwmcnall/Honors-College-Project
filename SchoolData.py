import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.pyplot import figure
from sklearn.impute import SimpleImputer
plt.rcParams.update({'font.size': 15})
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class DataContainer:
    """
    A wrapper class for the pandas DataFrame data type. Contains methods
    designed to explore a DataFrame
    """
    def __init__(self, df):
        """
        Constructor clss for Data
        """
        self.df = df

    def _column_bin(self, **kwargs):
        """
        Generates categorical columns based on numerical values, automatically
        splitting based on inputted bin size

        :param new_col: The new column to create
        :param bin_size: The number of bins to separate the data into
        :param labels: The labels to assign to each newly created bin
        """
        assert len(kwargs['labels']) == kwargs['bin_size'], ("You must assign"
            "the same number of labels as the number of bins you are creating")
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
        corr = data.df.corr()[col].sort_values()
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

class DataCleaner(DataContainer):
    """
    A class that inherits from DataContainer, designed to use methods to help
    clean data
    """
    def __init__(self, df):
        super().__init__(df)

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

class Graph(DataContainer):
    """
    A class that inherits from DataContainer, designed to make graphing with
    DataFrames somewhat more customized for my needs
    """
    def __init__(self, df, figwidth=15, figheight=7):
        super().__init__(df)
        self.figwidth = figwidth
        self.figheight = figheight

        return

    def _create_plot(self, title, xlabel, ylabel):
        """
        Creates a single figure and then labels it
        """
        ax = figure(figsize=(self.figwidth, self.figheight)).subplots(1)

        self._plot_label(ax, title, xlabel, ylabel)

        return ax

    def _plot_label(self, ax, title, xlabel, ylabel):
        """
        Adds labels to the plot
        """
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        return

    def sum_col_barplot(self, cols, title, xlabel, ylabel, names, pos_gap=10):
        """
        Sums the columns sent in and plots them in the order that they were
        given

        :param cols: List of columns, each of which will become a bar on the
            bar graph
        :param names: The names that will appear under each bar in order
        :param pos_gap: The distance between each bar
        :return: Nothing,
        """
        vals = []
        # TODO: Turn to list comprehension
        for col in cols:
            vals.append(self.df[col].sum())

        ax = self._create_plot(title, xlabel, ylabel)

        # Chooses the position of each barplots on the x-axis
        y_pos = [i * pos_gap for i in range(0, len(cols))]
        ax.bar(y_pos, vals, width=30)

        # Create names on the x-axis
        ax.set_xticks(y_pos, names)

        return

    def two_shared_barplot(self, barWidth, col_1, col_2,
                           label_1, label_2, section_labels, title, xlabel,
                           ylabel, col_spacing=3, color1='red', color2='blue'):
        """

        """
        assert len(col_1) == len(col_2), ("Function designed only for columns"
            "with exactly the same length.")
        assert len(col_1) == len(section_labels), ("Length of column 1 and"
            "number of section labels must be same.")

        ax = self._create_plot(title, xlabel, ylabel)

        col_1_data = []
        # Calculates the total of totals
        col_1_tot = self.df[col_1].sum().sum()
        col_2_data = []
        col_2_tot = self.df[col_2].sum().sum()

        # Sums all the columns, this is the height of the bar
        for i in range(0, len(col_1)):
            col_1_data.append(df[col_1[i]].sum() / col_1_tot)
            col_2_data.append(df[col_2[i]].sum() / col_2_tot)

        # Generate location of all bars
        col_1_loc = [*range(1, len(col_1) * col_spacing, col_spacing)]
        col_2_loc = [i + 1 for i in col_1_loc]

        ax.bar(col_1_loc, col_1_data, width=barWidth, color=color1,
                label=label_1)
        ax.bar(col_2_loc, col_2_data, width=barWidth, color=color2,
                label=label_2)

        ax.legend()

        plt.xticks(col_1_loc, section_labels)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=2))

        # plt.show()
        return

    def scatter(self, x_col, y_col, title, xlabel, ylabel, x_bounds=None,
                y_bounds=None, alpha=1, c=None, label_percs = False,
                rev_x = False, rev_y = False, x_low_limit = -9**999,
                x_high_limit=9**999, y_low_limit = -9**999,
                y_high_limit=9**999, reg_line = False):
        """
        Creates a scatterplot of the data given

        :param x_col: Data on the x column
        :param y_col: Data on the y column
        :param x_bounds: Limit or reverse the x-axis data
        :param y_bounds: Limit or reverse the y-axis data
        :param label_percs: Set to True to get percentages to 2-decimal places
            on both axes
        :param rev_x: Reverse x-axis if True
        :param rev_y: Reverse y-axis if True
        :param x_low_limit: Lower-limit for x-axis' data, inclusive
        :param y_low_limit: Lower-limit for y-axis' data, inclusive
        :param x_high_limit: Upper-limit for x-axis' data, inclusive
        :param y_high_limit: Upper-limit for y-axis' data, inclusive
        :return: The scatterplot generated
        """
        #TODO: Come up with a better idea for the default limit sizes
        #TODO: label_percs forces percentages on both axes atm, would be
            # smarter to be able to set either axis

        ax = self._create_plot(title, xlabel, ylabel)

        scatter_data = self.df[(self.df[x_col] >= x_low_limit) &
                        (self.df[x_col] <= x_high_limit) &
                        (self.df[y_col] >= y_low_limit) &
                        (self.df[y_col] <= y_high_limit)]
        x = scatter_data[x_col]
        y = scatter_data[y_col]
        ax.scatter(x, y,
                    alpha=alpha,
                    c=c)
        ax.grid(True)

        if rev_x:
            ax.set_xlim(max(x), min(y))
        elif x_bounds != None:
            ax.set_xlim(x_bounds[0], x_bounds[1])
        if rev_y:
            ax.set_ylim(max(y), min(y))
        elif y_bounds != None:
            ax.set_ylim(y_bounds[0], y_bounds[1])

        if label_percs:
            ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=2))
            ax.xaxis.set_major_formatter(ticker.PercentFormatter(decimals=2))

        if reg_line:
            self.add_regline(x, y)

        del scatter_data

        return plt.show()

    def scatter_two_percs(self, cols, title, reg_line = False):
        self.scatter(x_col=cols[0], y_col=cols[1], title = title,
                     xlabel = cols[0],
                     ylabel = cols[1], alpha = .25, label_percs=True,
                     x_bounds=[-0.025, 1.025],
                     y_bounds=[-0.025,1.025],
                     x_low_limit=0.01,x_high_limit=0.99,
                     y_low_limit=0.01,y_high_limit=0.99, reg_line = reg_line)

        return

    def add_regline(self, x, y):
        # https://stackoverflow.com/questions/19068862/how-to-overplot-a\
        # -line-on-a-scatter-plot-in-python, user: 1"
        plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)),
            c='black')
        return

class BaseData()
    pass

class SchoolData(DataCleaner, Graph):
    """
        A Data-inherited class designed to specifically deal with dataset
    """

    def __init__(self, df, figwidth, figheight):
        """
        Constructor method for SchoolData
        """
        super().__init__(df)
        self.figwidth=figwidth
        self.figheight=figheight
        # A collection of columns that will be created and summed based on the
        # arguments sent into columnGenerator
        self.__sum_dict = {
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
        self.__div_dict = {
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
            11: {'new_col': 'Economically Disadvantaged Students%',
                 'div_top': 'Economically Disadvantaged Students Total',
                 'div_bot': '4 Tested Total'}
           }
        # Collection of columns to be categorically split with pd.cut()
        self.__bin_dict = {
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
        self.__perc_cols = ['Percent ELL', 'Percent Asian', 'Percent Black',
                            'Percent Hispanic', 'Percent Black / Hispanic',
                            'Percent White', 'Student Attendance Rate',
                            'Percent of Students Chronically Absent',
                            'Rigorous Instruction %',
                            'Collaborative Teachers %',
                            'Supportive Environment %',
                            'Effective School Leadership %',
                            'Strong Family-Community Ties %', 'Trust %']
        # Collection of columns that require imputation for missing values
        self.__impute_dict = {
            1: {'col': 'Economic Need Index', 'miss_value': np.NaN,
                'strat': 'median'},
            2: {'col': 'Average ELA Proficiency', 'miss_value': np.NaN,
                'strat': 'median'},
            3: {'col': 'Average Math Proficiency', 'miss_value': np.NaN,
                'strat': 'median'}
            }
        # Collection of categorical columns for imputation
        self.__cat_impute = ['Rigorous Instruction Rating',
                             'Collaborative Teachers Rating',
                             'Supportive Environment Rating',
                             'Effective School Leadership Rating',
                             'Strong Family-Community Ties Rating',
                             'Trust Rating', 'Student Achievement Rating',
                             'ENI Bin']
        self._transform_data()

    def _transform_data(self):
        """
        A collection of methods and calls that re-structure the School data
        to be more organized
        """
        self._rename_cols()
        self._type_correction()
        # Set to retain only unique items, filled with some base columns
        # I won't be using
        drop_cols = set(['Adjusted Grade', 'New?',
                         'Other Location Code in LCGMS',
                         'SED Code', 'Location Code',
                         'Address (Full)'])
        drop_cols = self._feature_engineering(drop_cols)
        # Make sure not to drop columns concerning all students
        drop_cols = [i for i in drop_cols if 'All Students' not in i]
        # Drop superfluous columns
        self.drop_cols(drop_cols)

        # Organize grades
        self._grade_combination()
        # Impute numerical columns
        self.dict_fun_run(self.__impute_dict, self.imputer)
        # Impute categorical columns
        for col in self.__cat_impute:
            self.cat_impute(col)
        # Create Boolean columns for different grades
        self._grade_bools()
        del self.__impute_dict
        del self.__cat_impute

    def _rename_cols(self):
        """
        Columns that require re-naming to match the pattern that is displayed
        in the majority of data
        """
        self.df.rename(columns={'Grade 3 Math - All Students tested':
                                'Grade 3 Math - All Students Tested'},
                       inplace=True)

        return

    def _type_correction(self):
        """
        A function for all type corrections
        """
        # Convert from dollars to a float
        self.df['School Income Estimate'] = \
            self.df['School Income Estimate'].apply(self.dollarsToDigits)

        # Converts all object style percents to float style percents
        for col in self.__perc_cols:
            self.df[col] = self.df[col].apply(self.percents_to_floats)

        # Convert column to type Boolean
        self.df['Community School?'] = self.df['Community School?'].map(
            {'Yes': 1, 'No': 0})

        return

    def _misc_features(self):
        """
        A collection of operations to help readability and processing of data
        These fit outside the order of the logical feature engineering order,
        they are needed to be able to engineer the rest of the featuers.
        """
        # Column needed for upcoming processing
        self.df['4 Tested Total'] = self.df['Math Tested 4s'] + \
            self.df['ELA Tested 4s']
        column_4s = ['White Students Total',
                     'Asian / Pacific Islanders Students Total',
                     'Black Students Total',
                     'Hispanic / Latino Students Total',
                     'American Indian / Alaska Native Students Total',
                     'Multiracial Students Total']

        # Operations that fit outside the dictionaries for organization regions
        self.df['Ethnicity Tested Total'] = \
            self.df[column_4s].apply(sum, axis=1)
        self.df['Nonreported Ethnicity Total'] = \
            self.df['4 Tested Total'] - self.df['Ethnicity Tested Total']
        self.df['Nonreported Ethnicity %'] = \
            (self.df['Nonreported Ethnicity Total'] /
             self.df['4 Tested Total']).fillna(0)

        return

    def _feature_engineering(self, drop_cols):
        """
        Organizes, cleans, and feature engineers columns for the data

        Responsibilities:
            - Fixes some readability
            - Columns based around sums
            - Columns based around division
            - Columns based around bins
            - Organizes the Grades
            - Drops superfluous columns
        """
        # Engineer all features that involve sums
        drop_cols = self._process_drop_features(self.__sum_dict, drop_cols)

        # Help make the data more readable, must be called after the above line
        self._misc_features()

        # Engineer all features that involve division
        self.dict_fun_run(self.__div_dict, self._column_div)
        # Engineer all features that involve bins (pd.cut)
        self.dict_fun_run(self.__bin_dict, self._column_bin)

        del self.__sum_dict
        del self.__bin_dict
        del self.__div_dict
        del self.__perc_cols

        return drop_cols

    def _column_sum(self, **kwargs):
        """
        Generates columns using column_generator, sums them, and assigns them
        to a new column

        :return: The list of columns that were summed based on the **kwargs
            arguments sent in
        """
        col_data = self.column_generator(subject=kwargs['subject'],
                                         students=kwargs['students'],
                                         test=kwargs['test'])
        self.df[kwargs['new_col']] = self.df[col_data].apply(sum, axis=1)
        return(col_data)

    def _process_drop_features(self, dic, drop_cols):
        """
        Using column_generator and _column_sum, adds all of the values of the
        columns generated and stores the sum into the provided column in
        new_col

        :param drop_cols: A set that will be updated with columns to drop
        :return: A set of columns
        """
        # new_col is the name of the new column that will be updated with the
        # sums of all values generated by column_generator
        # Each nested dictionary acts as a list of **kwargs arguments for
        # _column_sum

        for item in dic.items():
            drop_cols.update(self._column_sum(**item[1]))

        return drop_cols

    def _grade_combination(self):
        """
        Sums all the like Grades 4 scores and stores it in a new total column

        :return: Nothing, all columns are assigned in the function
        """
        cols = list(self.df.columns)
        for grade in range(3, 8 + 1):
            col_data = [i for i in cols if ('Grade ' + str(grade) in i) and
                        ('All Students' in i) and
                        ('Tested' not in i)]
            self.df['Grade ' + str(grade) + ' 4s Total'] = \
                self.df[col_data].apply(sum, axis=1)
        del cols
        return

    def _grade_bools(self):
        """
        Create a boolean column for each possible grade
        """
        grades = self.lol_to_set(col='Grades', splitby=',')

        for grade in grades:
            self.df[grade] = False

        for grade in grades:
            self.df.loc[self.df['Grades'].str.contains(grade), grade] = True
        return

    def column_generator(self, subject='both', students='All Students',
                         test=False):
        """
        Generates a list of columns based on the input given

        :param subject: School subject, must be: 'both', 'Math', or 'Ela'
        :param students: Filters for the type of student, 'All Students' is
            default
        :param test: Also returns for columns that end in ' Tested' if True
        :return: A list of columns from the data

        >>> data.column_generator(test = True, subject = 'ELA')
        ['Grade 3 ELA - All Students Tested',
         'Grade 4 ELA - All Students Tested',
         'Grade 5 ELA - All Students Tested',
         'Grade 6 ELA - All Students Tested',
         'Grade 7 ELA - All Students Tested',
         'Grade 8 ELA - All Students Tested']

        >>> data.column_generator(test = False, subject = 'Math')
        ['Grade 3 Math 4s - All Students',
         'Grade 4 Math 4s - All Students',
         'Grade 5 Math 4s - All Students',
         'Grade 6 Math 4s - All Students',
         'Grade 7 Math 4s - All Students',
         'Grade 8 Math 4s - All Students']
        """
        # Ensures subject is assigned correctly
        assert subject in ['both', 'Math', 'ELA'], ('Subject must be: both'
                                                    'Math, or ELA')

        if test:
            assert students == 'All Students', ('test Flag should only be set'
                                                'true with All Students')
            students += ' Tested'
        else:
            students = '4s - ' + students

        # Stores a list of all the columns
        cols = list(self.df.columns)

        if subject == 'both':
            return [i for i in cols if students in i and
                    ('ELA' in i or 'Math' in i)]
        elif subject == 'Math':
            return [i for i in cols if students in i and 'Math' in i]
        elif subject == 'ELA':
            return [i for i in cols if students in i and 'ELA' in i]
        else:
            return -1  # An error has occurred


df = pd.read_csv('2016 School Explorer.csv')
# print(df.shape)
# Load data into a SchoolData Class
data = SchoolData(df, figwidth=11, figheight=7)
#%%
# data.sum_col_barplot(cols = ['Grade 3 4s Total', 'Grade 4 4s Total',
#     'Grade 5 4s Total','Grade 6 4s Total','Grade 7 4s Total',
#     'Grade 8 4s Total'], names = ['Grade 3', 'Grade 4', 'Grade 5', 'Grade 6',
#     'Grade 7', 'Grade 8'], title = 'Number of 4s Scored by Grade',
#     xlabel = 'Grade', ylabel = 'Number of 4s',
#     pos_gap = 40)
#     #TODO: x-axis column names not displaying correctly, steal solution
#     # from two_shared_barplot
# #%%
# cols = data.column_generator(subject = 'both')
# data.two_shared_barplot(barWidth = 1,
#                         col_1 = [i for i in cols if 'Math' in i],
#                         col_2 = [i for i in cols if 'ELA' in i],
#                         label_1 = 'Math',
#                         label_2 = 'ELA',
#                         section_labels = ['Grade 3', 'Grade 4', 'Grade 5',
#                             'Grade 6', 'Grade 7', 'Grade 8'],
#                         title = 'Proportion of 4s by Subject',
#                         xlabel = 'Grades',
#                         ylabel = '% of 4s')
# #%%
# data.scatter_two_percs(['Percent of Students Chronically Absent', 'Total 4 %'],
#      title = "Total 4 % for Chronically Absent Students", reg_line=True)
# #%%
# data.scatter_two_percs(['Economic Need Index', 'Total 4 %'],
#      title = "Total 4 % by ENI", reg_line=True)

data.df.head(1)
#%%
com_fun = lambda x:x.value_counts().index[0]
dis_df = Graph(df.groupby('District').agg({
                       'School Name':'count',
                       'City': com_fun,
                       'Economic Need Index': 'mean',
                       'School Income Estimate': 'mean',
                       'Percent ELL': 'mean',
                       'Percent Asian': 'mean',
                       'Percent Hispanic': 'mean',
                       'Percent Black / Hispanic': 'mean',
                       'Percent White': 'mean',
                       'Percent of Students Chronically Absent': 'mean',
                       'Rigorous Instruction %': 'mean',
                       'Rigorous Instruction Rating': com_fun,
                       'Collaborative Teachers %': 'mean',
                       'Collaborative Teachers Rating': com_fun,
                       'Supportive Environment %': 'mean',
                       'Supportive Environment Rating': com_fun,
                       'Effective School Leadership %': 'mean',
                       'Effective School Leadership Rating': com_fun,
                       'Strong Family-Community Ties %': 'mean',
                       'Strong Family-Community Ties Rating':com_fun,
                       'Trust %': 'mean',
                       'Trust Rating': com_fun,
                       'Student Achievement Rating': com_fun,
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
                       'Ethnicity Tested Total': 'sum',
                       'Nonreported Ethnicity Total': 'sum',
                       'Income Bin': com_fun,
                       'ENI Bin': com_fun,
                       'Total % Bin': com_fun
                       }))
dis_df.df
dis_df.scatter_two_percs(['Economic Need Index', 'Total 4 %'],
     title = "Total 4 % by ENI", reg_line=True)
DataContainer.corr_one_col(dis_df, 'Total 4 %')

#%%
data.corr_one_col('Total 4 %')
#%%
data.scatter_two_percs(['Percent Black / Hispanic', 'Total 4 %'],
     title = "", reg_line=True)
