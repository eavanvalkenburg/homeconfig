
blind_name = 'cover.blind'
blind_state = hass.states.get(blind_name)
blind_height = blind_state.attributes.get('current_position')

temp_inside = float(hass.states.get('sensor.study_temperature').state)
temp_outside = float(hass.states.get('sensor.weather_temperature').state)

sun_elevation = float(hass.states.get('sensor.sun_elevation').state)
sun_azimuth = float(hass.states.get('sensor.sun_azimuth').state)

clear_day_sensor =  int(hass.states.get('sensor.clear_day').state)
clear_day = True if clear_day_sensor > 0 else False

# logger.warning('current height: ' + str(blind_height))
# logger.warning(sun_elevation)
# logger.warning(clear_day)

sun = { 
    "elevation_min": 14,
    "elevation_max": 53,
    "azimuth_min": 162,
    "azimuth_max": 250
    }

temp_thresholds = { 
    "inside": 19, 
    "outside": 17
    }

new_position = 100
if sun_elevation < 0:
    new_position = 0
if  clear_day \
and temp_inside > temp_thresholds["inside"] \
and temp_outside > temp_thresholds["outside"] \
and sun_elevation < sun["elevation_max"] \
and sun_elevation > sun["elevation_min"] \
and sun_azimuth < sun["azimuth_max"] \
and sun_azimuth > sun["azimuth_min"]:
    new_position = ((15*sun_elevation*sun_elevation)/77)-((1005*sun_elevation)/77)+(2690/11)

# logger.warning(new_position)
if blind_height != new_position:
    hass.services.call('cover', 'set_cover_position', {'entity_id': blind_name, "position": new_position})