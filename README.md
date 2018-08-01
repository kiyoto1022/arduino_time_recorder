# arduino_time_recorder

Time Recorder with Arduino + RFID
Take the face of the exit person by the camera when punch out
Confirm whether you are a principal by machine learning

## Setup Arduino

### Setup Bread Board

![rfid_reader](https://user-images.githubusercontent.com/16317266/43329883-9d00e5fe-91fc-11e8-8efe-61dcde600e63.png)

### Install Library

Download ParallaxRFID Library
```
> git clone https://github.com/kiyoto1022/Arduino-parallax-rfid
> cd Arduino-parallax-rfid
> xcopy /e ParallaxRFID \Users\kiyoto1022\Documents\Arduino\libraries\ParallaxRFID
```

### Setup RFID Tag
Open Sketch File
```
ArduinoIDE > File > Open > ParallaxRFID\examples\ParallaxRFIDWrite\ParallaxRFIDWrite.ino
```

Writing Arduino Board
```
ArduinoIDE > Sketch > Upload
```

Writing RFID Tag

### Setup Arduino Time Recorder
Clone
```
git clone https://github.com/kiyoto1022/arduino_time_recorder.git
```

Open Sketch File
```
ArduinoIDE > File > Open > arduino_time_recorder\arduino_time_recorder.ino
```

Writing Arduino Board
```
ArduinoIDE > Sketch > Upload
```

## Python Setup (2.7)

### Install Package
```
$ easy_install pip
$ easy_install pillow
$ pip install numpy
$ pip install opencv-python
$ pip install opencv-contrib-python
```

### Execute
```
python time_record.py
```
