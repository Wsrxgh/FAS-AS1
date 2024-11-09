# Project overview

## Project Description

Wildfire-UAVSim is a customizable wildfire tracking simulator that enables
the evaluation of diverse adaptation strategies. Among its many configuration parameters, the forest area is customizable with different densities of vegetation, as well as fire and smoke dispersion patterns that are affected by factors such as wind, conforming different observability conditions. The configuration options of our simulator also allow to place a team of UAVs in charge of tracking the fire over the forest area. Wildfire-UAVSim provides a graphical web interface native from Mesa framework, executed by the simulator, in order to keep track of how the simulation evolves in time.

## File Structure

Several files compose the project structure, namely:

- [`/wildfire/`](/wildfire)
  - [`api.py`](/wildfire/api.py) holds the Flask REST API implementation. This is the entrypoint of the application.
  - [`agents.py`](/wildfire/agents.py) holds the logic for managing elements such as Fire, Smoke, Wind and UAVs.
  - [`wildfire_model.py`](/wildfire/wildfire_model.py) holds the logic for managing the wildfire simulation, by utilizing elements from [agents.py](/wildfire/agents.py).
  - [`main.py`](/wildfire/main.py) allows to execute the wildfire simulation built in [widlfire_model.py](/wildfire/wildfire_model.py) file.
  - [`common_fixed_variables.py`](/wildfire/common_fixed_variables.py) holds the variables used to set the simulation execution configurations.
  - [`Canvas_Grid_Visualisation.py`](/wildfire/Canvas_Grid_Visualization.py) contains a Mesa class, modified for making UAV observation areas visible on the graphical web interface. It is not really necessary to change this file.
  - [`/schemas/`](/wildfire/schemas)
    - [`adaptation_options_schema.json`](/wildfire/schemas/adaptation_options_schema.json) holds the JSON schema for the adaptations options JSON response body.
    - [`monitor_schema.json`](/wildfire/schemas/monitor_schema.json) holds the JSON schema for the monitor JSON response body.
    - [`execute_schema.json`](/wildfire/schemas/execute_schema.json) holds the JSON schema for the execute JSON request body.
  - [`/pages/`](/wildfire/pages)
    - [`index.html`](/wildfire/pages/index.html) the HTML page containing a brief API explanation. It can be accessed by sending a `GET` request to the `/` API endpoint.

# Installation Setup

In the following subsections, the installation process for executing the project will be explained.

## Make

Make is needed to build and run the docker image using the provided Makefile. You do not have to use the Makefile,
and can choose to run the commands manually instead, but it will make life easier.

