dataset_before = '''Int64Index: 309 entries, 0 to 308
Data columns (total 11 columns):
 #   Column    Non-Null Count  Dtype 
---  ------    --------------  ----- 
 0   name      309 non-null    object
 1   diet      309 non-null    object
 2   period    309 non-null    object
 3   lived_in  308 non-null    object
 4   type      309 non-null    object
 5   length    291 non-null    object
 6   taxonomy  309 non-null    object
 7   named_by  309 non-null    object
 8   species   304 non-null    object
 9   link      309 non-null    object
 10  image     308 non-null    object
dtypes: object(11)
'''

dataset_after = '''Int64Index: 300 entries, 0 to 308
Data columns (total 15 columns):
 #   Column       Non-Null Count  Dtype  
---  ------       --------------  -----  
 0   name         300 non-null    object 
 1   species      300 non-null    object 
 2   type         300 non-null    object 
 3   length       300 non-null    float64
 4   diet         300 non-null    object 
 5   period       300 non-null    object 
 6   period_from  300 non-null    int32  
 7   period_to    300 non-null    int32  
 8   lived_in     300 non-null    object 
 9   discovered   300 non-null    int32  
 10  named_by     300 non-null    object 
 11  major_group  300 non-null    object 
 12  taxonomy     300 non-null    object 
 13  link         300 non-null    object 
 14  image        300 non-null    object 
dtypes: float64(1), int32(3), object(11)
'''

dataset_describe = '''
             count         mean        std     min     25%     50%      75%     max
length       300.0     6.827900   6.403294     0.0     2.0     5.0     9.00    35.0
period_from  300.0   122.253333  45.037285    67.0    81.0   120.0   155.00   228.0
period_to    300.0   114.153333  44.775506    65.0    74.0    99.0   145.00   238.0
discovered   300.0  1955.633333  45.014069  1826.0  1922.0  1975.0  1993.25  2010.0'''