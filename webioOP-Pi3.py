import wiringpi

from flask import Flask, render_template, request
app = Flask(__name__)

INPUT = 0 
OUTPUT = 1 
LOW = 0 
HIGH = 1 
DEBUG = 1
PINS = {
   0 : {'name' : 'SDA.0', 'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 3},
   1 : {'name' : 'SCL.0', 'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 5},
   2 : {'name' : 'PWM.0',  'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 7},
   3 : {'name' : 'PL02',  'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 8},
   4 : {'name' : 'PL03',  'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 10},
   5 : {'name' : 'RXD.3',  'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 11},
   6 : {'name' : 'PD18',  'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 12},
   7 : {'name' : 'TXD.3',  'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 13},
   8 : {'name' : 'PL10',  'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 15},
   9 : {'name' : 'PD15', 'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 16},
  10 : {'name' : 'PD16', 'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 18},
  11 : {'name' : 'MOSI.1', 'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 19},
  12 : {'name' : 'MISO.1', 'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 21},
  13 : {'name' : 'PD21',  'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 22},
  14 : {'name' : 'SCLK.1', 'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 23},
  15 : {'name' : 'CE.1', 'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 24},
  16 : {'name' : 'PL08', 'mode' : 0, 'smode' : '' , 'value' : LOW,  'pin' : 26} 
   }

ALTS = [
   "IN", "OUT", "ALT5", "ALT4", "ALT0", "ALT1", "ALT2", "ALT3"
   ]

def readall():
    for i in PINS: 
        pin = PINS[i]['pin']
        alt=wiringpi.getAlt(pin)
        if DEBUG == 1: print("i=" + str(i) + " pin=" + str(pin) + " alt=" + str(alt))
        value=wiringpi.digitalRead(pin)
        if DEBUG == 1: print("pin=" + str(pin) + " alt=" + ALTS[alt] + " value=" + str(value))
        PINS[i]['mode']=alt
        PINS[i]['smode']=ALTS[alt]
        PINS[i]['value']=value
    for i in PINS: 
        if DEBUG == 1: print("i=" + str(i) + " mode=" + str(PINS[i]['mode']) + " " + PINS[i]['smode'])

wiringpi.wiringPiSetupPhys()

readall()

@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   templateData = {
      'pins' : PINS
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('webioOP.html', **templateData)

# change pin mode
@app.route("/changeMode/<int:changePin>/<action>")
def actionMode(changePin, action):
   if DEBUG == 1: print("actionMode:" + str(changePin) + ":" + action)
   # Convert the pin from the URL into an integer:
#   cpin = int(changePin)
   pin = PINS[changePin]['pin']

   # Get the device name for the pin being changed:
   deviceName = PINS[changePin]['name']
   if DEBUG == 1: print("pin=" + str(pin) + " deviceName=" + deviceName)
   # If the action part of the URL is "output," execute the code indented below:
   if action == "output":
      # Set the pin output:
      wiringpi.pinMode(pin, OUTPUT)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " output."
   if action == "input":
      wiringpi.pinMode(pin, INPUT)
      message = "Turned " + deviceName + " input."

   readall()

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'message' : message,
      'pins' : PINS
   }

   return render_template('webioOP.html', **templateData)


# change output value
@app.route("/changeValue/<int:changePin>/<action>")
def actionValue(changePin, action):
   if DEBUG == 1: print("actionValue:" + str(changePin) + ":" + action)
   # Convert the pin from the URL into an integer:
#   cpin = int(changePin)
   pin = PINS[changePin]['pin']

   # Get the device name for the pin being changed:
   deviceName = PINS[changePin]['name']
   if DEBUG == 1: print("pin=" + str(pin) + " deviceName=" + deviceName)
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      wiringpi.digitalWrite(pin, HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      wiringpi.digitalWrite(pin, LOW)
      message = "Turned " + deviceName + " off."
   if action == "toggle":
      # Read the pin and set it to whatever it isn't (that is, toggle it):
      value=wringpi.digitalRead(pin)
      wiringpi.digitalWrite(pin, not value)
      message = "Toggled " + deviceName + "."

   readall()

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'message' : message,
      'pins' : PINS
   }

   return render_template('webioOP.html', **templateData)

if __name__ == "__main__":
   if DEBUG == 1: app.run(host='0.0.0.0', port=80, debug=True)
   if DEBUG == 0: app.run(host='0.0.0.0', port=80, debug=False)

