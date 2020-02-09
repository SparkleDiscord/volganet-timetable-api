import requests
from re import sub
from datetime import date as d
from datetime import time as t

class VolganetTimetable:
    def __init__(self):
        self.methods_count = 0
        self.sid = self.__get_sid()
    
    def __create_post(self, method_name, params = {}):
        self.methods_count += 1
        res = requests.post("https://transport.volganet.ru/api/rpc.php",
            json={"jsonrpc": "2.0","method": method_name,"params":params, "id": self.methods_count},
            headers={
                "Content-Type":"application/json", 
                "Host":"transport.volganet.ru", 
                "Origin": "https://transport.volganet.ru", 
                "Referer": "https://transport.volganet.ru/main.php",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin"
            }
        )
        return res.json()["result"]

    def __get_sid(self):
        return self.__create_post("startSession")["sid"]

    def __clear_keys(self, bk_dictionary):
        if not isinstance(bk_dictionary, (list, dict)):
            return bk_dictionary

        for key in bk_dictionary.copy():
            try:
                bk_dictionary[key] = self.__clear_keys(bk_dictionary[key])
                bk_dictionary[sub(r"(mr_)|(tt_)|(rl_)|(rc_)|(st_)|(rv_)", '', key)] = bk_dictionary.pop(key)
            except:
                idx = bk_dictionary.index(key)
                bk_dictionary[idx] = self.__clear_keys(bk_dictionary[idx])
        return bk_dictionary

    def get_all_routes(self):
        params = {
            "sid": self.sid,
            "ok_id": ""
        }
        return self.__clear_keys(self.__create_post("getTransTypeTree", params))

    """
        r_type values:
        tt_id = 1 -> Автобус    - Bus
        tt_id = 2 -> Троллейбус - Trolleybus
        tt_id = 3 -> Трамвай    - Tram
    """
    def get_routes_by_transport_num(self, route_type, routes_numbers = []):
        timetable = self.get_all_routes()
        return [
            route 
            for route in timetable[route_type - 1]["routes"] 
            if route["num"] in routes_numbers
        ]

    """
        Get all stations on this route from A to B
    """
    def get_route_race_tree(self, route_id, date = ""):
        if date == "":
            date = d.today().strftime("%Y-%m-%d")
        params = {
            "sid": self.sid,
            "mr_id": route_id,
            "data": date
        }
        race_tree = self.__clear_keys(self.__create_post("getRaceTree", params))
        for i in range(0,1):
            race_tree[i]["stopList"] = [x for x in race_tree[i]["stopList"] if x["orderby"] > 0]
        return race_tree

    """
        direction values:
        A -> B
        B <- A
    """
    def get_route_timetable(self, route_id, transport_number, direction, date = "", station_id = 0):
        if date == "":
            date = d.today().strftime("%Y-%m-%d")
        params = {
            "sid": self.sid,
            "mr_id": route_id,
            "data": date,
            "rl_racetype": direction,
            "rc_kkp": "",
            "st_id": station_id
        }
        timetable = self.__create_post("getRaspisanie", params)
        timetable = self.__clear_keys(timetable)

        for idx in range(len(timetable["stopList"])):
            hours = timetable["stopList"][idx].pop("hours")
            timetable["stopList"][idx]["times"] = []
            for hour in hours:
                for minute in hour["minutes"]:
                    timetable["stopList"][idx]["times"].append(
                        t(
                            int(hour["hour"] if hour["hour"] < 24 else 0),
                            int(minute["minute"])
                        )
                    )
        return timetable
