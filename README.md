# Gravitator
Simulate the behavior of the gravitation between bodies.

## Requirements
* pygame==2.1.2
* VectorUtils==1.3.4

## Usage
* Install [python](https://www.python.org/downloads/)
* Set up virtualenv, if you want to
* Install pip packages with ```pip install -r requirements.txt```
* Run with python ```python Gravitator```

## Controls
* Press and hold <kbd>Leftclick</kbd> to create a body.
* Press and hold <kbd>Rightclick</kbd>
* Press <kbd>Backspace</kbd> to remove the last body.
* Press <kbd>c</kbd> to remove all bodies.
* Press <kbd>Esc</kbd> to pause / continue.

## Scripts
If you are running a custom script, you can use everything, that is inside the [Gravitator.Application class](Gravitator/app.py). Make sure to write ```self.``` infront of the variables and methods you are using.
