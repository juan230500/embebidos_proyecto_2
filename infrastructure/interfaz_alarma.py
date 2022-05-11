import PySimpleGUI as sg
import serial

# Theming
sg.theme('Black')

# PySimpleGUI variables
title = sg.Text('AlarmConfig App', font="Arial 15")
subtitle_1 = sg.Text('Entries:', font="Arial 12 italic")
label_hour = sg.Text('Hour:')
entry_hour = sg.Input(key='key_hour')
label_minute = sg.Text('Minute:')
entry_minute = sg.Input(key='key_minutes')
label_second = sg.Text('Second:')
entry_second = sg.Input(key='key_seconds')
subtitle_2 = sg.Text('Actions:', font="Arial 12 italic")
button_time = sg.Button('Set Time')
button_alarm = sg.Button('Set Alarm')

# Main layout distribution
layout = [[title],
          [subtitle_1],
          [label_hour, entry_hour],
          [label_minute, entry_minute],
          [label_second, entry_second],
          [subtitle_2],
          [button_time],
          [button_alarm]]

# Create PySimpleGUI window
window = sg.Window('AlarmConfig', layout)

# Start serial communication
ser = serial.Serial("COM3")
ser.baudrate = 115200


# Formats input to be sent through serial communication
def format_input(hour, minutes, seconds, type):
    result = []
    print(hour, minutes, seconds)
    hour = int(hour)
    minutes = int(minutes)
    seconds = int(seconds)

    if isinstance(hour, int) and isinstance(minutes, int) and isinstance(seconds, int):
        # Verify data is valid
        result.append(str(hour // 10))
        result.append(str(hour % 10))
        result.append(str(minutes // 10))
        result.append(str(minutes % 10))
        result.append(str(seconds // 10))
        result.append(str(seconds % 10))
        result.append(type)
    else:
        print("Error with data input")

    return result


# UI loop
while True:
    event, values = window.read()

    if event in (None, 'Exit'):
        break
    else:
        print("Event: " + event)
        selected_hour = values['key_hour']
        selected_minute = values['key_minutes']
        selected_seconds = values['key_seconds']
        if selected_hour != "" and -1 < int(selected_hour) < 24:
            if selected_minute != "" and -1 < int(selected_minute) < 60:
                if selected_seconds != "" and -1 < int(selected_seconds) < 60:
                    if event == 'Set Time':
                        # Handle set time action
                        result = format_input(
                            selected_hour, selected_minute, selected_seconds, 'C')
                        print("Setting time to " + selected_hour + ":" +
                              selected_minute + ":" + selected_seconds)
                        print(result)

                        for value in result:
                            ser.write(value.encode())
                            print(ser.read())
                            print("Time set!")
                    elif event == 'Set Alarm':
                        # Handle set alarm action
                        result = format_input(
                            selected_hour, selected_minute, selected_seconds, 'A')
                        print("Setting alarm to " + selected_hour +
                              ":" + selected_minute + ":" + selected_seconds)

                        for value in result:
                            ser.write(value.encode())
                            print(ser.read())
                else:
                    print("Invalid seconds")
            else:
                print("Invalid minute")
        else:
            print("Invalid hour")

window.close()
