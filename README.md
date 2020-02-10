*This API changes (overwrites) standard API dictionary (json) keys.*
# The Volganet Timetable API for Buses, Trolleybuses and Trams. Written on Python 3.6.8.
## How to use
Download. Put in your project folder. Import it. Use it.  
```python
from volganet_timetable import VolganetTimetable
```
## Methods explanations
### get_all_routes()
Get all routes, which include all types of transport.  
```python
vt = VolganetTimetable()
routes = vt.get_all_routes()
```
Return array of transport objects. Each **transport** contains fields:

Field | Description |
----- | ----------- |
id | ID of transport type:<br/> 1. Bus<br/> 2. Trolleybus<br/> 3. Tram<br/> |
title | RU name of transport type |
title_en | EN name of transport type |
routes | Array of all routes |  

Each **route** contains fields:

Field | Description |
----- | ----------- |
id | ID of route |
num | Local number of route |
title | RU path name of transport route |
title_en | EN path name of transport route |

### get_routes_by_local_num(route_type, routes_numbers = [])
Get all routes for selected local routes: 55, 1A, 55K and etc.  
Method parameters:  

Parameter | Description |
--------- | ----------- |
route_type | ID of transport type:<br/> 1. Bus<br/> 2. Trolleybus<br/> 3. Tram<br/> |
routes_numbers | Array of local transport numbers |

```python
vt = VolganetTimetable()
routes = vt.get_routes_by_local_num(1, [55, "1A"])
```
Return array of routes objects. Each **route** contains fields:

Field | Description |
----- | ----------- |
id | ID of route |
num | Local number of route |
title | RU path name of transport route |
title_en | EN path name of transport route |

### get_route_race_tree(route_id, date = "")
Get full information of route.
Method parameters:  

Parameter | Description |
--------- | ----------- |
route_id | ID of route |
date | Route date. If date not specified, current date will set in |

```python
vt = VolganetTimetable()
routes = vt.get_routes_by_local_num(1, [55, "1A"])
race_tree = vt.get_route_race_tree(routes[0]["id"])
```
Return array of two object: beginning station and ending station. Each **station** object contains fields:

Field | Description |
----- | ----------- |
id | ID of route |
racetype | A -> it's beginning station.<br/>B -> it's ending station |
firststation_id | ID of first station |
laststation_id | ID of last station |
firststation | RU name of station |
firststation_en | EN name of station |
laststation | RU name of station |
laststation_en | EN name of station |
stopList | Array of all stations on this route |

Each **station** contains fields:

Field | Description |
----- | ----------- |
id | ID of station |
title | RU name of station |
title_en | EN name of station |

### get_route_timetable(route_id, route_number, direction, date = "", station_id = 0)
Get route timetable.  
Method parameters:

Parameter | Description |
--------- | ----------- |
route_id | ID of route |
route_number | Local number of route |
direction | A -> it's beginning station.<br/>B -> it's ending station |
date | Route date. If date not specified, current date will set in |
station_id | Start station if stop stations list |

```python
vt = VolganetTimetable()
routes = vt.get_routes_by_local_num(1, [55, "1A"])
timetable = vt.get_route_timetable(routes[0]["id"], routes[0]["num"], "A")
```
Return **timetable** object, which contains fields:

Field | Description |
----- | ----------- |
id | ID of timetable |
startdate | Timetable adoption date |
enddate | Timetable end date |
enddateexists | 1 -> Yes<br/>0 -> None |
stopList | Array of all stations on this route with times |

Each **station** contains fields:

Field | Description |
----- | ----------- |
id | ID of station |
title | RU name of station |
title_en | EN name of station |
times | Array of datetime.time objects |

## Afterword
It's not official Volganet API. Hope you enjoy.  
Created by Evgeny Gribanov.
