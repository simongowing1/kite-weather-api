from dataclasses import dataclass


@dataclass
class KiteConditions:
    min_wind_kmh: float = 15.0
    max_wind_kmh: float = 50.0


CONDITIONS = KiteConditions()


def assess(wind_speed_kmh: float, conditions: KiteConditions = CONDITIONS) -> tuple[bool, str]:
    if wind_speed_kmh < conditions.min_wind_kmh:
        return False, f"Too calm — wind is only {wind_speed_kmh} km/h (need at least {conditions.min_wind_kmh})"
    if wind_speed_kmh > conditions.max_wind_kmh:
        return False, f"Too strong — wind is {wind_speed_kmh} km/h (max safe is {conditions.max_wind_kmh})"
    return True, f"Great kite weather — wind is {wind_speed_kmh} km/h"
