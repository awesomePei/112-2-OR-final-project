import gurobipy as gp
import pandas as pd


# 匯入檔案
df_person_data = pd.read_csv('person_f5.csv')
W = df_person_data.iloc[0, 0]  
H = df_person_data.iloc[1, 0]
BMI_level = df_person_data.iloc[2, 0]
budget = df_person_data.iloc[3, 0] * 4


cal_con = (40 - BMI_level * 5) * W
p_con = 0.8 * W
sod_con = 3500
sug_con = 70

df_breakfast = pd.read_csv('OR Final - Breakfast-final.csv')
df_breakfast.reset_index(drop = True, inplace = True)
n_b = len(df_breakfast.index)

df_food = pd.read_csv('OR Final - Food-final.csv')
df_food.reset_index(drop = True, inplace = True)
n_f = len(df_food.index)

df_sidemeal = pd.read_csv('OR Final - Sidemeal-final.csv')
df_sidemeal.reset_index(drop = True, inplace = True)
n_s = len(df_sidemeal.index)

df_beverage = pd.read_csv('OR Final - Beverage-final.csv')
df_beverage.reset_index(drop = True, inplace = True)
n_d = len(df_beverage.index)

df_dessert = pd.read_csv('OR Final - Dessert-final.csv')
df_dessert.reset_index(drop = True, inplace = True)
n_e = len(df_dessert.index)

b = {}
for i in range(len(df_breakfast)):
    b[i, 1] = df_breakfast.at[i, 'Calories']
    b[i, 2] = df_breakfast.at[i, 'Protein']
    b[i, 3] = df_breakfast.at[i, 'Sodium']
    b[i, 4] = df_breakfast.at[i, 'Sugar']
    b[i, 5] = df_breakfast.at[i, 'Price']
    b[i, 6] = df_person_data.iloc[i + 4, 0]
    b[i, 7] = 0

f = {}
for i in range(len(df_food)):
    f[i, 1] = df_food.at[i, 'Calories']
    f[i, 2] = df_food.at[i, 'Protein']
    f[i, 3] = df_food.at[i, 'Sodium']
    f[i, 4] = df_food.at[i, 'Sugar']
    f[i, 5] = df_food.at[i, 'Price']
    f[i, 6] = df_person_data.iloc[i + 4 + n_b, 0]
    f[i, 7] = 0

s = {}
for i in range(len(df_sidemeal)):
    s[i, 1] = df_sidemeal.at[i, 'Calories']
    s[i, 2] = df_sidemeal.at[i, 'Protein']
    s[i, 3] = df_sidemeal.at[i, 'Sodium']
    s[i, 4] = df_sidemeal.at[i, 'Sugar']
    s[i, 5] = df_sidemeal.at[i, 'Price']
    s[i, 6] = df_person_data.iloc[i + 4 + n_b + n_f, 0]
    s[i, 7] = 0

d = {}
for i in range(len(df_beverage)):
    d[i, 1] = df_beverage.at[i, 'Calories']
    d[i, 2] = df_beverage.at[i, 'Protein']
    d[i, 3] = df_beverage.at[i, 'Sodium']
    d[i, 4] = df_beverage.at[i, 'Sugar']
    d[i, 5] = df_beverage.at[i, 'Price']
    d[i, 6] = df_person_data.iloc[i + 4 + n_b + n_f + n_s, 0]
    d[i, 7] = 0

e = {}
for i in range(len(df_dessert)):
    e[i, 1] = df_dessert.at[i, 'Calories']
    e[i, 2] = df_dessert.at[i, 'Protein']
    e[i, 3] = df_dessert.at[i, 'Sodium']
    e[i, 4] = df_dessert.at[i, 'Sugar']
    e[i, 5] = df_dessert.at[i, 'Price']
    e[i, 6] = df_person_data.iloc[i + 4 + n_b + n_f + n_s + n_d, 0]
    e[i, 7] = 0
    
