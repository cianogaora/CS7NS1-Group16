import random
import threading
import time
from fastapi import FastAPI
from threading import Timer
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

# Harshit + Christopher : create classes for meaningful random data generation
class Sensor:
    def __int__(self, sensor_name) -> None:
        self.sensor_name = sensor_name

# class to genrate longitute and latitude data
class Location:
    def __init__(self):
        self.sensor_name = 'Location'
        self.longitude = (random.uniform(-90, 90))
        self.longitude = float(format(self.longitude, '.4f'))
        self.latitude = (random.uniform(-180, 180))
        self.latitude = float(format(self.latitude, ".4f"))
        self.final_loc = {}

    def generate_decimal(self, min, max, numbers):
        self.decimal = (random.uniform(min, max))
        self.decimal = float(format(self.decimal, '.%df' % (numbers)))
        return self.decimal

 #Changing the value of latitude and longitude while making sure they lie within their range 
    def change_longitude(self):

        longitude_change = self.generate_decimal(-1, 1, 4)
        latitude_change = self.generate_decimal(0, 2, 4)

        while True:
            if 90 >= self.longitude + longitude_change >= -90:
                self.longitude = self.longitude + longitude_change
            elif self.longitude + longitude_change > 90:
                self.longitude -= 1
            elif self.longitude + longitude_change < -90:
                self.longitude += 1
            if 180 >= self.latitude + latitude_change >= -180:
                self.latitude = self.latitude + latitude_change
            elif self.latitude + latitude_change > 180:
                self.latitude -= 1
            elif self.latitude + latitude_change < -180:
                self.latitude += 1
            self.final_loc.update({time.strftime(
                "%Y-%m-%d %H:%M:%S"): {"longitude": self.longitude, "latitude": self.latitude}})
            time.sleep(5)

    def generate_location(self):
        t1 = threading.Thread(target=self.change_longitude)
        # print(self.final_loc)
        t1.start()

 #Update the list to add the result       
    def result_location(self):
        # print(self.longitude)
        # print(self.latitude)
        self.loc = {}
        self.loc.update({time.strftime("%Y-%m-%d %H:%M:%S")                        : {"longitude": self.longitude, "latitude": self.latitude}})
        print(self.loc)
        return self.loc

#class for altitude data
class Altitude():

    def __init__(self):
        # self.alt = None
        self.sensor_name = 'Altitude'
        # super().__init__(sensor_name)
        self.altitude = (random.randint(300000, 500000))
        # self.final_alt = {}

    def change_altitude(self):
        number = random.randint(-100, 100)
        while True:
            if self.altitude + number <= 500000 and self.altitude >= 300000:
                self.altitude = self.altitude + number
            elif self.altitude + number < 300000:
                self.altitude += 100
            elif self.altitude + number > 500000:
                self.altitude -= 100
            # self.final_alt.update({time.strftime("%Y-%m-%d %H:%M:%S"):{"altitude":self.altitude}})
            time.sleep(5)

    def generate_altitude(self):
        t1 = threading.Thread(target=self.change_altitude)
        # t1.setDaemon(True)
        # print(self.final_alt)
        t1.start()

    def result_altitude(self):
        self.alt_ = {}
        self.alt_.update({time.strftime("%Y-%m-%d %H:%M:%S")                         : {"altitude": self.altitude}})
        # print(self.alt)
        return self.alt

