import pandas as pd # type: ignore

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
        
for i in range(len(df_sidemeal)):
    if s[i, 1] < 0.25*cal_con and f[i, 3] < 0.25*sod_con and f[i, 4] < 0.1*sug_con and f[i, 5] < 0.2*budget:
        s[i, 7] = 1
    else:
        s[i, 7] = 0
        
for i in range(len(df_beverage)):
    if d[i, 1] < 0.15*cal_con and d[i, 3] < 0.1*sod_con and d[i, 4] < 0.45*sug_con and d[i, 5] < 0.12*budget:
        d[i, 7] = 1
    else:
        d[i, 7] = 0
        
for i in range(len(df_dessert)):
    if e[i, 1] < 0.2*cal_con and e[i, 2] > 0.04*p_con and e[i, 3] < 0.1*sod_con and e[i, 4] < 0.45*sug_con and e[i, 5] < 0.12*budget:
        e[i, 7] = 1
    else:
        e[i, 7] = 0
        
        
# #  # Print the result
# print('breakfast:')
# for i in range(len(df_breakfast)):
#     print(b[i, 7], end = ' ')
        
# print('lunch:')
# for i in range(len(df_food)):
#     print(f[i, 7], end = ' ')
    
# print('sidemeal:')
# for i in range(len(df_sidemeal)):
#     print(s[i, 7], end = ' ')
            
# print('beverage:')
# for i in range(len(df_beverage)):
#     print(d[i, 7], end = ' ')
            
# print('dessert:')
# for i in range(len(df_dessert)):
#     print(e[i, 7], end = ' ')    

# breakfast_list = [(i, b[i, 1], b[i, 2], b[i, 3], b[i, 4], b[i, 5], b[i, 6], b[i, 7]) for i in range(len(df_breakfast)) if (i, 1) in b]
# sorted_breakfast = sorted(breakfast_list, key=lambda x: (x[7], x[6]), reverse=True)

# for breakfast in sorted_breakfast:
#     print(f"Breakfast ID: {breakfast[0]}, Details: {breakfast}")
 
 
happiness = 0   
cal = 0
pro = 0
sod = 0
sug = 0
mon = 0
    
    
print(happiness)  

breakfast_list = [(i, b[i, 1], b[i, 2], b[i, 3], b[i, 4], b[i, 5], b[i, 6], b[i, 7]) for i in range(len(df_breakfast)) if (i, 1) in b]
sorted_breakfast = sorted(breakfast_list, key=lambda x: (x[7], x[6]), reverse=True)


# Print only the top twelve breakfasts with day labels
for index, breakfast in enumerate(sorted_breakfast[:12]):
    if breakfast[0] == 0:
        continue
    else:
        print(f"Day{index + 1}: Breakfast ID: {breakfast[0]}, Happiness: {breakfast[6]}")
        happiness += breakfast[6]
        print(happiness) 
        cal += breakfast[1]
        pro += breakfast[2]
        sod += breakfast[3]
        sug += breakfast[4]
        mon += breakfast[5]
  
    

food_list = [(i, f[i, 1], f[i, 2], f[i, 3], f[i, 4], f[i, 5], f[i, 6], f[i, 7]) for i in range(len(df_food)) if (i, 1) in f]
sorted_food = sorted(food_list, key=lambda x: (x[7], x[6]), reverse=True)
for index, food in enumerate(sorted_food[:12]):
    #print(f"Day{index + 1}: Lucnh ID: {food[0]}, Happiness: {food[6]}")
    happiness += food[6]
    cal += food[1]
    pro += food[2]
    sod += food[3]
    sug += food[4]
    mon += food[5]
    


for index, food in enumerate(sorted_food[:12]):
    #print(f"Day{30 - index }: Dinner ID: {food[0]}, Happiness: {food[6]}")
    happiness += food[6]
    cal += food[1]
    pro += food[2]
    sod += food[3]
    sug += food[4]
    mon += food[5]
    
  
    
    
sidemeal_list = [(i, s[i, 1], s[i, 2], s[i, 3], s[i, 4], s[i, 5], s[i, 6], s[i, 7]) for i in range(len(df_sidemeal)) if (i, 1) in s]
sorted_sidemeal = sorted(sidemeal_list, key=lambda x: (x[7], x[6]), reverse=True)
for index, sidemeal in enumerate(sorted_sidemeal[:12]):
    #print(f"Day{index + 1}: Sidemeal ID: {sidemeal[0]}, Happiness: {sidemeal[6]}")
    happiness += sidemeal[6]
    cal += sidemeal[1]
    pro += sidemeal[2]
    sod += sidemeal[3]
    sug += sidemeal[4]
    mon += sidemeal[5]
    
    


beverage_list = [(i, d[i, 1], d[i, 2], d[i, 3], d[i, 4], d[i, 5], d[i, 6], d[i, 7]) for i in range(len(df_beverage)) if (i, 1) in d]
sorted_beverage = sorted(beverage_list, key=lambda x: (x[7], x[6]), reverse=True)
for index, beverage in enumerate(sorted_beverage[:12]):
    #print(f"Day{index + 1}: Beverage ID: {beverage[0]}, Happiness: {beverage[6]}")
    happiness += beverage[6]
    cal += beverage[1]
    pro += beverage[2]
    sod += beverage[3]
    sug += beverage[4]
    mon += beverage[5]
    
  
    
    
dessert_list = [(i, e[i, 1], e[i, 2], e[i, 3], e[i, 4], e[i, 5], e[i, 6], e[i, 7]) for i in range(len(df_dessert)) if (i, 1) in e]
sorted_desserts = sorted(dessert_list, key=lambda x: (x[7], x[6]), reverse=True)
for index, dessert in enumerate(sorted_desserts[:12]):
    # print(f"Day{index + 1}: Dessert ID: {dessert[0]}, Happiness: {dessert[6]}")
    happiness += dessert[6]
    cal += dessert[1]
    pro += dessert[2]
    sod += dessert[3]
    sug += dessert[4]
    mon += dessert[5]
  

print(f"Total Happiness: {happiness*30/12}")
print(cal_con*30 - cal*30/12)
print(p_con*30 - pro*30/12)
print(sod_con*30 - sod*30/12)
print(sug_con*30 - sug*30/12)
print(budget - mon*30/12)
    