"""Support for Azure Event Hubs."""
import json
import logging
from typing import Any, Dict

import voluptuous as vol
from azure.eventhub import EventData, EventHubClientAsync

from homeassistant.const import (
    EVENT_HOMEASSISTANT_STOP,
    EVENT_STATE_CHANGED,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)
from homeassistant.core import Event, HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entityfilter import FILTER_SCHEMA
from homeassistant.helpers.json import JSONEncoder

_LOGGER = logging.getLogger(__name__)

DOMAIN = "azure_event_hub_new"

CONF_EVENT_HUB_NAMESPACE = "event_hub_namespace"
CONF_EVENT_HUB_INSTANCE_NAME = "event_hub_instance_name"
CONF_EVENT_HUB_SAS_POLICY = "event_hub_sas_policy"
CONF_EVENT_HUB_SAS_KEY = "event_hub_sas_key"
CONF_EVENT_HUB_CON_STRING = "event_hub_connection_string"
CONF_IOT_HUB_CON_STRING = "iot_hub_connection_string"
CONF_FILTER = "filter"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Any(
            vol.Schema(
                {
                    vol.Required(CONF_IOT_HUB_CON_STRING): cv.string,
                    vol.Optional(CONF_FILTER, default={}): FILTER_SCHEMA,
                }
            ),
            vol.Schema(
                {
                    vol.Required(CONF_EVENT_HUB_CON_STRING): cv.string,
                    vol.Optional(CONF_FILTER, default={}): FILTER_SCHEMA,
                }
            ),
            vol.Schema(
                {
                    vol.Required(CONF_EVENT_HUB_NAMESPACE): cv.string,
                    vol.Required(CONF_EVENT_HUB_INSTANCE_NAME): cv.string,
                    vol.Required(CONF_EVENT_HUB_SAS_POLICY): cv.string,
                    vol.Required(CONF_EVENT_HUB_SAS_KEY): cv.string,
                    vol.Optional(CONF_FILTER, default={}): FILTER_SCHEMA,
                }
            ),
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, yaml_config: Dict[str, Any]):
    """Activate Azure EH component."""
    config = yaml_config[DOMAIN]

    entities_filter = config[CONF_FILTER]
    if config[CONF_IOT_HUB_CON_STRING]:
        client = EventHubClientAsync.from_iot_connection_string(
            config[CONF_IOT_HUB_CON_STRING]
        )
    elif config[CONF_EVENT_HUB_CON_STRING]:
        client = EventHubClientAsync.from_connection_string(
            config[CONF_EVENT_HUB_CON_STRING]
        )
    else:
        event_hub_address = "amqps://{}.servicebus.windows.net/{}".format(
            config[CONF_EVENT_HUB_NAMESPACE], config[CONF_EVENT_HUB_INSTANCE_NAME]
        )
        client = EventHubClientAsync(
            event_hub_address,
            username=config[CONF_EVENT_HUB_SAS_POLICY],
            password=config[CONF_EVENT_HUB_SAS_KEY],
        )

    async_sender = client.add_async_sender()
    await client.run_async()

    # encoder = JSONEncoder()

    async def async_send_to_event_hub(event: Event):
        """Send states to Event Hub."""
        state = event.data.get("new_state")
        if (
            state is None
            or state.state in (STATE_UNKNOWN, "", STATE_UNAVAILABLE)
            or not entities_filter(state.entity_id)
        ):
            return

        event_data = EventData(
            json.dumps(obj=state, cls=JSONEncoder).encode("utf-8")
            # json.dumps(obj=state.as_dict(), default=encoder.default).encode("utf-8")
        )
        try:
            await async_sender.send(event_data)
        except AttributeError:
            await async_sender.reconnect_async()
            await async_sender.send(event_data)

    async def async_shutdown(event: Event):
        """Shut down the client."""
        await client.stop_async()

    hass.bus.async_listen(EVENT_STATE_CHANGED, async_send_to_event_hub)
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, async_shutdown)

    return True