#class for angle data of satellite
class Angle():

    def __init__(self):
        # self.ang = None
        self.sensor_name = 'Angle'
        self.height_angle = (random.uniform(60, 90))
        self.height_angle = float(format(self.height_angle, '.2f'))
        # self.final_ang = {}

    def generate_decimal(self, min, max, numbers):
        self.decimal = (random.uniform(min, max))
        self.decimal = float(format(self.decimal, '.%df' % (numbers)))
        return self.decimal

    def change_angle(self):
        angle_change = self.generate_decimal(-1, 1, 2)
        while True:
            if 60 <= self.height_angle + angle_change <= 90:
                self.height_angle = self.height_angle + angle_change
            elif self.height_angle < 60:
                self.height_angle += 10
            elif self.height_angle > 90:
                self.height_angle -= 10
            # self.final_ang.update({time.strftime("%Y-%m-%d %H:%M:%S"):{"height angle":self.height_angle}})
            time.sleep(5)

    def generate_angle(self):
        t1 = threading.Thread(target=self.change_angle)
        # print(self.final_ang)
        t1.start()

    def result_anlge(self):
        time.sleep(1)
        self.ang = {}
        self.ang.update({time.strftime("%Y-%m-%d %H:%M:%S")                        : {"height angle": self.height_angle}})
        # print(self.ang)
        return self.ang

#class to generate data for speed of satellite
class Speed():

    def __init__(self):
        # self.spd = None
        self.sensor_name = 'Speed'
        self.speed = (random.uniform(6000, 8000))
        self.speed = float(format(self.speed, '.3f'))
        # self.final_spd = {}

    def generate_decimal(self, min, max, numbers):
        self.decimal = (random.uniform(min, max))
        self.decimal = float(format(self.decimal, '.%df' % (numbers)))
        return self.decimal

    def change_speed(self):
        speed_change = self.generate_decimal(-1, 1, 3)
        while True:
            if 6000 <= self.speed + speed_change <= 8000:
                self.speed = speed_change + self.speed
            elif self.speed < 6000:
                self.speed += 100
            elif self.speed > 8000:
                self.speed -= 100
            # self.final_spd.update({time.strftime("%Y-%m-%d %H:%M:%S"):{"speed":self.speed}})
            time.sleep(5)

    def generate_speed(self):
        t1 = threading.Thread(target=self.change_speed)
        # print(self.final_spd)
        t1.start()

    def result_speed(self):
        self.spd = {}
        self.spd.update(
            {time.strftime("%Y-%m-%d %H:%M:%S"): {"speed": self.speed}})
        # print(self.spd)
        return self.spd

#Eccentricity refers to how much a conic section varies from being circlar eg. circle has eccentricity of 0
class Eccentricity:

    def __init__(self):
        # self.decimal = None
        # self.ecce = None
        self.sensor_name = 'Eccentricity'
        self.eccentricity = (random.uniform(0, 1))
        self.eccentricity = float(format(self.eccentricity, '.2f'))
        # self.final_ecc = {}

    def generate_decimal(self, min, max, numbers):
        self.decimal = (random.uniform(min, max))
        self.decimal = float(format(self.decimal, '.%df' % (numbers)))
        return self.decimal

    def change_eccentricity(self):
        eccentricity_change = self.generate_decimal(-1, 1, 2)
        while True:
            if 0 <= self.eccentricity + eccentricity_change <= 1:
                self.eccentricity = self.eccentricity + eccentricity_change
            elif self.eccentricity + eccentricity_change > 1:
                self.eccentricity -= 0.2
            elif self.eccentricity + eccentricity_change < 0:
                self.eccentricity += 0.2
            # self.final_ecc.update({time.strftime("%Y-%m-%d %H:%M:%S"):{"Orbital eccentricity":self.eccentricity}})
            time.sleep(5)

    def generate_eccentricity(self):
        t1 = threading.Thread(target=self.change_eccentricity)
        t1.start()

    def result_eccentricity(self):
        self.ecce = {}
        self.ecce.update({time.strftime("%Y-%m-%d %H:%M:%S"): {"Orbital eccentricity": self.eccentricity}})
        # print(self.ecce)
        return self.ecce

