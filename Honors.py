"""
This file is completely meant for testing. All tested solutions of Python
code were transferred to an organized position in the Jupyter Notebook
or within a wdata / school_wdata class or method
"""

from wdata import *
from school_wdata import *

df = pd.read_csv('2016 School Explorer.csv')
data = SchoolData(df=df,figwidth=11,figheight=7,font_size=16)

data.df['In Need Score'].describe()

# data.df['Total 4 % City Bin'].value_counts()

# data._init_cit()
# data._init_dis()
# data.df['In Need Score'] = 0
#%%
data.grades_bargraph('School Income Estimate',
    title = 'School Income Estimate by Grades offered at Schools')
#%%
# drop_cols = []
# data.df.head()
# #
# data.df.sort_values('In Need Score').tail()
#
# data.df['In Need Score'].describe()
#
# data.iterate_bin('Total 4 % City Bin')
#
#
#
# pre_cols = [
#     'Economic Need Index',
#     'White Students %',
#     'Asian / Pacific Islanders Students %',
#     'Black Students %',
#     'Hispanic / Latino Students %',
#     'American Indian / Alaska Native Students %',
#     'Multiracial Students %',
#     'Limited English Students %',
#     'Economically Disadvantaged Students %',
#     'Total 4 %',
#     'Math Prop 4',
#     'ELA Prop 4']

# data.corr_one_col('Total 4 %')

# data.simple_scatter(['Grocery Store Count', 'Average Math Proficiency'])

# data.df.head()
