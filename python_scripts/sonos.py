
"""       Requires python_script: to be enabled in you configuration       """


""" Usage:                                                                 """
"""                                                                        """
""" automation:                                                            """
"""   alias: Refresh John's birthday sensor                                """
"""   trigger:                                                             """
"""     platform: time                                                     """
"""     at: '00:00:01'                                                     """
"""   action:                                                              """
"""     service: python_script.date_countdown                              """
"""     data:                                                              """
"""       action: ungroup                                                       """
"""       speakers: 
            - living room
            - study                                                   """
"""      source: tv                                   """

dom = 'media_player'
test = { "action": "join", "speakers": "media_player.living room, media_player.kitchen" }
sources = {'Line-in', 'TV'}
actions = {'join', 'unjoin'}

action = data.get('action')
logger.info(action)
speakers = data.get('speakers')
logger.info(speakers)
source = data.get('source')
logger.info(source)

if action in actions:
    if action == 'join':
        service = 'sonos_join' 
        service_data = { "master": speakers[0], "entity_id": speakers[1:] }
    else:
        service = 'sonos_unjoin'
        service_data = { "entity_id": speakers }
    hass.call(dom, service, service_data )

if source is sources:
    speaker = 'media_player.study' if source == 'Line-in' else 'media_player.living_room'
    hass.call(dom, 'select_source', { "entity_id": speaker, " source": source } )
