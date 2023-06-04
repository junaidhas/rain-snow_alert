import requests
from twilio.rest import Client
import os


API_key =os.environ.get("API_KEY")

WEATHER_API_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"


MY_LAT = 52.133213
MY_LONG = -106.670044

TRILLIO_PHONE_NUMBER =os.environ.get("TRILLIO_PHONE_NUMBER")
account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")
MY_PHONE_NUMBER = os.environ.get("MY_PHONE_NUMBER")

# to set environment variables, In pycharm -->run-->edit configuration ---> add environment variables --> rule is type the variable 
#followed with equal to sign and value with no spaces
#while calling it in main function, import os, get the env variable inside a string

parameters = {
    "lat":MY_LAT,
    "lon":MY_LONG,
    "appid":API_key,
    "exclude":"current,minutely,daily"

}
# calling the API using requests module
response1 = requests.get(WEATHER_API_ENDPOINT,params=parameters)
response1.raise_for_status()

data = response1.json()

#slicing---> getting the data of the big json file for 0-12 hours, 
weather_data_sliced = data["hourly"][0:12]
#0:12 will get hourly details of 0,1,2..11 i.e (12-1)
print(weather_data_sliced)


will_rain_or_snow = False

# in Open weather map, weather id for rainy or snowy condition is less than 700 above 800 means it's not raining or snowing
for hour in weather_data_sliced:
    #hour = 0,1,2,3....11
    weather_id = hour["weather"][0]["id"]
    print(weather_id)
    if weather_id < 700:
        will_rain_or_snow = True

 # sending the sms from a trillio virual number to my phone number, this code below is code for sending sms from triilio  
if will_rain_or_snow:
    client = Client(account_sid,auth_token)
    message = client.messages \
        .create(
        body="its going to rain or snow!,🌧 Please carry a jacket or umbrella ☔",
        from_=TRILLIO_PHONE_NUMBER,
        to=MY_PHONE_NUMBER
    )
    print(message.status)

#Rough
# data = data["hourly"][0]["weather"][0]["id"]
#
#
# for i in range(10):
#     if data["hourly"][i]["weather"][0]["id"]:
#         print("its going to rain or snow!, Please carry an umbrella")
#     else:
#         print("It's not raining")
