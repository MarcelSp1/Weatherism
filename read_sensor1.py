import time
import board
import adafruit_dht
import csv
from datetime import datetime

# Funktion um den Sensor auszulesen
def get_temp_hmd():
    #Den DHT22 initiieren
    dhtDevice = adafruit_dht.DHT22(board.D2)

    # Lese den Sensor so lange aus, bis die Daten abgerufen werden können
    while True:
        try:
            # Temperatur in Grad Celsius
            temperature_c = dhtDevice.temperature
            # Luftfeuchtigkeit
            humidity = dhtDevice.humidity
            return temperature_c, humidity

        except RuntimeError as error:
            # Wenn Error: einfach nochmal versuchen (-> schwieriges Auslesen)
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error

# Notiere das Datum, die Zeit, die Luftfeuchtigkeit und die Temperatur in csv_data/humidity_and_temperature.csv
def note_data(temp, hmd):
    temperature, humidity = temp, hmd
    date = datetime.now()
    extracted_date = date.date()
    time = date.time()
    data = [[extracted_date, time, humidity, temperature]]
    with open("csv_data/humidity_and_temperature.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Notiere alle zwei Minuten die dafür ausgelesenen Daten
def main_cycle():
    while True:
        prep_time = datetime.now()
        prep_time = prep_time.time()
        prep_time = str(prep_time)
        prep_time = prep_time.split(":")
        time_minute = int(prep_time[1])
        if (time_minute % 2 == 0):
            temp, hmd = get_temp_hmd()
            note_data(temp, hmd)

main_cycle()