selected = {'b': {}, 'f1': {}, 'f2': {}, 's1': {}, 's2': {}, 'd': {}, 'e': {}}
day_cnt = 30

# 餐點統計
daily_calories = [0] * day_cnt
daily_protein = [0] * day_cnt
daily_sodium = [0] * day_cnt
daily_sugar = [0] * day_cnt
daily_cost = [0] * day_cnt
total_cost = 0
total_happiness = 0

# 飲料和甜點限制
drink_count = 0
dessert_count = 0

def check_restrictions_f(day, meal_index, meal_type, daily_calories, daily_protein, daily_sodium, daily_sugar, daily_cost, cal_con, p_con, sod_con, sug_con, budget, drink_count, dessert_count, selected):
    meal = meal_dicts[meal_type]
    if meal[(meal_index, 7)] >= 3:
        return False

    if(meal[(meal_index, 2)] < (0.23*p_con)):
#         print("f false 2-1")
        return False
#     elif(meal[(meal_index, 2)] >= (0.3*p_con)):
#         print(f"Day{day}: {meal_type}, {meal_index}, protein = {meal[meal_index, 2]}")
    elif (daily_calories[day] + meal[(meal_index, 1)] > cal_con):
#         print("f false 2-2")
        return False
    elif(daily_sodium[day] + meal[(meal_index, 3)] > sod_con):
#         print("f false 2-3")
        return False
    elif(daily_sugar[day] + meal[(meal_index, 4)] > sug_con):
#         print("f false 2-4")
        return False
    elif(daily_cost[day] + meal[(meal_index, 5)] > budget/30):
#         print("f false 2-5")
        return False
    
    if meal_type == 'd' and drink_count >= 3:
#         print("f false 3")
        return False
    if meal_type == 'e' and dessert_count >= 2:
#         print("f false 4")
        return False

    if day > 0:
        prev_day_selected = selected[meal_type].get(day-1, -1)
        if prev_day_selected == meal_index:
#             print("f false 5")
            return False

    count = sum(1 for d in range(day_cnt) if selected[meal_type].get(d) == meal_index)
    if count >= 3:
#         print("f false 6")
        return False

    return True

def check_restrictions_s(day, meal_index, meal_type, daily_calories, daily_protein, daily_sodium, daily_sugar, daily_cost, cal_con, p_con, sod_con, sug_con, budget, drink_count, dessert_count, selected):
    meal = meal_dicts[meal_type]
    if meal[(meal_index, 7)] >= 3:
#         print("s false 1")
        return False

    if(meal[(meal_index, 2)] < (0.23*p_con)):
#         print("s false 2-1")
        return False
#     elif(meal[(meal_index, 2)] >= (0.3*p_con)):
#         print(f"Day{day}: {meal_type}, {meal_index}, protein = {meal[meal_index, 2]}")
    elif (daily_calories[day] + meal[(meal_index, 1)] > cal_con):
#         print("s false 2-2")
        return False
    elif(daily_sodium[day] + meal[(meal_index, 3)] > sod_con):
#         print("s false 2-3")
        return False
    elif(daily_sugar[day] + meal[(meal_index, 4)] > sug_con):
#         print("s false 2-4")
        return False
    elif(daily_cost[day] + meal[(meal_index, 5)] > budget/30):
#         print("s false 2-5")
        return False
    
    if meal_type == 'd' and drink_count >= 3:
#         print("s false 3")
        return False
    if meal_type == 'e' and dessert_count >= 2:
#         print("s false 4")
        return False

    if day > 0:
        prev_day_selected = selected[meal_type].get(day-1, -1)
        if prev_day_selected == meal_index:
#             print("s false 5")
            return False

    count = sum(1 for d in range(day_cnt) if selected[meal_type].get(d) == meal_index)
    if count >= 3:
#         print("s false 6")
        return False

    return True

