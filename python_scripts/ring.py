
media_dom = 'media_player'

sonos_to_check = \
    ['media_player.study', 
    'media_player.living_room', 
    'media_player.kitchen']

plex = 'media_player.xboxone_plex'
plex_state = hass.states.get(plex)
# logger.debug(plex_state)
# logger.debug(plex_state.attributes)
if plex_state.state == 'playing':
    logger.debug('Pausing plex (when running)')
    hass.services.call(media_dom, 'media_pause', {"entity_id": plex})
# else:
#     logger.debug('No pausing {}, state is {}'.format(plex, plex_state))

states = {}
for speaker in sonos_to_check:
    states[speaker] = hass.states.get(speaker)

for speaker, state in states.items():
    if state.state == 'playing':
        # logger.debug(state)
        volume_level = state.attributes.get('volume_level', 0.2)
        service_data = { "entity_id": speaker, "volume_level": volume_level/2 }
        # logger.debug('Setting volume of {} to {}'.format(speaker, volume_level/2))
        hass.services.call(media_dom, 'volume_set', service_data)

time.sleep(120)

for speaker, state in states.items():
    if state.state == 'playing':
        # logger.debug(state)
        volume_level = state.attributes.get('volume_level', 0.1)
        service_data = { "entity_id": speaker, "volume_level": volume_level }
        # logger.debug('Setting volume of {} to {}'.format(speaker, volume_level))
        hass.services.call(media_dom, 'volume_set', service_data)
