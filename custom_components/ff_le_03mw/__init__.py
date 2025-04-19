from __future__ import annotations

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from pymodbus.client import AsyncModbusTcpClient
import asyncio

from .const import DOMAIN, CONF_HOST, CONF_PORT

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the FF LE-03MW integration."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up FF LE-03MW from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]

    client = AsyncModbusTcpClient(host, port=port)
    await client.connect()

    # Inicjalizuj globalny lock (jeśli jeszcze nie ma)
    if "lock" not in hass.data[DOMAIN]:
        hass.data[DOMAIN]["lock"] = asyncio.Lock()

    hass.data[DOMAIN]["client"] = client
    hass.data[DOMAIN]["entry_data"] = entry.data

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop("client", None)
        hass.data[DOMAIN].pop("entry_data", None)
        # lock celowo zostaje – może być używany przez inne wpisy

    return unload_ok
