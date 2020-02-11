from tkinter import *
from PIL import ImageTk, Image
import requests
import json


root = Tk()
root.geometry("600x100")

# Create Zipcode Lookup Function
def zipLookup():
    url = "http://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode="+zip.get()+"&distance=5&API_KEY=F9F70079-FDC6-45A6-A3F5-55CD512F6CBB"

    try:
        api_request = requests.get(url)
        api = json.loads(api_request.content)
        city = api[0]['ReportingArea']
        quality = api[0]['AQI']
        category = api[0]['Category']['Name']
        
        if category == "Good":
            weather_color = "#00e400"
        elif category == "Moderate":
            weather_color = '#ffff00'
        elif category == "Unhealthy for Sensitive Groups":
            weather_color = '#ff7e00'
        elif category == "Unhealthy":
            weather_color = '#ff0000'
        elif category == "Very Unhealthy":
            weather_color = "#8f3f97"
        elif category == "Hazardous":
            weather_color = '#7E0023'

        root.configure(background=weather_color)

        myLabel = Label(root, text = city + " Air Quality " + str(quality) + " " + category, font=("Helvetica", 20), background=weather_color)
        myLabel.grid(row=1, column=0, columnspan=2)
    except Exception as e:
        api = "Error..."

zip = Entry(root)
zip.grid(row=0, column=0, sticky=W+E+N+S)

zipButton = Button(root, text="Lookup Zipcode", command=zipLookup)
zipButton.grid(row=0, column=1, sticky=W+E+N+S)

root.mainloop()

#NOTES
# 