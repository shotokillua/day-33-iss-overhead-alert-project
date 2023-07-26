# import requests
# from datetime import datetime
#
# MY_LAT = 51.507351
# MY_LONG = -0.127758
# # response = requests.get(url="http://api.open-notify.org/iss-now.json")
# ## Instead of trying to raise an exception fo revery single possible status code and telling the developer what might
# ## be the reason... we can just use .raise_for_status() method
#
# # if response != 200:
# #     raise Exception("Bad response from ISS API")
# #response.raise_for_status() # this works much better than raising exceptions for every error
#
# # longitude = response.json()["iss_position"]["longitude"]
# # latitude = response.json()["iss_position"]["latitude"]
# # iss_position = (latitude, longitude)
# # print(iss_position)
#
# parameters = {
#     "lat": MY_LAT,
#     "lng": MY_LONG,
#     "formatted": 0,
# }
#
# response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
# response.raise_for_status()
# data = response.json()["results"]
#
# #you can further split items by accessing the index of the list that the .split() method generates
# sunrise = data["sunrise"].split("T")[1].split(":")[0]
# sunset = data["sunset"].split("T")[1].split(":")[0]
#
# print(sunrise)
# print(sunset)
#
# time_now = datetime.now()
# print(time_now.hour)

import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 51.507351
MY_LONG = -0.127758
MY_EMAIL = "shotokillua55@gmail.com"
MY_PASSWORD = "***"



def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the iss position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com", port=587)
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Look Up👆\n\nThe ISS is above you in the sky."
        )