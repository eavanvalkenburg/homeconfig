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

action = data.get('action','')
logger.info(action)

speakers = data.get('speakers','')
if isinstance(speakers, str):
    speakers = [s.strip() for s in speakers.split(',')]
speakers = ["media_player."+s.replace(" ", "_") for s in speakers]
logger.info(speakers)

source = data.get('source', '')
logger.info(source)

if source in sources:
    speaker = 'media_player.study' if source == 'Line-in' else 'media_player.living_room'
    hass.services.call(dom, 'select_source', { "entity_id": speaker, " source": source } )
    hass.services.call(dom, 'media_play', { "entity_id": speaker, })

#get current state from all speakers
states = {}
for s in speakers:
    states[s] = hass.states.get(s)
logger.info(states)

if action in actions:
    if action == 'join':
        for key,value in states.items():
            if value.state == 'playing':
                master = key
                break
        speakers.remove(master)
        service = 'sonos_join' 
        service_data = { "master": master, "entity_id": speakers }
    else:
        service = 'sonos_unjoin'
        service_data = { "entity_id": speakers }
    hass.services.call(dom, service, service_data )

