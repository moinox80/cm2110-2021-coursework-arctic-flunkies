import window as w 
import Weather_api as wa
import window_mechanism as wm
import csv

window = w.window()
api = wa.weatherApi()
window_mechanism = wm.window_mechanism()

with open('user_data.txt', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        line_count += 1
    
    if line_count > 1:
        preferred_temp = int(input("Welcome to SmartWindow, please input your preferred home temperature: "))
        window.setPreferredTemperature(preferred_temp)
        city = input("Now input the city you live in")
        api.set_city(city)
    else:
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            api.set_city(row["city"])
            window.setPreferredTemperature(int(row["preferred_temp"]))
            line_count += 1
            
while True:
    
    dashboard = input("-=SmartWindow=-  \n[1] Run window \n[2] Check weather \n[3] Open window \n[4] Close window \n[5] Close app\n")

    if dashboard == "1":
        window.window.work()
    elif dashboard == "2":
       print(api.get_weather_data())
    elif dashboard == "3":
        window_mechanism.open_window()
    elif dashboard == "4":
        window_mechanism.close_window()  
    elif dashboard == "5":
        with open('user_data.txt', mode='w') as csv_file:
            fieldnames = ['preferred_temp', 'city']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'preferred_temp': self.__preferred_temperature})
            writer.writerow({'city': api.get_city()})
        break

