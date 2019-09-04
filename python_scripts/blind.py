
blind_name = 'cover.blind'
blind_state = hass.states.get(blind_name)
blind_position = float(blind_state.attributes.get('current_position'))
blind_threshold = float(hass.states.get('input_number.blind_closure').state)

temp_inside = float(hass.states.get('sensor.study_sensor_temperature').state)
temp_outside = float(hass.states.get('sensor.weather_temperature').state)

sun_elevation = float(hass.states.get('sensor.sun_elevation').state)
sun_azimuth = float(hass.states.get('sensor.sun_azimuth').state)

clear_day_sensor =  int(hass.states.get('sensor.clear_day').state)
clear_day = True if clear_day_sensor > 0 else False

previous_position_input = 'input_number.last_set_blind_position'
previous_set_position = float(hass.states.get(previous_position_input).state)

# logger.warning("Timer status: " + hass.states.get('timer.blind_manual_override_timer').state)
# logger.warning("Current blind position: " + str(blind_position))
# logger.warning("Previous set blind position: " + str(previous_set_position))
if hass.states.get('timer.blind_manual_override_timer').state != 'active':
    # logger.warning("Current blind position: " + str(blind_position))
    # logger.warning("Previous set blind position: " + str(previous_set_position))
    if abs(previous_set_position - blind_position) >= 1:
        # manual override triggered
        # logger.warning("Setting timer")
        service_data = {'entity_id': 'timer.blind_manual_override_timer', 'duration': "01:00:00" }
        hass.services.call('timer', 'start', service_data)
        hass.services.call('input_number', 'set_value', {'entity_id': previous_position_input, 'value': blind_position})
    else:
        sun = { 
            "elevation_min": 14,
            "elevation_max": 60,
            "azimuth_min": 162,
            "azimuth_max": 255
            }

        temp_thresholds = { 
            "inside": 19, 
            "outside": 17
            }

        new_position = 100
        if sun_elevation < blind_threshold:
            new_position = 0
        if  clear_day \
        and temp_inside > temp_thresholds["inside"] \
        and temp_outside > temp_thresholds["outside"] \
        and sun_elevation < sun["elevation_max"] \
        and sun_elevation > sun["elevation_min"] \
        and sun_azimuth < sun["azimuth_max"] \
        and sun_azimuth > sun["azimuth_min"]:
            new_position = ((15*sun_elevation*sun_elevation)/77)-((1005*sun_elevation)/77)+(2690/11)

        # logger.warning("New set blind position: " + str(new_position))
        if blind_position != new_position:
            hass.services.call('cover', 'set_cover_position', {'entity_id': blind_name, "position": new_position})
        hass.services.call('input_number', 'set_value', {'entity_id': previous_position_input, 'value': new_position})
