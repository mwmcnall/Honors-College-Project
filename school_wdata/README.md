# school_wdata

Contains classes that inherit from *wdata*, created specifically for this project

### SchoolOrganize
- Contains organizational methods for the dataset, mostly exists as a way to help organize the many methods written specifically for this data

### SchoolGraph
- Contains Graphing methods for this data. A lot of them exist to deal with particular groupby DataFrames for this datasset

### SchoolData
- Inherits from the two above classe. The main piece of code is the __init__() constructor method as it does the entire ETL process upon class creation
