from wdata import Data
import numpy as np

class SchoolData(Data):
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
