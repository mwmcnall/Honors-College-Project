from wdata import *
from school_wdata import SchoolData


df = pd.read_csv('2016 School Explorer.csv')
# print(df.shape)
# Load data into a SchoolData Class
data = SchoolData(df=df,figwidth=11,figheight=7)
#%%
data.sum_col_barplot(cols = ['Grade 3 4s Total', 'Grade 4 4s Total',
    'Grade 5 4s Total','Grade 6 4s Total','Grade 7 4s Total',
    'Grade 8 4s Total'], names = ['Grade 3', 'Grade 4', 'Grade 5', 'Grade 6',
    'Grade 7', 'Grade 8'], title = 'Number of 4s Scored by Grade',
    xlabel = 'Grade', ylabel = 'Number of 4s',
    pos_gap = 40)
    #TODO: x-axis column names not displaying correctly, steal solution
    # from two_shared_barplot
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
