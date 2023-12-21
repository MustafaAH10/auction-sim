import csv

# # Read player names from the CSV file
# with open("pastplayers.csv", "r", encoding="utf-8-sig") as file:
#     reader = csv.reader(file)
#     player_names = [
#         row[0] for row in reader
#     ]  # Adjust depending on the structure of your CSV
#     # print(player_names)

# new_players = list(set(player_names))
# print(new_players)

# with open("oldplayers.csv", mode="w", newline="") as file:
#     # Create a CSV writer
#     writer = csv.writer(file)

#     for name in new_players:
#         writer.writerow([name])


import csv


# Function to read names from a CSV file and return them as a list
def read_names_from_csv(file_path):
    names = []
    with open(file_path, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            names.extend(row)
    return names


# Function to write a list of names to a CSV file
def write_names_to_csv(file_path, names):
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        for name in names:
            writer.writerow([name])


# File paths for your two CSV files
csv_file1_path = "players.csv"
csv_file2_path = "oldplayers.csv"

# Read names from both CSV files
names_list1 = read_names_from_csv(csv_file1_path)
names_list2 = read_names_from_csv(csv_file2_path)

# Identify common names
common_names = set(names_list1) & set(names_list2)

if common_names:
    print("Common names found:", common_names)

    # Remove common names from one of the lists (let's remove from names_list2)
    updated_names_list2 = [name for name in names_list2 if name not in common_names]

    # Write the updated list back to the second CSV file
    write_names_to_csv(csv_file2_path, updated_names_list2)
    print("Common names removed from", csv_file1_path)
else:
    print("No common names found.")
