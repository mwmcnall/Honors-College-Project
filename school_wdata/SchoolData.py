from .SchoolGraph import SchoolGraph
from .SchoolOrganize import SchoolOrganize
import numpy as np
import pandas as pd
from sklearn import preprocessing

class SchoolData(SchoolOrganize, SchoolGraph):
    """
    A class designed specifically to deal with this dataset. Mostly dedicated
    to calling methods upon creation to sort the data how I want.
    """
    def __init__(self, df, figwidth, figheight,subset=False,**kwargs):
        """
        Constructor method for SchoolData
        """
        super().__init__(df,**kwargs)
        # A collection of columns that will be created and summed based on the
        # arguments sent into columnGenerator
        # IDEA: Will a list of dictionaries be faster than a nested dictionary
        # where the number representation doesn't matter
        if not subset:
            self.retail_read()
            self.metro_read()
            self.car_read()
            self._transform_data()
            self._calculate_in_need()
            self._final_drop()

    def retail_read(self):
        """
        Reads in Grocery Store Data and merges with dataset
        """
        retail_food_df = pd.read_csv('Retail_Food_Stores.csv')

        retail_food_df['Establishment Type'] = [ i.strip() \
            for i in retail_food_df['Establishment Type'] ]
        retail_zips = pd.DataFrame(retail_food_df[retail_food_df[\
            'Establishment Type'] == \
            'A'].groupby('Zip Code').count().loc[:,'County'])
        retail_zips = retail_zips.reset_index()
        retail_zips.columns = ['Zip', 'Grocery Store Count']

        self.df = pd.merge(self.df, retail_zips, on = 'Zip', how = 'left')

        del retail_food_df
        del retail_zips

        # Convert to integer values and fill empty values with 0
        self.df['Grocery Store Count'] = \
            self.df['Grocery Store Count'].fillna(0)
        self.df['Grocery Store Count'] = \
            self.df['Grocery Store Count'].astype(int)

        return

    def  metro_read(self):
        """
        Reads in Metro Distances data and merges with dataset
        """
        # Computationally expensive, ran once and saved info
        # self._metro_read()
        # Reloads computed code and adds it to the dataframe
        metro_distance = pd.read_csv('Metro distances.csv')
        self.df['Closest Metro Station'] = metro_distance

        del metro_distance

        return

    def _metro_read(self):
        # Read in file
        metro_df = pd.read_csv('NYC_Transit_Subway_Entrance_And_Exit_Data.csv')

        # Create a tuple of co-ordinates to match the metro_df
        df['Coords'] = [(i,j) for i, j in zip(df['Latitude'], df['Longitude'])]

        # Read from bottom to top for most coherent explanation of the double
        # list comprehension
                    # Creates a tuple out of the two float numbers in a
                    # co-ordinate
        stations = [tuple([float(number) for number in group]) \
                    # Takes each string co-ordinate, and separates it into
                    # two float numbers (in string form)
                    for group in [s.strip("()").split(",") \
                                  # For each co-ordinate stored in the metro
                                  # dataframe
                                  for s in metro_df['Station Location']] ]

        def returnClosestStation(coords):
            closest = -1
            for station in stations:
                distance = coordsDistance( station, coords)
                if distance > closest:
                    closest = distance
            return closest

        self.df['Closest Metro Station'] = \
            self.df['Coords'].apply(returnClosestStation)

        del metro_df
        del stations

        self.df['Closest Metro Station'].to_csv(\
            'Metro distances.csv', index = False)

    def car_read(self):
        """
        Reads in the car-accident data and merges with the dataset
        """
        # Computationally expensive, ran once and saved info
        # self._car_read()
        # Reloads computed code and adds it to the dataframe
        car_crashes = pd.read_csv('Car Crash Count.csv')
        self.df['Car Crash Count'] = car_crashes
        del car_crashes

    def _car_read(self):
        crashes_df = pd.read_csv('nypd-motor-vehicle-collisions.csv')
        # Many zip code values weren't kept track of, most of these were considered less severe car accidents so I dropped
        # them all from the dataset
        crashes_df = pd.DataFrame(crashes_df.dropna(subset = \
            ['ZIP CODE']).groupby('ZIP CODE').count()['TIME'])
        crashes_df = crashes_df.reset_index()
        crashes_df.columns = ['Zip', 'Car Crash Count']

        # Zip codes were not inputted well in this dataset, there were multiple formats for all zip codes, I went through a process
        # of converting from strings to floats or ints or just returned as an empty string to drop later.

        def convert(n):
            try:
                return(int(n))
            except:
                pass
            try:
                return(float(n))
            except:
                pass
            return(n.strip())

        crashes_df['Zip'] = crashes_df['Zip'].apply(convert)
        crashes_df = crashes_df[crashes_df['Zip'] != ''].astype(int)
        crashes_df = crashes_df.groupby('Zip').sum()
        self.df = pd.merge(self.df, crashes_df, on = 'Zip', how = 'left')

        del crashes_df

        self.df['Car Crash Count'].to_csv('Car Crash Count.csv', index = False)

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
        self.dict_fun_run(self._impute_dict, self.imputer)
        # Impute categorical columns
        for col in self._cat_impute:
            self.cat_impute(col)
        # Create Boolean columns for different grades
        self._grade_bools()
        del self._impute_dict
        del self._cat_impute
        return

    def _rename_cols(self):
        """
        Columns that require re-naming to match the pattern that is displayed
        in the majority of data
        """
        self.df.rename(columns={
            'Grade 3 Math - All Students tested':
            'Grade 3 Math - All Students Tested'}, inplace=True)
        return

    def _type_correction(self):
        """
        A function for all type corrections
        """
        # Convert from dollars to a float
        self.df['School Income Estimate'] = \
            self.df['School Income Estimate'].apply(self.dollarsToDigits)

        # Converts all object style percents to float style percents
        for col in self._perc_cols:
            self.df[col] = self.df[col].apply(self.percents_to_floats)

        # Convert column to type Boolean
        self.df['Community School?'] = self.df['Community School?'].map(
            {'Yes': 1, 'No': 0})

        return

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
            col_data = [i for i in cols if ('Grade ' + str(grade) in i) and
                        ('All Students' in i) and
                        ('Tested' in i)]
            self.df['Grade ' + str(grade) + ' 4s Tested Total'] = \
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

    def _calculate_in_need(self):
        """
        Calculates the In Need Score for schools, a weighted formula to
        determine what schools are in need of the new resources
        """
        # Instantiate score column with 0, for lowest possible score
        self.df['In Need Score'] = 0
        # A nested dictionary to calculate weights and add to the In Need Score
        pre_dict = {
            0: {'pre_col':'Economic Need Index', 'weight':0.75},
            1: {'pre_col':'White Students %', 'invert':True, 'weight':0.80},
            2: {'pre_col':'Asian / Pacific Islanders Students %',
                'weight':0.40},
            3: {'pre_col':'Multiracial Students %', 'weight':0.05},
            4: {'pre_col':'Black Students %', 'weight':0.80},
            5: {'pre_col':'Hispanic / Latino Students %', 'weight':0.60},
            6: {'pre_col':'American Indian / Alaska Native Students %',
                'weight':0.15},
            7: {'pre_col':'Limited English Students %', 'weight':0.05},
            8: {'pre_col':'Economically Disadvantaged Students %',
                'weight':0.30},
            9: {'pre_col':'Total 4 %', 'invert':True, 'weight':0.8},
            10: {'pre_col':'Math Prop 4', 'invert':True, 'weight':0.6},
            11: {'pre_col':'ELA Prop 4', 'invert':True, 'weight':0.6},
            12: {'pre_col':'Percent of Students Chronically Absent',
                'weight':0.25}
        }
        # Computes all straight-forward weighted scores
        self.dict_fun_run(pre_dict, self._in_need_calculate)

        # School Income Estimate fits outside of the nice loop structure
        # This is beacuse 0 indicates that they had no data for it, meaning it
        # has to be handled differently than all other columns
        self.subset_normalized_in_need(col='School Income Estimate',
            weight=0.30, col_greater_than=0.001, filter_greater_than=0.001,
            invert=False)
        # Bin columns from groupby calls
        bin_dict={
            0:{'bin_col':'Total 4 % City Bin', 'lowest':0.30, 'low':0.20,
                'medium':-0.40, 'high':-0.8},
            1:{'bin_col':'School Income City Bin', 'lowest':0.20, 'low':0.10,
                'medium':-0.40, 'high':-0.8},
            2:{'bin_col':'ENI City Bin', 'lowest':0.20, 'low':0.10,
                'medium':-0.40, 'high':-0.8},
            3:{'bin_col':'School Income District Bin', 'lowest':0.20,
                'low':0.10, 'medium':-0.40, 'high':-0.8},
            4:{'bin_col':'Total 4 % District Bin', 'lowest':0.30, 'low':0.15,
                'medium':-0.40, 'high':-0.8}
        }

        # Instantiate Classes in order to get their information
        self._init_cit()
        self._init_dis()

        self.dict_fun_run(bin_dict, self.iterate_bin_need)
        # Rating information and how it affects score
        rating_dict={
            0:{'bin_col':'Rigorous Instruction Rating',
                'not_meeting_target':0.75, 'approaching_target':0.55,
                'meeting_target':-0.75, 'exceeding_target':-1},
            1:{'bin_col':'Collaborative Teachers Rating',
                'not_meeting_target':0.75, 'approaching_target':0.55,
                'meeting_target':-0.75, 'exceeding_target':-1},
            2:{'bin_col':'Supportive Environment Rating',
                'not_meeting_target':0.75, 'approaching_target':0.55,
                'meeting_target':-0.75, 'exceeding_target':-1},
            3:{'bin_col':'Effective School Leadership Rating',
                'not_meeting_target':0.5, 'approaching_target':0.25,
                'meeting_target':-0.25, 'exceeding_target':-0.5},
            4:{'bin_col':'Strong Family-Community Ties Rating',
                'not_meeting_target':0.25, 'approaching_target':0.10,
                'meeting_target':-0.10, 'exceeding_target':-0.25},
            5:{'bin_col':'Trust Rating',
                'not_meeting_target':0.25, 'approaching_target':0.10,
                'meeting_target':-0.10, 'exceeding_target':-0.25},
            6:{'bin_col':'Student Achievement Rating',
                'not_meeting_target':0.75, 'approaching_target':0.55,
                'meeting_target':-0.75, 'exceeding_target':-1}
        }

        self.dict_fun_run(rating_dict, self.iterate_bin_rating)

        # If the school offers a grade associated with SE or 6+
        grades_in_need = (self.df['SE'] == True) | (self.df['06'] == True) |\
            (self.df['07'] == True) | (self.df['08'] == True) | \
            (self.df['09'] == True) | (self.df['10'] == True) | \
            (self.df['11'] == True) | (self.df['12'] == True)
        # Increase the In Need Score
        self.df.loc[grades_in_need, 'In Need Score'] += 0.5

        # Normalize the In Need Score column from 0 to 100
        self.df['In Need Score'] = self.normalize_column('In Need Score') * 100

        return

    def iterate_bin_need(self, bin_col, lowest, low, medium, high):
        """
        This is inefficient but it works
        """
        for index, value in enumerate(self.df[bin_col]):
            self._bin_need_calculate(value, index, lowest, low, medium, high)

    def iterate_bin_rating(self, bin_col, not_meeting_target,
        approaching_target, meeting_target, exceeding_target):
        """
        This is inefficient but it works
        """
        for index, value in enumerate(self.df[bin_col]):
            self._bin_rating_calculate(value, index, not_meeting_target,
                approaching_target, meeting_target, exceeding_target)

    def _bin_rating_calculate(self, value, index, not_meeting_target,
        approaching_target, meeting_target, exceeding_target):
        if value=='Not Meeting Target':
            self.df.loc[index, 'In Need Score'] += not_meeting_target
        elif value=='Approaching Target':
            self.df.loc[index, 'In Need Score'] += approaching_target
        elif value=='Meeting Target':
            self.df.loc[index, 'In Need Score'] += meeting_target
        elif value=='Exceeding Target':
            self.df.loc[index, 'In Need Score'] += exceeding_target
        return

    def _bin_need_calculate(self, value, index, lowest, low, medium, high):
        if value=='lowest':
            self.df.loc[index, 'In Need Score'] += lowest
        elif value=='low':
            self.df.loc[index, 'In Need Score'] += low
        elif value=='medium':
            self.df.loc[index, 'In Need Score'] += medium
        elif value=='high':
            self.df.loc[index, 'In Need Score'] += high
        return

    def _in_need_calculate(self, pre_col, weight, invert=False):
        normalized_values = self.normalize_column(pre_col, invert)
        self.df['In Need Score'] += normalized_values * weight
        return

    def subset_normalized_in_need(self, col, weight, col_greater_than=None,
        col_less_than=None, filter_greater_than=None,
        filter_less_than=None, invert=False):

        col_greater_than, col_less_than = self._set_greater_less_than(col,
            col_greater_than, col_less_than)

        subset_normalized = self.normalize_column_filter(col=col,
            greater_than=filter_greater_than, less_than=filter_less_than,
            invert=True)

        self.df.loc[(self.df[col] >= col_greater_than) & \
            (self.df[col] <= col_less_than),'In Need Score'] += \
            subset_normalized * weight

        return

    def _final_drop(self):
        """
        Columns that aren't needed anymore after all my calculations are done
        Totals are superfluos now that I have proportions.
        """
        drop_cols = ['Student Tested 4s', 'Math Tested Total', 'Math Tested 4s',
            'ELA Tested Total', 'ELA Tested 4s', 'White Students Total',
            'Asian / Pacific Islanders Students Total',
            'Black Students Total', 'Hispanic / Latino Students Total',
            'American Indian / Alaska Native Students Total',
            'Multiracial Students Total', 'Limited English Students Total',
            'Economically Disadvantaged Students Total',
            '4 Tested Total', 'Ethnicity Tested Total',
            'Nonreported Ethnicity Total', 'Total 4 % City Bin',
            'School Income City Bin', 'ENI City Bin', 'Total 4 % District Bin',
            'School Income District Bin','Percent ELL', 'Percent Asian',
            'Percent Black', 'Percent Hispanic', 'Percent Black / Hispanic',
            'Percent White']
        self.drop_cols(drop_cols)
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

        # Operations that fit outside the dictionaries for organization reasons
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
        """
        # Engineer all features that involve sums
        drop_cols = self._process_drop_features(self._sum_dict, drop_cols)

        # Help make the data more readable, must be called after sum features
        # but before division and bin features
        self._misc_features()

        # Engineer all features that involve division
        self.dict_fun_run(self._div_dict, self._column_div)
        # Engineer all features that involve bins (pd.cut)
        self.dict_fun_run(self._bin_dict, self._column_bin)

        del self._sum_dict
        del self._bin_dict
        del self._div_dict
        del self._perc_cols

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
        Processes all features that will also be added to a list of columns to
        drop from the dataset

        :param drop_cols: A set that will be updated with columns to drop
        :return: A set of columns
        """

        for item in dic.items():
            drop_cols.update(self._column_sum(**item[1]))

        return drop_cols

    def column_generator(self, subject='both', students='All Students',
                         test=False, grade=None):
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
            lst = [i for i in cols if students in i and
                    ('ELA' in i or 'Math' in i)]
        elif subject == 'Math':
            lst = [i for i in cols if students in i and 'Math' in i]
        elif subject == 'ELA':
            lst = [i for i in cols if students in i and 'ELA' in i]

        if grade != None:
            assert grade >= 3 and grade <= 8
            lst = [i for i in lst if ('Grade ' + str(grade) in i)]

        return lst
        # else:
        #     return -1  # An error has occurred
