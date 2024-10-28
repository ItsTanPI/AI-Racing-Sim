import csv
import vectorMath
import vectorMath as VM

def csv_to_vector2_list(file_path):
    vector2_list = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            x, y = map(float, row)
            vector2_list.append(VM.Vector2(x, y))
    return vector2_list

# Replace 'file1.csv' and 'file2.csv' with the paths to your CSV files
file1_path = r'assets\Env\C.csv'
file2_path = r'assets\Env\I.csv'

Central = csv_to_vector2_list(file1_path)
Inflated = csv_to_vector2_list(file2_path)