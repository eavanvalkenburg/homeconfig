
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
test = { "action": "join", "speakers": "living room, kitchen" }
sources = {'Line-in', 'TV'}
actions = {'join', 'unjoin'}

action = data.get('action')
logger.warning(action)
speakers = data.get('speakers')
if isinstance(speakers, str):
    speakers = [s.strip() for s in speakers.split(',')]
speakers = ["media_player."+s.replace(" ", "_") for s in speakers]
logger.warning(speakers)
source = data.get('source', '')
logger.warning(source)

if action in actions:
    if action == 'join':
        service = 'sonos_join' 
        service_data = { "master": speakers[0], "entity_id": speakers[1:] }
    else:
        service = 'sonos_unjoin'
        service_data = { "entity_id": speakers }
    hass.services.call(dom, service, service_data )

if source is sources:
    speaker = 'media_player.study' if source == 'Line-in' else 'media_player.living_room'
    hass.services.call(dom, 'select_source', { "entity_id": speaker, " source": source } )