- If you are on Windows, you can download [Make for Windows](https://gnuwin32.sourceforge.net/packages/make.htm)
- If you are on Linux:
  - Check if you have make: `make -version`. If you are given output stating the Make version, you have it installed.
  - If not, install make: 
    ```commandline
    sudo apt-get update
    sudo apt-get install make
    ```

## Docker

Installing Docker is required in order to build and run the image containing the exemplar. You can find out how to do 
so for your operating system on the [Docker website](https://docs.docker.com/get-started/get-docker/).

# Execution

The exemplar runs inside of a Docker container. You can interact with it through the REST API and the web interface.

To run the docker container, navigate to the folder containing the [`Makefile`](/Makefile), open a terminal, and execute:
```commandline
make run
```
> **NOTE**: The first time you run the container, you will need to run `make runFirst` instead of `make run`.

You can hit `Ctrl+C` in this terminal window to terminate the process, which should also stop the container. If the 
container does not stop, you can use:
```commandline
make stop
```
To remove the container and image, you can run:
```commandline
make clean
```

You can find the web interface at [http://127.0.0.1:8521/](http://127.0.0.1:8521/).

The REST API can be reached at [http://127.0.0.1:55555/](http://127.0.0.1:55555/). (_Note that the terminal output will
claim the API is running at `172.17.0.2:55555` instead. This is its address **within** the container, and you can ignore
this difference._)

# Graphical interface functionalities

When executing the project as explained above, a web page hosted in http://127.0.0.1:8521/ should appear in user's default browser. Port can be modified in `main.py` file if user has the default one already busy.

The relevant graphical interface elements are:

### `Grid`

The grid with generated cells, with vegetation, fire, smoke, and UAVs, can be seen in the center of the screen.

### `Start button`

The start button allows to run the simulation without having to repeatedly click `Step`.

### `Step button`

The step button allows to execute one time step at a time. This will block until a `PUT` request to `/execute` specifies
the drone directions for the step. To experiment with this, you can use [Postman](https://www.postman.com/downloads/).

### `Reset button`

The reset button allows to execute the `reset()` method, inherited and overwritten from Mesa framework class `mesa.Model`, into WildFireModel class, inside `widlfire_model.py` file.

### `Frames per second`

It is a slider that allows to set the frames per second (FPS) velocity for the graphical visualization of the simulation execution. Each frame corresponds to one time step. Its range goes from 1 to 20 FPS, taking into account that, counterintuitively, 0 FPS set the fastest FPS velocity. One reason why the simulation might seem not be playing fluently could be the setting of the `FIRE_SPREAD_SPEED` variable referenced below.

### `Current step counter`

Indicates the current time step of the simulation.

# Common variables configuration

Global variables are used in the project to configure different simulation executions. In the next subsections several global variables descriptions are shown, as well as many configuration examples for execution.

## Variables description

### Forest area

`BATCH_SIZE`: It establishes how long the simulation will run, in number of time steps.

`WIDTH`, `HEIGHT`: They set the grid size (forest area size) in cells.

`BURNING_RATE`: It sets the fuel decay speed in terms of time steps.

`FIRE_SPREAD_SPEED`: it sets how fast fire spreads to other cells, in terms of time steps.

`FUEL_UPPER_LIMIT`, `FUEL_BOTTOM_LIMIT`: They establish the maximum and
minimum amount of burnable fuel present in each cell, respectively.

`DENSITY_PROB`: It is a value in the range `[0, 1]` that establishes the
percentage of the grid covered by vegetation.

### Wind

`ACTIVATE_WIND`: It sets whether the fire spread is influenced by wind.

`FIXED_WIND`: If it is active, then wind blows in the direction set by `WIND_DIRECTION`. If it is not, it means wind blows two directions, specified by `FIRST_DIR` and `SECOND_DIR`. Since wind can blow a direction stronger than the other one, `FIRST_DIR_PROB` establishes the wind first direction’s predominance.

`PROBABILITY_MAP`: If it is active, the probability of the fire to spread to each cell at all times can be visualized.

`MU`: It sets how strong wind blows with a value in the range `[0, 1]`.

### Smoke

`ACTIVATE_SMOKE`: It sets whether smoke will be part of the simulation.

`SMOKE_PRE_DISPELLING_COUNTER`: It establishes how fast smoke appears after fire starts in a cell.

### UAV

`NUM_AGENTS`: It establishes the amount of UAVs that will fly over the forest area (zero indicates the simulator will simulate only the wildfire spread).

`N_ACTIONS`: Specifies the number of possible actions each UAV can take when deciding on a move, which by default is set as `[north, east, west, south]`.

`UAV_OBSERVATION_RADIUS`: It sets the observation radius—technically it is not a radius, since observed areas have square shapes.

`SECURITY_DISTANCE`: It establishes the minimum distance that UAVs should be separated from each other for avoiding collisions.

## Configuration examples

Six default examples of how different variables can be configured to develop distinct scenarios, can be seen below. All scenarios shown are captured in `time step = 20`, in different time steps scenarios might look different.

### Common default variables

Before showing the examples, this section compiles all variables that can be set in common with all examples. The variables that were not mentioned can be set to their default value.

`BATCH_SIZE = 90`

`WIDTH = 50`, `HEIGHT = 50`

`BURNING_RATE = 1`

`FIRE_SPREAD_SPEED = 2`

`FUEL_UPPER_LIMIT = 10`, `FUEL_BOTTOM_LIMIT = 7`

`DENSITY_PROB = 1`

### Normal conditions (no smoke, no wind, no UAV)

A scenario with no wind, smoke, or UAV, should appear.

`NUM_AGENTS = 0`

`ACTIVATE_WIND = False`

`ACTIVATE_SMOKE = False`

`PROBABILITY_MAP = False`

### Windy conditions (no smoke, wind, no UAV)

Concretely, a scenario with two weak wind components should appear, first with 50% of south component, and a second west component with 50%. In this scenario, neither smoke nor UAV should appear.

`NUM_AGENTS = 0`

`ACTIVATE_WIND = True`

`ACTIVATE_SMOKE = False`

`PROBABILITY_MAP = False`

`FIXED_WIND = False`

`WIND_DIRECTION = 'south'`

`FIRST_DIR = 'south'`

`SECOND_DIR = 'west'`

`FIRST_DIR_PROB = 0.5`

`MU = 0.5`

### Windy and partial observability conditions (smoke, wind, no UAV)

A scenario with strong windy conditions, blowing east, and late short-lasting smoke should appear. Remember that, since the dispelling counter for smoke is set in `Smoke` class by default, inside `agents.py` file, changes should be done to the `self.dispelling_counter_start_value` variable, inside `__init()__` method (`Smoke` class). Keep also in mind that `self.dispelling_counter_start_value + SMOKE_PRE_DISPELLING_COUNTER` should be greater than the amount of fuel assigned to each cell (for taking less risks, compare to `FUEL_UPPER_LIMIT`, which is the maximum possible amount of fuel of each cell), in order to avoid situations in which smoke dissipates before the end of the cell’s burning process.

`NUM_AGENTS = 0`

`ACTIVATE_WIND = True`

`ACTIVATE_SMOKE = True`

`PROBABILITY_MAP = False`

`FIXED_WIND = True`

`WIND_DIRECTION = 'east'`

`MU = 0.95`

`SMOKE_PRE_DISPELLING_COUNTER = 7`

`self.dispelling_counter_start_value = 4`

### 2 UAV with small partial areas (normal conditions)

A scenario with 2 UAV having small partial areas in normal conditions should appear.

`NUM_AGENTS = 2`

`ACTIVATE_WIND = False`

`ACTIVATE_SMOKE = False`

`PROBABILITY_MAP = False`

`UAV_OBSERVATION_RADIUS = 3`

### 3 UAV with big partial areas (smoke, no wind)

A scenario with 3 UAV having big partial areas, with fast long-lasting smoke, should appear.

`NUM_AGENTS = 3`

`ACTIVATE_WIND = False`

`ACTIVATE_SMOKE = True`

`PROBABILITY_MAP = False`

`SMOKE_PRE_DISPELLING_COUNTER = 2`

`self.dispelling_counter_start_value = 9`

`UAV_OBSERVATION_RADIUS = 12`

### Probability map

A scenario with normal conditions should appear. Keep in mind that changing wind conditions will affect to the visualized probabilitites. Also, remember to set 0 UAV when showing the fire probability map.

`NUM_AGENTS = 0`

`ACTIVATE_WIND = False`

`ACTIVATE_SMOKE = False`

`PROBABILITY_MAP = True`
