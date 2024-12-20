import math
from UPISAS.strategy import Strategy
import logging

class WildfireAvoidanceStrategy(Strategy):
    def __init__(self, exemplar):
        super().__init__(exemplar)
        self.smoke_density_threshold = 50  # Smoke density threshold

    def analyze(self):

        data = self.knowledge.fresh_data.get("dynamicValues", {}).get("uavDetails", [])
        avoidance_data = {}

        for uav in data:
            uav_id = uav.get("id")
            fire_states = uav.get("fireStates", [])
            smoke_states = uav.get("smokeStates", [])
            hp = uav.get("Integrity(MR3)", 1.0)

            logging.info(f"UAV {uav_id} at position ({uav.get('x')}, {uav.get('y')})")
            logging.info(f"Detected {len(smoke_states)} smoke points and {len(fire_states)} fire points")

            if len(smoke_states) > self.smoke_density_threshold:
                danger_positions = fire_states + smoke_states
                logging.info(f"UAV {uav_id} detected high smoke density: {len(smoke_states)} points")
            else:
                danger_positions = fire_states

            avoidance_data[uav_id] = danger_positions

        self.knowledge.analysis_data["avoidance_data"] = avoidance_data
        return True

    def plan(self):

        avoidance_data = self.knowledge.analysis_data.get("avoidance_data", {})
        plan_data = {"uavDetails": []}

        current_step = self.knowledge.fresh_data.get("currentStep", 0)
        constants = self.knowledge.fresh_data.get("constants", {})
        first_direction = constants.get("firstDirection", "south")
        second_direction = constants.get("secondDirection", "east")

        for index, uav in enumerate(self.knowledge.fresh_data.get("dynamicValues", {}).get("uavDetails", [])):
            uav_id = uav.get("id")
            x = uav.get("x", 0)
            y = uav.get("y", 0)
            current_direction = uav.get("direction", 0)

            # Initial dispersion phase
            if index == 0:
                if current_step < 15:
                    # The first UAV moves along the first wind direction
                    new_direction = self.convert_direction_to_int(first_direction)
                elif current_step < 20:
                    # After 10 steps, switch to the second wind direction
                    new_direction = self.convert_direction_to_int(second_direction)
                else:
                    danger_positions = avoidance_data.get(uav_id, [])
                    other_uav_positions = [
                        (other_uav.get("x", 0), other_uav.get("y", 0))
                        for other_uav in self.knowledge.fresh_data.get("dynamicValues", {}).get("uavDetails", [])
                        if other_uav.get("id") != uav_id
                    ]
                    new_direction = self.find_safe_direction(x, y, current_direction, danger_positions, other_uav_positions)

            elif current_step < 5:
                if index == 1:
                    # The second UAV moves along the second wind direction
                    new_direction = self.convert_direction_to_int(second_direction)
                elif index == 2 and current_step < 2:
                    # The third UAV chooses another direction
                    new_direction = (set([0, 1, 2, 3]) - {
                        self.convert_direction_to_int(first_direction),
                        self.convert_direction_to_int(second_direction)
                    }).pop()
                else:
                    danger_positions = avoidance_data.get(uav_id, [])
                    other_uav_positions = [
                        (other_uav.get("x", 0), other_uav.get("y", 0))
                        for other_uav in self.knowledge.fresh_data.get("dynamicValues", {}).get("uavDetails", [])
                        if other_uav.get("id") != uav_id
                    ]
                    new_direction = self.find_safe_direction(x, y, current_direction, danger_positions, other_uav_positions)

            else:
                danger_positions = avoidance_data.get(uav_id, [])
                other_uav_positions = [
                    (other_uav.get("x", 0), (other_uav.get("y", 0)))
                    for other_uav in self.knowledge.fresh_data.get("dynamicValues", {}).get("uavDetails", [])
                    if other_uav.get("id") != uav_id
                ]
                new_direction = self.find_safe_direction(x, y, current_direction, danger_positions, other_uav_positions)

            plan_data["uavDetails"].append({
                "id": uav_id,
                "action": "move",
                "direction": new_direction
            })

        self.knowledge.plan_data = plan_data
        return True

    def find_safe_direction(self, x, y, current_direction, danger_positions, other_uav_positions):
        """
        Find the safest direction to move by considering the total score from all danger positions.
        """
        possible_directions = [0, 1, 2, 3, 4]  
        direction_vectors = {
            0: (1, 0),   # east
            1: (0, 1),   # south
            2: (-1, 0),  # west
            3: (0, -1),  # north
            4: (0, 0)    # stay
        }

        if not danger_positions:
            return 4  

        max_score = -math.inf  
        best_direction = current_direction  

        for direction in possible_directions:
            dx, dy = direction_vectors[direction]
            new_x, new_y = x + dx, y + dy

            # calculate the total distance to all danger positions
            total_distance_to_danger = sum(
                math.sqrt((new_x - danger_x) ** 2 + (new_y - danger_y) ** 2)
                for danger_x, danger_y in danger_positions
            )

            # calculate the total distance to other UAV
            total_distance_to_other_uav = sum(
                math.sqrt((new_x - other_x) ** 2 + (new_y - other_y) ** 2)
                for other_x, other_y in other_uav_positions
            )

            if total_distance_to_other_uav < 10 * len(other_uav_positions):
                total_distance_to_danger -= (10 * len(other_uav_positions) - total_distance_to_other_uav)

            score = total_distance_to_danger

            if score > max_score:
                max_score = score
                best_direction = direction

        return best_direction

    def convert_direction_to_int(self, direction_str):
        """
        Convert string direction to numeric encoding
        """
        direction_map = {
            "east": 0,
            "south": 1,
            "west": 2,
            "north": 3,
            "stay": 4
        }
        return direction_map.get(direction_str.lower(), 0)
