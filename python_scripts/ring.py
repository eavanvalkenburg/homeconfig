import asyncio
media_dom = 'media_player'

sonos_to_check = \
    ['media_player.study', 
    'media_player.living_room', 
    'media_player.kitchen']

plex = 'media_player.xboxone_plex'
plex_state = hass.states.get(plex)
logger.info(plex_state)
if plex_state == 'playing':
    logger.info('Pausing plex (when running)')
    # hass.services.call(media_dom, 'media_pause', {"entity_id": plex})
else:
    logger.info(f'No pausing {plex} is {plex_state}')

for speaker in sonos_to_check:
    state = hass.states.get(speaker)
    if state == 'playing':
        logger.info(state)
        volume_level = state.get('volume_level', 0.2)
        service_data = { "entity_id": speaker, "volume_level": volume_level/2 }
        logger.info(f'Setting volume of {speaker} to {volume_level/2}')
        # hass.services.call(media_dom, 'volume_set', service_data)

asyncio.sleep(300)

for speaker in sonos_to_check:
    state = hass.states.get(speaker)
    if state == 'playing':
        logger.info(state)
        volume_level = state.get('volume_level', 0.1)
        service_data = { "entity_id": speaker, "volume_level": volume_level*2 }
        logger.info(f'Setting volume of {speaker} to {volume_level*2}')
        # hass.services.call(media_dom, 'volume_set', service_data)