#class that gives temperature at the surface of the satellite:varies as its distance and face from the sun
class Temperature:

    def __init__(self):
        # self.temp = None
        # self.decimal = None
        self.sensor_name = 'temperature'
        self.temperature = (random.uniform(-100, 100))
        self.temperature = float(format(self.temperature, '.2f'))
        # self.final_temp = {}

    def generate_decimal(self, min, max, numbers):
        self.decimal = (random.uniform(min, max))
        self.decimal = float(format(self.decimal, '.%df' % (numbers)))
        return self.decimal

    def change_temperature(self):
        temperature_change = self.generate_decimal(-5, 5, 2)
        while True:
            if -100 <= temperature_change + self.temperature <= 100:
                self.temperature = self.temperature + temperature_change
            elif self.temperature + temperature_change < -100:
                self.temperature += 5
            elif self.temperature + temperature_change > 100:
                self.temperature += 5
            # self.final_temp.update({time.strftime("%Y-%m-%d %H:%M:%S"):{"temperature":self.temperature}})
            time.sleep(5)

    def generate_temperature(self):
        t1 = threading.Thread(target=self.change_temperature)
        t1.start()

    def result_temperature(self):
        self.temp = {}
        self.temp.update({time.strftime("%Y-%m-%d %H:%M:%S"): {"temperature": self.temperature}})
        return self.temp

#class to give the signal strength from the satellite
class Signal:
    def __init__(self):
        # self.decimal = None
        # self.sig = None
        self.sensor_name = 'Singal'
        self.signal_strength = (random.uniform(-114.58, -102.27))
        self.signal_strength = float(format(self.signal_strength, '.2f'))

    def generate_decimal(self, min, max, numbers):
        self.decimal = (random.uniform(min, max))
        self.decimal = float(format(self.decimal, '.%df' % (numbers)))
        return self.decimal

    def change_singal(self):
        signal_change = self.generate_decimal(-3, 3, 2)
        while True:
            if -114.58 <= self.signal_strength + signal_change <= -102.27:
                self.signal_strength = self.signal_strength + signal_change
            elif self.signal_strength + signal_change < -114.58:
                self.signal_strength += 3
            elif self.signal_strength + signal_change > -102.27:
                self.signal_strength -= 3
            time.sleep(5)

    def generate_signal(self):
        t1 = threading.Thread(target=self.change_singal)
        t1.start()

    def result_signal(self):
        self.sig = {}
        self.sig.update({time.strftime("%Y-%m-%d %H:%M:%S")                        : {"signal_strength": self.signal_strength}})
        print(self.sig)
        return self.sig

#class depicting microwave radiation 
class Microwave:
    def __init__(self):
        self.sensor_name = "Microwave"
        self.microwave_radiation = random.randint(300, 300000)

    def change_microwave(self):
        microave_change = random.randint(-10, 10)
        while True:
            if 300 <= self.microwave_radiation + microave_change <= 300000:
                self.microwave_radiation = self.microwave_radiation + microave_change
            elif self.microwave_radiation + microave_change < 300:
                self.microwave_radiation += 10
            elif self.microwave_radiation + microave_change > 300000:
                self.microwave_radiation -= 10
            time.sleep(5)

    def generate_microwave(self):
        t1 = threading.Thread(target=self.change_microwave)
        t1.start()

    def result_microwave(self):
        self.mic = {}
        self.mic.update({time.strftime("%Y-%m-%d %H:%M:%S")                        : {"microwave radiation": self.microwave_radiation}})
        print(self.mic)
        return self.mic


# if __name__ == '__main__':
#     # sensor1 = Location()
#     # sensor2 = Angle()
#     # sensor3 = Speed()
#     # sensor4 = Altitude()
#     # sensor6 = Signal()
#     # sensor2.generate_angle()
#     # sensor5 = Eccentricity()
#     # sensor5.generate_eccentricity()
#     # sensor6.generate_signal()
#     # sensor7 = Microwave()
#     # sensor7.generate_microwave()
#     # while True:
#     #     # sensor1.generate_location()
#     #     # sensor1.result_location()
#     #
#     #     # sensor2.result_anlge()
#     #     # sensor3.generate_speed()
#     #     # sensor3.result_speed()
#     #     # sensor4.generate_altitude()
#     #     # sensor4.result_altitude()
#     #     # sensor6.result_signal()
#     #     sensor7.result_microwave()
#     #     time.sleep(5)