def check_restrictions_b(day, meal_index, meal_type, daily_calories, daily_protein, daily_sodium, daily_sugar, daily_cost, cal_con, p_con, sod_con, sug_con, budget, drink_count, dessert_count, selected):
    meal = meal_dicts[meal_type]
    if meal[(meal_index, 7)] >= 3:
#         print("b false 1")
        return False

    if(meal[(meal_index, 2)] < (0.15*p_con)):
#         print("b false 2-1")
        return False
#     elif(meal[(meal_index, 2)] >= (0.15*p_con)):
#         print(f"Day{day}: {meal_type}, {meal_index}, protein = {meal[meal_index, 2]}")
    elif (daily_calories[day] + meal[(meal_index, 1)] > cal_con):
#         print("b false 2-2")
        return False
    elif(daily_sodium[day] + meal[(meal_index, 3)] > sod_con):
#         print("b false 2-3")
        return False
    elif(daily_sugar[day] + meal[(meal_index, 4)] > sug_con):
#         print("b false 2-4")
        return False
    elif(daily_cost[day] + meal[(meal_index, 5)] > budget/30):
#         print("b false 2-5")
        return False
    
    if meal_type == 'd' and drink_count >= 3:
#         print("b false 3")
        return False
    if meal_type == 'e' and dessert_count >= 2:
#         print("b false 4")
        return False

    if day > 0:
        prev_day_selected = selected[meal_type].get(day-1, -1)
        if prev_day_selected == meal_index:
#             print("b false 5")
            return False

    count = sum(1 for d in range(day_cnt) if selected[meal_type].get(d) == meal_index)
    if count >= 3:
#         print("b false 6")
        return False

    return True

def check_restrictions_d(day, meal_index, meal_type, daily_calories, daily_protein, daily_sodium, daily_sugar, daily_cost, cal_con, p_con, sod_con, sug_con, budget, drink_count, dessert_count, selected):
    meal = meal_dicts[meal_type]

    if (daily_calories[day] + meal[(meal_index, 1)] > cal_con):
#         print(f"{meal_type} false 2-2")
        return False
    elif(daily_sodium[day] + meal[(meal_index, 3)] > sod_con):
#         print(f"{meal_type} false 2-3")
        return False
    elif(daily_sugar[day] + meal[(meal_index, 4)] > sug_con):
#         print(f"{meal_type} false 2-4")
        return False
    elif(daily_cost[day] + meal[(meal_index, 5)] > budget/30):
#         print(f"{meal_type} false 2-5")
        return False
    
    if meal_type == 'd' and drink_count >= 3:
#         print(f"{meal_type} false 3")
        return False
    if meal_type == 'e' and dessert_count >= 2:
#         print(f"{meal_type} false 4")
        return False

    return True

meal_dicts = {'b': b, 'f1': f, 'f2': f, 's1': s, 's2': s, 'd': d, 'e': e}

