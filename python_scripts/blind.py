# name = data.get('name', 'world')

# logger.info("Hello {}".format(name))
blind_height = hass.states.get('cover.blind')
logger.warning(f'current height: {blind_height}')
