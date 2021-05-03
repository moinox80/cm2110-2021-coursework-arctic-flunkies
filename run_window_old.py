import window as w 
import Weather_api as wa
import window_mechanism as wm
import curtain as c
import os
import csv

window = w.Window()
api = wa.WeatherApi()
window_mechanism = wm.WindowMechanism()
curtain = c.Curtain()

with open('user_data.txt', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        line_count += 1
    
    if line_count < 1:
        preferred_temp = int(input("Welcome to MyWindow, please input your preferred home temperature: "))
        window.set_preferred_temperature(preferred_temp)
        
    else:
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
        window.set_preferred_temperature(row["temp"])
        api.set_city(row["city"])
        
        line_count += 1

        
        
            
while True:
    print("   [Time]")
    print("-=" + curtain.get_time() + "=-")

    if curtain.run_curtain() == 1:
        print("Curtains are currently opened")
    elif curtain.run_curtain() == 0:
        print("Curtains are currently closed")
    dashboard = input("-=MyWindow=-  \n[1] Run window \n[2] Check weather \n[3] Open window \n[4] Close window \n[5] Change city and preferred temperature \n[6] Close app\n")
    

    if dashboard == "1":
        window.window_work()
    elif dashboard == "2":
        print(api.get_weather_data())
    elif dashboard == "3":
        window_mechanism.open_window()
    elif dashboard == "4":
        window_mechanism.close_window()  
    elif dashboard == "5":
        f = open('user_data.txt', 'r+')
        f.truncate(0)
        f.close()
        city = input("Please input your city: ")
        temp = int(input("Please input the your preferred temperature: "))
        api.set_city(city)
        window.set_preferred_temperature(temp)
        with open('user_data.txt', mode='w') as csv_file:
            fieldnames = ['city']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'city': api.get_city()})
        
        print("Changes saved, please restart the program")
        break
    elif dashboard == "6":
        with open('user_data.txt', mode='w') as csv_file:
            fieldnames = ['city']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'city': api.get_city()}) 
        break


