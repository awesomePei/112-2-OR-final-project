# -*- coding: utf-8 -*-
"""
Created on Mon May 27 09:11:48 2024

@author: TPJ
"""

import random

# Generate test data for one person
person_data = {}

# Weight (W) in kilograms
person_data['W'] = random.uniform(30.0, 120.0)

# BMI Level (1: underweight, 2: normal weight, 3: overweight)
person_data['H'] = random.uniform(1.2, 2.2)
BMI = person_data['W'] / (person_data['H'] ** 2)

if BMI < 18.5:
    person_data['BMI_level'] = 1  # Underweight
elif 18.5 <= BMI < 24:
    person_data['BMI_level'] = 2  # Normal weight
else:
    person_data['BMI_level'] = 3  # Overweight
    
# Monthly budget for food in dollars
person_data['budget'] = random.uniform(200.0, 1500.0)

# Happiness index for each food item (range 0 to 10)
# breakfast
person_data['happiness_index_br'] = [random.randint(0, 10) for _ in range(86)]
# food
person_data['happiness_index_fd'] = [random.randint(0, 10) for _ in range(103)]
# side meal
person_data['happiness_index_sm'] = [random.randint(0, 10) for _ in range(51)]
# beverage
person_data['happiness_index_bv'] = [random.randint(0, 10) for _ in range(87)]
# dessert
person_data['happiness_index_ds'] = [random.randint(0, 10) for _ in range(55)]

# Output the generated test data
print(person_data)
