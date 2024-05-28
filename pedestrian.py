import random
import pandas as pd #type: ignore

# 簡單的演算法，隨機選擇食物，並計算總幸福感
def simple_random_meal_planning(df_breakfast, df_food, df_sidemeal, df_beverage, df_dessert, df_person_data, days):
    total_happiness = 0
    plan = {}
    for day in range(1, days+1):
        breakfast = random.choice(df_breakfast.index)
        main_meal1 = random.choice(df_food.index)
        side_meal1 = random.choice(df_sidemeal.index)
        main_meal2 = random.choice(df_food.index)
        side_meal2 = random.choice(df_sidemeal.index)
        beverage = random.choice(df_beverage.index)
        dessert = random.choice(df_dessert.index)
        
        day_happiness = (
            df_person_data.iloc[breakfast + 4, 0] +
            df_person_data.iloc[main_meal1 + 4 + len(df_breakfast), 0] +
            df_person_data.iloc[side_meal1 + 4 + len(df_breakfast) + len(df_food), 0] +
            df_person_data.iloc[main_meal2 + 4 + len(df_breakfast), 0] +
            df_person_data.iloc[side_meal2 + 4 + len(df_breakfast) + len(df_food), 0] +
            df_person_data.iloc[beverage + 4 + len(df_breakfast) + len(df_food) + len(df_sidemeal), 0] +
            df_person_data.iloc[dessert + 4 + len(df_breakfast) + len(df_food) + len(df_sidemeal) + len(df_beverage), 0]
        )
        
        total_happiness += day_happiness
        plan[day] = {
            'Breakfast': breakfast,
            'Main Meal 1': main_meal1,
            'Side Meal 1': side_meal1,
            'Main Meal 2': main_meal2,
            'Side Meal 2': side_meal2,
            'Beverage': beverage,
            'Dessert': dessert,
            'Day Happiness': day_happiness
        }
    
    return plan, total_happiness



# 匯入檔案
df_person_data = pd.read_csv('/Users/sophiehuang/Downloads/five_female_data/person_f5.csv')
W = df_person_data.iloc[0, 0]  
H = df_person_data.iloc[1, 0]
BMI_level = df_person_data.iloc[2, 0]
budget = df_person_data.iloc[3, 0]

budget = budget * 30/7


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
    b[i, 6] = df_person_data.iloc[i + 3, 0] ## happiness
    
    


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

# 使用簡單演算法計劃一週餐點
meal_plan, total_happiness = simple_random_meal_planning(df_breakfast, df_food, df_sidemeal, df_beverage, df_dessert, df_person_data, 7)

# 印出每天的餐點計劃以及總幸福感
print(f"Total Happiness for the Week: {total_happiness}")
# for day, meals in meal_plan.items():
#     print(f"Day {day}:")
#     print(f"  Breakfast: {meals['Breakfast']} (Happiness: {df_person_data.iloc[meals['Breakfast'] + 4, 0]})")
#     print(f"  Main Meal 1: Food {meals['Main Meal 1']} (Happiness: {df_person_data.iloc[meals['Main Meal 1'] + 4 + len(df_breakfast), 0]}), Side {meals['Side Meal 1']} (Happiness: {df_person_data.iloc[meals['Side Meal 1'] + 4 + len(df_breakfast) + len(df_food), 0]})")
#     print(f"  Main Meal 2: Food {meals['Main Meal 2']} (Happiness: {df_person_data.iloc[meals['Main Meal 2'] + 4 + len(df_breakfast), 0]}), Side {meals['Side Meal 2']} (Happiness: {df_person_data.iloc[meals['Side Meal 2'] + 4 + len(df_breakfast) + len(df_food), 0]})")
#     print(f"  Beverage: {meals['Beverage']} (Happiness: {df_person_data.iloc[meals['Beverage'] + 4 + len(df_breakfast) + len(df_food) + len(df_sidemeal), 0]})")
#     print(f"  Dessert: {meals['Dessert']} (Happiness: {df_person_data.iloc[meals['Dessert'] + 4 + len(df_breakfast) + len(df_food) + len(df_sidemeal) + len(df_beverage), 0]})")
#     print(f"  Day Happiness: {meals['Day Happiness']}")
