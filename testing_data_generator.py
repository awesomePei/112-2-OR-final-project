import csv
import random

# Generate test data for one person
def generate_person_data():
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
    person_data['budget'] = random.uniform(1500.0, 10000.0)
    
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

    return person_data

# Convert person data to a format suitable for CSV
def person_data_to_csv_format(person_data):
    csv_data = [
        ' ',
        person_data['W'],
        person_data['H'],
        person_data['BMI_level'],
        person_data['budget']
    ] + person_data['happiness_index_br'] + person_data['happiness_index_fd'] + person_data['happiness_index_sm'] + person_data['happiness_index_bv'] + person_data['happiness_index_ds']
    return csv_data

# Generate the data
person_data = generate_person_data()
csv_data = person_data_to_csv_format(person_data)

# Transpose the data
transposed_data = list(map(list, zip(*[csv_data])))

# Write the data to a CSV file
with open('person_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write data
    writer.writerows(transposed_data)

print("Data has been written to person_data.csv")
