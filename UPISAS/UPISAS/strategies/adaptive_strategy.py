import math
from UPISAS.strategy import Strategy

class WildfireAvoidanceStrategy(Strategy):
    def analyze(self):
        data = self.knowledge.fresh_data.get("dynamicValues", {}).get("uavDetails", [])
        avoidance_data = {}

        for uav in data:
            uav_id = uav.get("id")
            fire_states = uav.get("fireStates", [])
            smoke_states = uav.get("smokeStates", [])

            # positions of the fire and smoke are danger positions
            danger_positions = fire_states + smoke_states
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

            # initial dispersion
            if current_step < 5:
                if index == 0:
                    # uav in the first amd second wind direction move more steps
                    new_direction = self.convert_direction_to_int(first_direction)
                elif index == 1:
                    new_direction = self.convert_direction_to_int(second_direction)
                elif index == 2 and current_step < 2:
                    # the third uav move 2 steps
                    new_direction = (set([0, 1, 2, 3]) - {self.convert_direction_to_int(first_direction), self.convert_direction_to_int(second_direction)}).pop()
                else:
                    danger_positions = avoidance_data.get(uav_id, [])
                    other_uav_positions = [
                        (other_uav.get("x", 0), other_uav.get("y", 0)) for other_uav in self.knowledge.fresh_data.get("dynamicValues", {}).get("uavDetails", [])
                        if other_uav.get("id") != uav_id
                    ]
                    new_direction = self.find_safe_direction(x, y, current_direction, danger_positions, other_uav_positions)
            elif current_step < 10 and index == 0:
                # first direction uav move more
                new_direction = self.convert_direction_to_int(first_direction)
            else:
                danger_positions = avoidance_data.get(uav_id, [])
                other_uav_positions = [
                    (other_uav.get("x", 0), other_uav.get("y", 0)) for other_uav in self.knowledge.fresh_data.get("dynamicValues", {}).get("uavDetails", [])
                    if other_uav.get("id") != uav_id
                ]

                new_direction = self.find_safe_direction(x, y, current_direction, danger_positions, other_uav_positions)
            
            # update move plan
            plan_data["uavDetails"].append({
                "id": uav_id,
                "action": "move",
                "direction": new_direction
            })

        self.knowledge.plan_data = plan_data
        return True

    def find_safe_direction(self, x, y, current_direction, danger_positions, other_uav_positions):
        possible_directions = [0, 1, 2, 3, 4]
        direction_vectors = {
            0: (1, 0),  # east
            1: (0, 1),  # south
            2: (-1, 0), # west
            3: (0, -1), # north
            4: (0, 0)   
        }

        if not danger_positions:
            return 4

        # calculate the distance to danger positions
        max_score = -math.inf
        best_direction = current_direction

        for direction in possible_directions:
            dx, dy = direction_vectors[direction]
            new_x, new_y = x + dx, y + dy

            min_distance_to_danger = min(
                math.sqrt((new_x - danger_x) ** 2 + (new_y - danger_y) ** 2)
                for danger_x, danger_y in danger_positions
            ) if danger_positions else math.inf  

            # calculate the distance to other uavs
            min_distance_to_other_uav = min(
                math.sqrt((new_x - other_x) ** 2 + (new_y - other_y) ** 2)
                for other_x, other_y in other_uav_positions
            ) if other_uav_positions else math.inf  

            if min_distance_to_other_uav < 5:
                min_distance_to_danger -= (5 - min_distance_to_other_uav)

            score = min_distance_to_danger

            # the direction with the highest score
            if score > max_score:
                max_score = score
                best_direction = direction

        return best_direction

    def convert_direction_to_int(self, direction_str):
        direction_map = {
            "east": 0,
            "south": 1,
            "west": 2,
            "north": 3,
            "stay": 4  
        }
        return direction_map.get(direction_str.lower(), 0)

    def execute(self):
        super().execute()
        return True
