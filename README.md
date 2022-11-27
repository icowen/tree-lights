# Christmas Lights

Micropython code for running a Christmas lights display.

## Ingredients
* [Raspberry Pico](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)
    * I used a Pico W but it should work on a normal Pico
* Individually Addressable LED Pixels
    * Available on [Amazon](https://www.amazon.com/ALITOVE-LED-Individually-Addressable-Waterproof/dp/B01AG923GI/ref=pd_lpo_1?pd_rd_w=p1cWJ&content-id=amzn1.sym.116f529c-aa4d-4763-b2b6-4d614ec7dc00&pf_rd_p=116f529c-aa4d-4763-b2b6-4d614ec7dc00&pf_rd_r=G3DR33JPN596N3K660F0&pd_rd_wg=ZgB3R&pd_rd_r=04358559-50ed-444c-829e-0b8741c722e4&pd_rd_i=B01AG923GI&th=1)
* A button
    * Available on [Amazon](https://www.amazon.com/Waterproof-Momentary-Button-Switch-Colors/dp/B07F24Y1TB/ref=sr_1_3?crid=1HLTFHUV8PHK5&keywords=12mm+momentary+push+button&qid=1669582996&sprefix=12mm+momentary+push+button%2Caps%2C93&sr=8-3)
* Wires / solder

## Setup
1. Flash Pi (I used the firmware in this repo since it includes Wifi capability) and upload files in `src/` to the root of the Pi
1. Attach the lights together and connect the data line of the lights to `Pin 28`, and connect ground and 5V
    1. You can also wire the additional 5V/ground wires of the 2nd strand of lights in parallel
1. Connect the button to ground and `Pin 27`
1. Power on the Pi and the lights should turn on
1. Press the button to cycle through different displays and hold the button to turn the lights off

## Diagram
![diagram](docs/LightsPinout.svg)