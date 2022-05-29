# Gravitator
Simulate the behavior of the gravitation between celestial objects.

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
If you are running a custom script, you can use the following variables, functions & modules.
Make sure you use these variables & functions with a ```self.``` in front of them

### Variables
* ```running```: bool (used for the main loop)
* ```paused```: bool (used for physics)
* ```g```: float | int
* ```delta_time```: float
* ```bodies```: list
* ```current_body```: Body | None (when creating a body with <kbd>Leftclick</kbd>, the body gets stored inside this variable)
* ```dragged_body```: Body | None (when moving a body with <kbd>Rightclick</kbd>, the body gets stored inside this variable)
* ```config_surf```: ui.Surface
* ```fps_text```: ui.Text
* ```run_button```: ui.Button
* ```mass_input```: ui.InputField
* ```radius_input```: ui.InputField
* ```g_input```: ui.InputField
* ```path_length_input```: ui.InputField
* ```path_multiplier_input```: ui.InputField
* ```draw_lines_input```: ui.Checkbox
* ```bg_alpha_input```: ui.InputField

## Functions
* ```runScript```
* ```createBody```
* ```handleBodies```
* ```run```

## Modules
* ```ui```
* ```pygame```
* ```tk```