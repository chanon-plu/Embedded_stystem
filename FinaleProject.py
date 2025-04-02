import time
import schedule
import datetime
import board
import busio
import os
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_dht
import lcddriver
from gpiozero import Servo
import RPi.GPIO as GPIO

os.system("sudo killall libgpiod_pulsein")

GPIO.cleanup()
time.sleep(4)

display = lcddriver.lcd()
servo = Servo(17, min_pulse_width=0.0005, max_pulse_width=0.0025)



# Initialize I2C for ADS1115 (Soil Moisture Sensor)
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
soil_sensor = AnalogIn(ads, ADS.P0)  # Using A0 for soil moisture

# Initialize I2C for ADS1115 (Soil Moisture Sensor)
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
soil_sensor = AnalogIn(ads, ADS.P0)  # Using A0 for soil moisture

# Initialize DHT11 sensor (Set GPIO Pin)
dht_pin = board.D4  
dht11 = adafruit_dht.DHT11(dht_pin)



# Function to convert ADC to moisture percentage
def adc_to_moisture(adc_value):
    wet_adc = 7300   # 100% moisture
    dry_adc = 17800  # 0% moisture
    moisture = (dry_adc - adc_value) / (dry_adc - wet_adc) * 100
    return max(0, min(100, moisture))  # Ensure range is 0-100%

def displayFace():
    now = datetime.datetime.now()
    hour = now.hour
            
    if hour < 12:
        line1 = " (^¬^)/ Good    "
        line2 = "  ( )   Morning "
    elif hour < 18:
        line1= " (^¬^)/Good     "
        line2= "  ( )  Afternoon"
    else:
        line1= " (^¬^)/ Good    "
        line2= "  ( )   Night   "
            
    display.lcd_display_string(line1, 1)
    display.lcd_display_string(line2,2)
    time.sleep(2)
    
def displayValue(temperature,humidity):
    TempAndHumi = "T: "+str(temperature)+"C "+"H: "+str(humidity)+"%"
    str_Temp = TempAndHumi.ljust(16)
    MoistFormat = "{:.2f}".format(moisture_percent)
    str_Moist = "Moist:"+MoistFormat+"%"
    display_Moist = str_Moist.ljust(16)
    display.lcd_display_string(str_Temp, 1)
    display.lcd_display_string(display_Moist, 2)
    
    time.sleep(2)

def RunningServo():
    # Turn servo clockwise (full speed) for 0.18 sec
    servo.value = -1  
    time.sleep(2)
    # Turn servo counterclockwise (full speed) for 0.18 sec
    servo.value = 1  
    time.sleep(2)
    #Stop the servo
    servo.value = 0
    
def scheduled_watering():
    temperature = dht11.temperature
    humidity = dht11.humidity
    if temperature is not None and humidity is not None:  # Ensure valid readings
        Watering(temperature, humidity)
    else:
        print("Skipping watering due to sensor error.")

schedule.every(1).minute.do(scheduled_watering)

try:
    while True:
        try:
            # Read soil moisture
            adc_value = soil_sensor.value
            moisture_percent = adc_to_moisture(adc_value)

            # Read temperature & humidity
            temperature = dht11.temperature
            humidity = dht11.humidity

            # Display results
            print(f"Soil Moisture: {moisture_percent:.2f}%")
            print(f"Temperature: {temperature:.1f}°C")
            print(f"Humidity: {humidity:.1f}%\n")
            
            displayFace()
            
            displayValue(temperature,humidity)
            
            schedule.run_pending()

        except RuntimeError as e:
            print(f"Sensor error: {e}")  # Handle occasional DHT11 errors

        # Wait before next reading
        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    GPIO.cleanup()  # Proper cleanup when exiting