for day in range(day_cnt):
    print(f"Day {day}:")
    # 選擇早餐
    for meal_index in range(len(df_breakfast)):
        if check_restrictions_b(day, meal_index, 'b', daily_calories, daily_protein, daily_sodium, daily_sugar, daily_cost, cal_con, p_con, sod_con, sug_con, budget, drink_count, dessert_count, selected):
            selected['b'][day] = meal_index
            daily_calories[day] += b[(meal_index, 1)]
            daily_protein[day] += b[(meal_index, 2)]
            daily_sodium[day] += b[(meal_index, 3)]
            daily_sugar[day] += b[(meal_index, 4)]
            daily_cost[day] += b[(meal_index, 5)]
            total_cost += b[(meal_index, 5)]
            total_happiness += b[(meal_index, 6)]
            b[(meal_index, 7)] = 1
            print(f"Selected breakfast {meal_index} for day {day}.")
            break

    # 選擇正餐
    meals_chosen = 0
    for meal_index in range(len(df_food)):
        if meals_chosen == 2:
            break
        if check_restrictions_f(day, meal_index, f'f{meals_chosen+1}', daily_calories, daily_protein, daily_sodium, daily_sugar, daily_cost, cal_con, p_con, sod_con, sug_con, budget, drink_count, dessert_count, selected):
            selected[f'f{meals_chosen+1}'][day] = meal_index
            daily_calories[day] += f[(meal_index, 1)]
            daily_protein[day] += f[(meal_index, 2)]
            daily_sodium[day] += f[(meal_index, 3)]
            daily_sugar[day] += f[(meal_index, 4)]
            daily_cost[day] += f[(meal_index, 5)]
            total_cost += f[(meal_index, 5)]
            total_happiness += f[(meal_index, 6)]
            f[(meal_index, 7)] = 1
            meals_chosen += 1
            print(f"Selected food {meal_index} for day {day}, {meals_chosen}.")

    # 檢查營養需求，添加副餐、飲料或甜點
    sides_chosen = 0
    if (daily_protein[day] < p_con):
        # 選擇副餐
        for meal_index in range(len(df_sidemeal)):
            if sides_chosen == 2:
                break
            if check_restrictions_s(day, meal_index, f's{sides_chosen+1}', daily_calories, daily_protein, daily_sodium, daily_sugar, daily_cost, cal_con, p_con, sod_con, sug_con, budget, drink_count, dessert_count, selected):
                selected[f's{sides_chosen+1}'][day] = meal_index
                daily_calories[day] += s[(meal_index, 1)]
                daily_protein[day] += s[(meal_index, 2)]
                daily_sodium[day] += s[(meal_index, 3)]
                daily_sugar[day] += s[(meal_index, 4)]
                daily_cost[day] += s[(meal_index, 5)]
                total_cost += s[(meal_index, 5)]
                total_happiness += s[(meal_index, 6)]
                s[(meal_index, 7)] = 1
                sides_chosen += 1
                print(f"Selected sidemeal {meal_index} for day {day}, {sides_chosen}.")

    if drink_count < 3:
        # 選擇飲料
        for meal_index in range(len(df_beverage)):
            if check_restrictions_d(day, meal_index, 'd', daily_calories, daily_protein, daily_sodium, daily_sugar, daily_cost, cal_con, p_con, sod_con, sug_con, budget, drink_count, dessert_count, selected):
                selected['d'][day] = meal_index
                daily_calories[day] += d[(meal_index, 1)]
                daily_protein[day] += d[(meal_index, 2)]
                daily_sodium[day] += d[(meal_index, 3)]
                daily_sugar[day] += d[(meal_index, 4)]
                daily_cost[day] += d[(meal_index, 5)]
                total_cost += d[(meal_index, 5)]
                total_happiness += d[(meal_index, 6)]
                drink_count += 1
                d[(meal_index, 7)] = 1
                break

    if dessert_count < 2:
        # 選擇甜點
        for meal_index in range(len(df_dessert)):
            if check_restrictions_d(day, meal_index, 'e', daily_calories, daily_protein, daily_sodium, daily_sugar, daily_cost, cal_con, p_con, sod_con, sug_con, budget, drink_count, dessert_count, selected):
                selected['e'][day] = meal_index
                daily_calories[day] += e[(meal_index, 1)]
                daily_protein[day] += e[(meal_index, 2)]
                daily_sodium[day] += e[(meal_index, 3)]
                daily_sugar[day] += e[(meal_index, 4)]
                daily_cost[day] += e[(meal_index, 5)]
                total_cost += e[(meal_index, 5)]
                total_happiness += e[(meal_index, 6)]
                dessert_count += 1
                e[(meal_index, 7)] = 1
                break

print("Daily protein:", daily_protein)
print("Daily sodium:", daily_sodium)
print("Daily sugar:", daily_sugar)
print("Total happiness:", total_happiness)
print("Total cost:", total_cost)
print(len(selected['b']))
print(len(selected['f1']))
print(len(selected['f2']))
print(len(selected['s1']))
print(len(selected['s2']))
print(selected)
