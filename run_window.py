import window
import csv

windows = []

with open('window_data.txt', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        w = window.Window(
            id=row["id"],
            preferred_temperature=row["pref_temp"],
            curtain_time=row["curtain_time"]
        )
        windows.append(w)

while True:
    """
    Run Window
    """