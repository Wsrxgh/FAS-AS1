import os.path
import sys

from flask import Flask, Response, request
from threading import Thread
from os import path
import json
import jsonschema

from wildfire_model import WildFireModel
import common_fixed_variables as values
import main
from agents import UAV

SCHEMAS_PATH = "schemas"
PAGES_PATH = "pages"


def create_app(test_config=None):
    values.NUM_AGENTS = 3

    app = Flask(__name__, instance_relative_config=True)

    wildfire = Thread(target=main.main, args=(), daemon=True)
    wildfire.start()

    @app.route("/")
    def index():
        try:
            page = get_page("index.html")
            return Response(
                response=page,
                status=200,
                mimetype='text/html'
            )
        except Exception as e:
            return Response(response=e.__str__(),
                            status=500,
                            mimetype='text/html')


    @app.route("/monitor")
    def monitor():
        try:
            print(f"Server is ready: {main.SERVER}")
            data = get_monitor_data(main.SERVER.model)
            return Response(
                response=json.dumps(data),
                status=200,
                mimetype='text/json'
            )
        except Exception as e:
            return Response(response=e.__str__(),
                            status=500,
                            mimetype='text/html')

    @app.route("/execute", methods=['PUT'])
    def execute():
        try:
            set_uav_directions(request.json, main.SERVER.model)
            return Response(
                status=200,
                mimetype='text/json'
            )
        except Exception as e:
            return Response(response=e.__str__(),
                            status=500,
                            mimetype='text/html')

    @app.route("/adaptation_options")
    def adaptation_options():
        try:
            data = get_adaptation_options(main.SERVER.model)
            return Response(
                response=json.dumps(data),
                status=200,
                mimetype='text/json'
            )
        except Exception as e:
            return Response(response=e.__str__(),
                            status=500,
                            mimetype='text/html')

    @app.route("/monitor_schema")
    def monitor_schema():
        try:
            schema = get_schema("monitor_schema.json")
            return Response(
                response=schema,
                status=200,
                mimetype='text/json'
            )
        except Exception as e:
            return Response(response=e.__str__(),
                            status=500,
                            mimetype='text/html')

    @app.route("/execute_schema")
    def execute_schema():
        try:
            schema = get_schema("execute_schema.json")
            return Response(
                response=schema,
                status=200,
                mimetype='text/json'
            )
        except Exception as e:
            return Response(response=e.__str__(),
                            status=500,
                            mimetype='text/html')

    @app.route("/adaptation_options_schema")
    def adaptation_options_schema():
        try:
            schema = get_schema("adaptation_options_schema.json")
            return Response(
                response=schema,
                status=200,
                mimetype='text/json'
            )
        except Exception as e:
            return Response(response=e.__str__(),
                            status=500,
                            mimetype='text/html')

    return app


def get_monitor_data(model: WildFireModel):
    monitor_data = {
        "currentStep": model.evaluation_timesteps_counter,
        "constants": {
            "fixedWind": values.FIXED_WIND,
            "activateSmoke": values.ACTIVATE_SMOKE,
            "activateWind": values.ACTIVATE_WIND,
            "windDirection": values.WIND_DIRECTION,
            "firstDirection": values.FIRST_DIR,
            "secondDirection": values.SECOND_DIR,
            "firstDirStrength": values.FIRST_DIR_PROB,
            "windVelocity": values.MU,
            "simulationDuration": values.BATCH_SIZE,
            "width": values.WIDTH,
            "height": values.HEIGHT,
            "burningRate": values.BURNING_RATE,
            "fireSpreadSpeed": values.FIRE_SPREAD_SPEED,
            "fuelUpperLimit": values.FUEL_UPPER_LIMIT,
            "fuelBottomLimit": values.FUEL_BOTTOM_LIMIT,
            "densityProbability": values.DENSITY_PROB,
            "smokePreDispellingCounter": values.SMOKE_PRE_DISPELLING_COUNTER,
            "numUAV": values.NUM_AGENTS,
            "observationRadius": values.UAV_OBSERVATION_RADIUS,
            "securityDistance": values.SECURITY_DISTANCE
        },
        "dynamicValues": {
            "MR1": model.MR1_LIST,
            "MR2": model.MR2_VALUE,
            "uavDetails": get_uav_details(model)[1]
        }
    }

    return monitor_data


def get_adaptation_options(model: WildFireModel):
    all_details = get_uav_details(model)[1]
    relevant_details = []
    for uav in all_details:
        uav.pop("x")
        uav.pop("y")
        relevant_details.append(uav)

    adaptation_opt = {
        "uavDetails": relevant_details
    }
    return adaptation_opt


def get_uav_details(model: WildFireModel) -> tuple[list[UAV], list[dict]]:
    uavs = [agent for agent in model.schedule.agents if type(agent) is UAV]
    uav_details = []
    for uav in uavs:
        uav_details.append({
            "id": uav.unique_id,
            "x": uav.pos[0],
            "y": uav.pos[1],
            "direction": uav.selected_dir,
            "fireStates": uav.fire_states,
            "smokeStates": uav.smoke_states,
            "Integrity(MR3)": round(uav.integrity, 2),
        })
    return uavs, uav_details


def get_schema(filename: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    schemas_dir = os.path.join(current_dir, SCHEMAS_PATH)
    schema_file = os.path.join(schemas_dir, filename)
    with open(schema_file) as f:
        schema = f.read()
    return schema

def get_page(filename: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pages_dir = os.path.join(current_dir, PAGES_PATH)
    page_file = os.path.join(pages_dir, filename)
    with open(page_file) as f:
        page = f.read()
    return page


def set_uav_directions(adaptation: list[dict], model: WildFireModel):
    uavs : list[UAV] = [agent for agent in model.schedule.agents if type(agent) is UAV]
    directions = []
    with (model.next_step_available):
        for model_uav in uavs:
            found = False
            # Try to find the direction in the adaptation execute
            for exec_uav in adaptation["uavDetails"]:
                if exec_uav["id"] == model_uav.unique_id:
                    found = True
                    directions.append(exec_uav["direction"])

            # otherwise let it keep its current direction
            if not found:
                directions.append(model_uav.selected_dir)

        model.new_direction = directions
        model.last_step_seen = model.evaluation_timesteps_counter
        model.next_step_available.notify_all()


if __name__ == '__main__':
    print("\n\n ## WildFire REST API available at http://127.0.0.1:55555 ##\n\n")
    create_app().run(host="172.17.0.2", port=55555) # Default docker bridge address is 172.17.0.2