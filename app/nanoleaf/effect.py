from app.nanoleaf.model import AuroraObject
import socket
import random


class AuroraStream:
    def __init__(self, addr: str, port: int):
        self._prepare = []
        self.addr = (addr, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1)

    def __send(self, msg: bytes):
        self.sock.sendto(msg, self.addr)

    def panel_set(self, panel_id: int, red: int, green: int, blue: int,
                  white: int = 0, transition_time: int = 1):
        b = bytes([1, panel_id, 1, red, green, blue, white, transition_time])
        self.__send(b)

    def panel_prepare(self, panel_id: int, red: int, green: int, blue: int,
                      white: int = 0, transition_time: int = 1):
        self._prepare = self._prepare + [panel_id, 1, red, green, blue, white, transition_time]

    def panel_strobe(self):
        data = [len(self._prepare)] + self._prepare
        self._prepare = []
        self.__send(bytes(data))


class Effect(AuroraObject):

    def __init__(self, requester):
        super().__init__(requester)

    _reserved_effect_names = ["*Static*", "*Dynamic*", "*Solid*"]

    @property
    def effect(self):
        """Returns the active effect"""
        return self.__requester.request(method="GET", endpoint="effects/select")

    @effect.setter
    def effect(self, effect_name: str):
        """Sets the active effect to the name specified"""
        data = {"select": effect_name}
        self.__requester.request(method="PUT", endpoint="effects", data=data)

    @property
    def effects_list(self):
        """Returns a list of all effects stored on the device"""
        return self.__requester.request(method="GET", endpoint="effects/effectsList")

    def effect_random(self) -> str:
        """Sets the active effect to a new random effect stored on the device.

        Returns the name of the new effect."""
        effect_list = self.effects_list
        active_effect = self.effect
        if active_effect not in self._reserved_effect_names:
            effect_list.remove(self.effect)
        new_effect = random.choice(effect_list)
        self.effect = new_effect
        return new_effect

    def effect_set_raw(self, effect_data: dict):
        """Sends a raw dict containing effect data to the device.

        The dict given must match the json structure specified in the API docs."""
        data = {"write": effect_data}
        self.__requester.request(method="PUT", endpoint="effects", data=data)

    def effect_details(self, name: str) -> dict:
        """Returns the dict containing details for the effect specified"""
        data = {"write": {"command": "request",
                          "animName": name}}
        return self.__requester.request(method="PUT", endpoint="effects", data=data)

    def effect_details_all(self) -> dict:
        """Returns a dict containing details for all effects on the device"""
        data = {"write": {"command": "requestAll"}}
        return self.__requester.request(method="PUT", endpoint="effects", data=data)

    def effect_delete(self, name: str):
        """Removed the specified effect from the device"""
        data = {"write": {"command": "delete",
                          "animName": name}}
        self.__requester.request(method="PUT", endpoint="effects", data=data)

    def effect_rename(self, old_name: str, new_name: str):
        """Renames the specified effect saved on the device to a new name"""
        data = {"write": {"command": "rename",
                          "animName": old_name,
                          "newName": new_name}}
        self.__requester.request(method="PUT", endpoint="effects", data=data)

    def effect_stream(self):
        """Open an external control stream"""
        data = {"write": {"command": "display",
                          "animType": "extControl"}}

        udp_info = self.__requester.request(method="PUT", endpoint="effects", data=data)
        return AuroraStream(udp_info["streamControlIpAddr"], udp_info["streamControlPort"])
