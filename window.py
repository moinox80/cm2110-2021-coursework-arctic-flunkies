import window_mechanism as wm 
import TemperatureSensor as ts 
class window():

    def __init__(self):
        self._window_mechanism = wm.window_mechanism()
        self._temp_sensor = ts.TemperatureSensor()
        self._run_window = int(input("Input your preferred temperature"))
    
    def window_work(self):
        #When  room temperature is higher than the preferred temperature and room temperature is lower than outside
        if (self._temp_sensor.get_room_temperature() > self._run_window) and (self._temp_sensor.get_room_temperature() > self._temp_sensor.get_outside_temperature()):
            self._window_mechanism.open_window()
            while True:
                if self._temp_sensor.get_room_temperature() > self._run_window:
                    print("loop 1")
                    self._temp_sensor.set_room_temperature(self._temp_sensor.get_room_temperature() - 1)
                    print(self._temp_sensor.get_room_temperature())
                else:
                    self._window_mechanism.close_window()
                    print("Temperature stabilized")
                    break
        #When room temperature is lower than preferred temperature and room temperature is higher than outside.
        elif self._temp_sensor.get_room_temperature() < self._run_window and self._temp_sensor.get_room_temperature() > self._temp_sensor.get_outside_temperature():
              self._window_mechanism.close_window()
              while True:
                if self._temp_sensor.get_room_temperature() < self._run_window:
                    print("loop 2")
                    self._temp_sensor.set_room_temperature(self._temp_sensor.get_room_temperature() + 1)
                    print("Heating room: " + str(self._temp_sensor.get_room_temperature()))
                else:
                    print("Temperature stabilized")
                    break
        #When room temperature is lower than preferred temperature and room temperature is lower than outside
        elif self._temp_sensor.get_room_temperature() < self._run_window and self._temp_sensor.get_room_temperature() < self._temp_sensor.get_outside_temperature():
              self._window_mechanism.open_window()
              while True:
                if self._temp_sensor.get_room_temperature() < self._run_window:
                    print("loop 3")
                    self._temp_sensor.set_room_temperature(self._temp_sensor.get_room_temperature() + 1)
                else:
                    self._window_mechanism.close_window()
                    print("Temperature stabilized")
                    break
        #When room temperature is higher than preferred temperature and room temperature is lower than outside
        elif self._temp_sensor.get_room_temperature() > self._run_window and self._temp_sensor.get_room_temperature() < self._temp_sensor.get_outside_temperature():
            print("Air Conditioner turned on")
            while True:
                if self._temp_sensor.get_room_temperature() > self._run_window:
                    print("loop 4")
                    self._temp_sensor.set_room_temperature(self._temp_sensor.get_room_temperature() + 1)
                else:
                    print("Temperature stabilized")
                    break