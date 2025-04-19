from __future__ import annotations

import asyncio
import struct
import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator, UpdateFailed
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)
DOMAIN = "ff_le_03mw"


SENSORS = [
    # Napięcia fazowe
    {"name": "Napięcie L1", "address": 14, "unit": "V", "device_class": SensorDeviceClass.VOLTAGE},
    {"name": "Napięcie L2", "address": 16, "unit": "V", "device_class": SensorDeviceClass.VOLTAGE},
    {"name": "Napięcie L3", "address": 18, "unit": "V", "device_class": SensorDeviceClass.VOLTAGE},

    # Częstotliwość
    {"name": "Częstotliwość", "address": 20, "unit": "Hz", "device_class": SensorDeviceClass.FREQUENCY},

    # Prądy fazowe
    {"name": "Prąd L1", "address": 22, "unit": "A", "device_class": SensorDeviceClass.CURRENT},
    {"name": "Prąd L2", "address": 24, "unit": "A", "device_class": SensorDeviceClass.CURRENT},
    {"name": "Prąd L3", "address": 26, "unit": "A", "device_class": SensorDeviceClass.CURRENT},

    # Moc czynna
    {"name": "Moc czynna", "address": 28, "unit": "kW", "device_class": SensorDeviceClass.POWER},
    {"name": "Moc czynna L1", "address": 30, "unit": "kW", "device_class": SensorDeviceClass.POWER},
    {"name": "Moc czynna L2", "address": 32, "unit": "kW", "device_class": SensorDeviceClass.POWER},
    {"name": "Moc czynna L3", "address": 34, "unit": "kW", "device_class": SensorDeviceClass.POWER},

    # Moc bierna
    {"name": "Moc bierna", "address": 36, "unit": "kVAr", "device_class": None},
    {"name": "Moc bierna L1", "address": 38, "unit": "kVAr", "device_class": None},
    {"name": "Moc bierna L2", "address": 40, "unit": "kVAr", "device_class": None},
    {"name": "Moc bierna L3", "address": 42, "unit": "kVAr", "device_class": None},

    # Moc pozorna
    {"name": "Moc pozorna", "address": 44, "unit": "kVA", "device_class": None},
    {"name": "Moc pozorna L1", "address": 46, "unit": "kVA", "device_class": None},
    {"name": "Moc pozorna L2", "address": 48, "unit": "kVA", "device_class": None},
    {"name": "Moc pozorna L3", "address": 50, "unit": "kVA", "device_class": None},

    # Współczynnik mocy
    {"name": "Współczynnik mocy", "address": 52, "unit": "", "device_class": None},
    {"name": "Współczynnik mocy L1", "address": 54, "unit": "", "device_class": None},
    {"name": "Współczynnik mocy L2", "address": 56, "unit": "", "device_class": None},
    {"name": "Współczynnik mocy L3", "address": 58, "unit": "", "device_class": None},

    # Energia czynna – całkowita, fazowa, pobrana, oddana
    {"name": "Energia czynna całkowita", "address": 256, "unit": "kWh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia czynna L1", "address": 258, "unit": "kWh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia czynna L2", "address": 260, "unit": "kWh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia czynna L3", "address": 262, "unit": "kWh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia czynna pobrana", "address": 264, "unit": "kWh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia czynna pobrana L1", "address": 266, "unit": "kWh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia czynna pobrana L2", "address": 268, "unit": "kWh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia czynna pobrana L3", "address": 270, "unit": "kWh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia czynna oddana", "address": 272, "unit": "kWh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia czynna oddana L1", "address": 274, "unit": "kWh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia czynna oddana L2", "address": 276, "unit": "kWh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia czynna oddana L3", "address": 278, "unit": "kWh", "device_class": SensorDeviceClass.ENERGY},

    # Energia bierna – całkowita, fazowa, pobrana, oddana
    {"name": "Energia bierna całkowita", "address": 280, "unit": "kVArh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia bierna L1", "address": 282, "unit": "kVArh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia bierna L2", "address": 284, "unit": "kVArh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia bierna L3", "address": 286, "unit": "kVArh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia bierna pobrana", "address": 288, "unit": "kVArh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia bierna pobrana L1", "address": 290, "unit": "kVArh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia bierna pobrana L2", "address": 292, "unit": "kVArh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia bierna pobrana L3", "address": 294, "unit": "kVArh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia bierna oddana", "address": 296, "unit": "kVArh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia bierna oddana L1", "address": 298, "unit": "kVArh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia bierna oddana L2", "address": 300, "unit": "kVArh", "device_class": SensorDeviceClass.ENERGY},
    {"name": "Energia bierna oddana L3", "address": 302, "unit": "kVArh", "device_class": SensorDeviceClass.ENERGY},
]

READ_BLOCKS = [
    {"start": 14, "length": 48},
    {"start": 256, "length": 48},
]

async def async_setup_entry(hass, config_entry: ConfigEntry, async_add_entities):
    client = hass.data[DOMAIN]["client"]
    slave_id = config_entry.data.get("slave", 5)

    if slave_id == 3:
        _LOGGER.warning("Pomijam konfigurację Modbus dla slave_id=3")
        return

    coordinator = FFCoordinator(hass, client, slave_id)

    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        _LOGGER.warning(f"Błąd pierwszego odczytu Modbus: {err} – encje zostaną dodane jako 'unavailable'")

    async_add_entities([
        FFLE03MWSensor(coordinator, s["name"], s["address"], s["unit"], s["device_class"], slave_id)
        for s in SENSORS
    ])


class FFCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, client, slave_id: int):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
        self._client = client
        self._slave_id = slave_id
        self._lock = asyncio.Lock()

    async def _async_update_data(self):
        data = {}
        try:
            async with self._lock:
                for block in READ_BLOCKS:
                    _LOGGER.debug(f"[MODBUS] Czytam blok {block['start']} (slave {self._slave_id})")
                    result = await self._client.read_holding_registers(
                        address=block["start"],
                        count=block["length"],
                        slave=self._slave_id,
                    )
                    if result.isError():
                        raise Exception(f"Błąd odczytu blok {block['start']}")
                    for i, value in enumerate(result.registers):
                        data[block["start"] + i] = value
        except asyncio.exceptions.InvalidStateError as e:
            _LOGGER.warning(f"[MODBUS] Ignoruję InvalidStateError (błąd pymodbus 3.x): {e}")
            return self.data or {}
        except Exception as err:
            raise UpdateFailed(f"Błąd komunikacji Modbus: {err}")
        return data


class FFLE03MWSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, name, address, unit, device_class, slave_id):
        super().__init__(coordinator)
        self._address = address
        self._attr_name = name
        self._attr_native_unit_of_measurement = str(unit)
        self._attr_device_class = device_class
        self._attr_unique_id = f"{DOMAIN}_{slave_id}_{address}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, str(slave_id))},
            "name": "F&F LE-03MW",
            "manufacturer": "F&F",
            "model": "LE-03MW",
        }

    @property
    def native_value(self):
        try:
            low = self.coordinator.data.get(self._address)
            high = self.coordinator.data.get(self._address + 1)
            if low is None or high is None:
                return None
            packed = struct.pack(">HH", low, high)
            return round(struct.unpack(">f", packed)[0], 2)
        except Exception as e:
            _LOGGER.warning(f"Nie można odczytać {self._attr_name} (reg {self._address}): {e}")
            return None