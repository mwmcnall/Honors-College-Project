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



from .DataContainer import *
from .DataCleaner import *
from .Graph import *
from .Data import *
