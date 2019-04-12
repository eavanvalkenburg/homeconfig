# """       Requires python_script: to be enabled in you configuration       """
# """   action:                                                              """
# """     service: python_script.sonos                                       """
# """     data:                                                              """
# """       action: unjoin/join                                              """
# """       speakers:                                                        """
# """         - living room                                                  """
# """         - study                                                        """
# """      source: blank/TV/Line-in                                          """
# """ testjson = { "action": "join", "speakers": "living room, kitchen" }    """

dom = 'media_player'
sources = {'Line-in', 'TV'}
actions = {'join', 'unjoin'}

action = data.get('action')
logger.info(action)
speakers = data.get('speakers')
if isinstance(speakers, str):
    speakers = [s.strip() for s in speakers.split(',')]
speakers = ["media_player."+s.replace(" ", "_") for s in speakers]
logger.info(speakers)
source = data.get('source', '')
logger.info(source)

if action in actions:
    if action == 'join':
        service = 'sonos_join' 
        service_data = { "master": speakers[0], "entity_id": speakers[1:] }
    else:
        service = 'sonos_unjoin'
        service_data = { "entity_id": speakers }
    hass.services.call(dom, service, service_data )

if source in sources:
    speaker = 'media_player.study' if source == 'Line-in' else 'media_player.living_room'
    hass.services.call(dom, 'select_source', { "entity_id": speaker, " source": source } )
