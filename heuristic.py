import gurobipy as gp  # type: ignore
from gurobipy import GRB # type: ignore
import pandas as pd # type: ignore


# 匯入檔案
df_person_data = pd.read_csv('/Users/sophiehuang/Documents/person1_data.csv')
W = df_person_data.iloc[0, 0]  
H = df_person_data.iloc[1, 0]
BMI_level = df_person_data.iloc[2, 0]
budget = df_person_data.iloc[3, 0]


cal_con = (40 - BMI_level*5)*W
p_con = 0.8*W
sod_con = 2000
sug_con = 70

df_breakfast = pd.read_csv('/Users/sophiehuang/Documents/final-data/OR Final - Breakfast-final.csv')
df_breakfast.reset_index(drop=True, inplace=True)
n_b = len(df_breakfast.index)

df_food = pd.read_csv('/Users/sophiehuang/Documents/final-data/OR Final - Food-final.csv')
df_food.reset_index(drop=True, inplace=True)
n_f = len(df_food.index)

df_sidemeal = pd.read_csv('/Users/sophiehuang/Documents/final-data/OR Final - Sidemeal-final.csv')
df_sidemeal.reset_index(drop=True, inplace=True)
n_s = len(df_sidemeal.index)

df_beverage = pd.read_csv('/Users/sophiehuang/Documents/final-data/OR Final - Beverage-final.csv')
df_beverage.reset_index(drop=True, inplace=True)
n_d = len(df_beverage.index)

df_dessert = pd.read_csv('/Users/sophiehuang/Documents/final-data/OR Final - Dessert-final.csv')
df_dessert.reset_index(drop=True, inplace=True)
n_e = len(df_dessert.index)


# Sets
B = range(0, n_b)
F = range(0, n_f)
S = range(0, n_s)
D = range(0, n_d)
E = range(0, n_e)
M = [0, 1, 2]
K = range(1, 8)

# Parameters (to be defined based on your data)
# b, f, s, d, e should be dictionaries with keys (i, j) where j is the attribute index
# For example: b[i,1] for calories of breakfast i, b[i,2] for protein of breakfast i, etc.
# 匯入 b, f, s, d, e 的資料
b = {}
for i in range(len(df_breakfast)):
    b[i, 1] = df_breakfast.at[i, 'Calories']
    b[i, 2] = df_breakfast.at[i, 'Protein']
    b[i, 3] = df_breakfast.at[i, 'Sodium']
    b[i, 4] = df_breakfast.at[i, 'Sugar']
    b[i, 5] = df_breakfast.at[i, 'Price']
    b[i, 6] = df_person_data.iloc[i + 3, 0]
    
    


f = {}
for i in range(len(df_food)):
    f[i, 1] = df_food.at[i, 'Calories']
    f[i, 2] = df_food.at[i, 'Protein']
    f[i, 3] = df_food.at[i, 'Sodium']
    f[i, 4] = df_food.at[i, 'Sugar']
    f[i, 5] = df_food.at[i, 'Price']
    f[i, 6] = df_person_data.iloc[i + 3 + n_b, 0]

s = {}
for i in range(len(df_sidemeal)):
    s[i, 1] = df_sidemeal.at[i, 'Calories']
    s[i, 2] = df_sidemeal.at[i, 'Protein']
    s[i, 3] = df_sidemeal.at[i, 'Sodium']
    s[i, 4] = df_sidemeal.at[i, 'Sugar']
    s[i, 5] = df_sidemeal.at[i, 'Price']
    s[i, 6] = df_person_data.iloc[i + 3 + n_b + n_f, 0]

d = {}
for i in range(len(df_beverage)):
    d[i, 1] = df_beverage.at[i, 'Calories']
    d[i, 2] = df_beverage.at[i, 'Protein']
    d[i, 3] = df_beverage.at[i, 'Sodium']
    d[i, 4] = df_beverage.at[i, 'Sugar']
    d[i, 5] = df_beverage.at[i, 'Price']
    d[i, 6] = df_person_data.iloc[i + 3 + n_b + n_f + n_s, 0]

e = {}
for i in range(len(df_dessert)):
    e[i, 1] = df_dessert.at[i, 'Calories']
    e[i, 2] = df_dessert.at[i, 'Protein']
    e[i, 3] = df_dessert.at[i, 'Sodium']
    e[i, 4] = df_dessert.at[i, 'Sugar']
    e[i, 5] = df_dessert.at[i, 'Price']
    e[i, 6] = df_person_data.iloc[i + 3 + n_b + n_f + n_s + n_d, 0]


print(cal_con)
print(p_con)
print(sod_con)
print(sug_con)



## Choose nice option for every meals
for i in range(len(df_breakfast)):
    if b[i, 1] < 0.25*cal_con and b[i, 2] > 0.05*p_con and b[i, 3] < 0.15*sod_con and b[i, 4] < 0.15*sug_con and b[i, 5] < 0.15*budget:
        b[i, 7] = 1
    else:
        b[i, 7] = 0
        
for i in range(len(df_food)):
    if f[i, 1] < 0.4*cal_con and f[i, 3] < 0.4*sod_con and f[i, 4] < 0.1*sug_con and f[i, 5] < 0.33*budget:
        f[i, 7] = 1
    else:
        f[i, 7] = 0
        
for i in range(len(df_food)):
    if f[i, 1] < 0.4*cal_con and f[i, 3] < 0.4*sod_con and f[i, 4] < 0.1*sug_con and f[i, 5] < 0.33*budget:
        f[i, 8] = 1
    else:
        f[i, 8] = 0
        
for i in range(len(df_beverage)):
    if d[i, 1] < 0.15*cal_con and d[i, 3] < 0.1*sod_con and d[i, 4] < 0.45*sug_con and d[i, 5] < 0.12*budget:
        d[i, 7] = 1
    else:
        d[i, 7] = 0
        
for i in range(len(df_dessert)):
    if e[i, 1] < 0.2*cal_con and e[i, 2] > 0.08*p_con and e[i, 3] < 0.1*sod_con and e[i, 4] < 0.45*sug_con and e[i, 5] < 0.12*budget:
        e[i, 7] = 1
    else:
        e[i, 7] = 0
        
 ## Print the result
print('breakfast:')
for i in range(len(df_breakfast)):
    print(b[i, 7], end = ' ')
        
print('lunch:')
for i in range(len(df_food)):
    print(f[i, 7], end = ' ')
        
print('dinner:')
for i in range(len(df_food)):
    print(f[i, 8], end = ' ')
        
print('beverage:')
for i in range(len(df_beverage)):
    print(d[i, 7], end = ' ')
            
print('dessert:')
for i in range(len(df_dessert)):
    print(e[i, 7], end = ' ')    

        
    