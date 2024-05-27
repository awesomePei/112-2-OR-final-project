import gurobipy as gp
from gurobipy import GRB
import pandas as pd


# 匯入檔案
df_person_data = pd.read_csv('/Users/cindychang/Documents/school/大二/OR/Final/column_person_data_new/person1_data.csv')
W = df_person_data.iloc[0, 0]  
H = df_person_data.iloc[1, 0]
BMI_level = df_person_data.iloc[2, 0]
budget = df_person_data.iloc[3, 0]

df_breakfast = pd.read_csv('/Users/cindychang/Documents/school/大二/OR/Final/final-data/OR Final - Breakfast-final.csv')
df_breakfast.reset_index(drop=True, inplace=True)
n_b = len(df_breakfast.index)

df_food = pd.read_csv('/Users/cindychang/Documents/school/大二/OR/Final/final-data/OR Final - Food-final.csv')
df_food.reset_index(drop=True, inplace=True)
n_f = len(df_food.index)

df_sidemeal = pd.read_csv('/Users/cindychang/Documents/school/大二/OR/Final/final-data/OR Final - Sidemeal-final.csv')
df_sidemeal.reset_index(drop=True, inplace=True)
n_s = len(df_sidemeal.index)

df_beverage = pd.read_csv('/Users/cindychang/Documents/school/大二/OR/Final/final-data/OR Final - Beverage-final.csv')
df_beverage.reset_index(drop=True, inplace=True)
n_d = len(df_beverage.index)

df_dessert = pd.read_csv('/Users/cindychang/Documents/school/大二/OR/Final/final-data/OR Final - Dessert-final.csv')
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


# Model
model = gp.Model("Meal_Planning")

# Decision variables
x = model.addVars(B, K, vtype=GRB.BINARY, name="x")
y = model.addVars(F, [1, 2], K, vtype=GRB.BINARY, name="y")
z = model.addVars(S, [1, 2], K, vtype=GRB.BINARY, name="z")
w = model.addVars(D, K, vtype=GRB.BINARY, name="w")
v = model.addVars(E, K, vtype=GRB.BINARY, name="v")

# Objective function
model.setObjective(
    gp.quicksum(b[i, 6] * x[i, k] for i in B for k in K) +
    gp.quicksum(d[i, 6] * w[i, k] for i in D for k in K) +
    gp.quicksum(e[i, 6] * v[i, k] for i in E for k in K) +
    gp.quicksum(f[i, 6] * y[i, j, k]  for i in F for j in [1, 2] for k in K) +
    gp.quicksum(s[i, 6] * z[i, j, k] for i in S for j in [1, 2] for k in K),
    GRB.MAXIMIZE
)

# Constraints
# Nutrition Constraints
for k in K:
    model.addConstr(
        gp.quicksum(b[i, 1] * x[i, k] for i in B) +
        gp.quicksum(d[i, 1] * w[i, k] for i in D) +
        gp.quicksum(e[i, 1] * v[i, k] for i in E) +
        gp.quicksum(f[i, 1] * y[i, j, k] for i in F for j in [1, 2]) +
        gp.quicksum(s[i, 1] * z[i, j, k] for i in S for j in [1, 2]) <= 
        (40 - BMI_level * 5) * W
    )
    model.addConstr(
        gp.quicksum(b[i, 2] * x[i, k] for i in B) +
        gp.quicksum(d[i, 2] * w[i, k] for i in D) +
        gp.quicksum(e[i, 2] * v[i, k] for i in E) +
        gp.quicksum(f[i, 2] * y[i, j, k] for i in F for j in [1, 2]) +
        gp.quicksum(s[i, 2] * z[i, j, k] for i in S for j in [1, 2]) >= 
        0.8 * W
    )
    model.addConstr(
        gp.quicksum(b[i, 3] * x[i, k] for i in B) +
        gp.quicksum(d[i, 3] * w[i, k] for i in D) +
        gp.quicksum(e[i, 3] * v[i, k] for i in E) +
        gp.quicksum(f[i, 3] * y[i, j, k] for i in F for j in [1, 2]) +
        gp.quicksum(s[i, 3] * z[i, j, k] for i in S for j in [1, 2]) <= 
        2000
    )
    model.addConstr(
        gp.quicksum(b[i, 4] * x[i, k] for i in B) +
        gp.quicksum(d[i, 4] * w[i, k] for i in D) +
        gp.quicksum(e[i, 4] * v[i, k] for i in E) +
        gp.quicksum(f[i, 4] * y[i, j, k] for i in F for j in [1, 2]) +
        gp.quicksum(s[i, 4] * z[i, j, k] for i in S for j in [1, 2]) <= 
        70
    )

# Budget Constraint
model.addConstr(
    gp.quicksum(
        gp.quicksum(b[i, 5] * x[i, k] for i in B) +
        gp.quicksum(d[i, 5] * w[i, k] for i in D) +
        gp.quicksum(e[i, 5] * v[i, k] for i in E) +
        gp.quicksum(f[i, 5] * y[i, j, k] for i in F for j in [1, 2]) +
        gp.quicksum(+ s[i, 5] * z[i, j, k] for i in S for j in [1, 2])
        for k in K
    ) <= budget
)

# Beverage and Dessert Constraints
model.addConstr(gp.quicksum(w[i, k] for i in D for k in K) <= 3)
model.addConstr(gp.quicksum(v[i, k] for i in E for k in K) <= 2)

# Repetition Constraints
for i in F:
    for k in K:
        if k > 1:
            model.addConstr(
                gp.quicksum(y[i, j, k] + y[i, j, k-1] for j in [1, 2]) <= 1
            )

for i in S:
    for k in K:
        if k > 1:
            model.addConstr(
                gp.quicksum(z[i, j, k] + z[i, j, k-1] for j in [1, 2]) <= 1
            )

for i in B:
    for k in K:
        if k > 1:
            model.addConstr(x[i, k] + x[i, k-1] <= 1)

# Meal Completeness Constraints
for k in K:
    model.addConstr(gp.quicksum(x[i, k] for i in B) == 1)
    for j in [1, 2]:
        model.addConstr(gp.quicksum(y[i, j, k] for i in F) == 1)

# Optimize model
model.optimize()

# Print solution
if model.status == GRB.OPTIMAL:
    print("Optimal solution found:")
    for k in K:
        print(f"Day {k}:")
        for i in B:
            if x[i, k].x > 0.5:
                print(f"  Breakfast: {i}")
        for j in [1, 2]:
            for i in F:
                if y[i, j, k].x > 0.5:
                    print(f"  Meal {j}: Food {i}")
            for i in S:
                if z[i, j, k].x > 0.5:
                    print(f"  Meal {j}: Side {i}")
        for i in D:
            if w[i, k].x > 0.5:
                print(f"  Beverage: {i}")
        for i in E:
            if v[i, k].x > 0.5:
                print(f"  Dessert: {i}")
else:
    print("No optimal solution found.")
