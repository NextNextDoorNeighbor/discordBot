import json
import requests

def curWeath(zipcode):
    url = 'https://api.openweathermap.org/data/2.5/weather?zip={},us&appid=9a5a4353163c0c15faf3e6cc7d2ce583'.format(zipcode)
    response = requests.get(url)
    valJSON = response.json()
    valTempK = float(valJSON['main'] ['temp'])
    valTempF = round(float(valTempK * 9/5 - 459.67))
    valDescr = valJSON['weather'][0] ['description']
    valWindSpeed= float(valJSON['wind']['speed'])
    output = "Current weather in your area: \n Temperature: " + str(valTempF)+' F \n Forecast: '+ str(valDescr)+ '\n Wind Speed: ' + str(valWindSpeed)+ 'mph\n'
    return output