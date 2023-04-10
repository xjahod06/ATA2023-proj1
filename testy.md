# CEG graf
| | popis | test 1 | test 2 | test 3 | test 4 |
| --- | --- | --- | --- | --- | --- |
| 1 | náklad materialu do 1 minuty od založení požadavku | 1 | 0 | 0 | 0 |
| 2 | čas >= 1 minuta od nastavení požadavku | 0 | 1 | 0 | 1 |
| 3 | náklad materialu s prioritním atributem na 1 | 0 | 1 | 0 | 1 |
| 5 | čas >= 1 minuta od nastavení prioritního požadavku | 0 | 0 | 1 | 0 |
| 6 | vozík má ve svém slotu material s prioritním atributem 1 | 0 | 0 | 0 | 1 |
| 7 | vozík má volný dostatečný počet slotů pro material | 1 | 1 | 1 | 0 |
| 8 | naložením nákladu se nepřekročí hmotnostní limit | 1 | 1 | 0 | 0 |
| 40 | naložení materiálu na vozík | `true` | *false* | *false* | *false* |
| 41 | nastavení atributu priority materialu na 1 | *false* | `true` | *false* | `true` |
| 42 | naložení prioritního materialu na vozík | *false* | `true` | *false* | *false* |
| 43 | uložení požadavku do logu nestihnutých požadavku | *false* | *false* | `true` | *false* |
| 44 | nastavení vozíku do režimu pouze vykládka | *false* | `true` | *false* | `true` |
| 45 | zůstání v řežimu pouze vykládka | *false* | *false* | *false* | `true` |

# parametry testů

| název parametru | popis parametru |
| --- | --- |
| `source_station` | startovní stanice materialu |
| `destination_station` | konečná stanice materialu |
| `request_uptime` | čas od vzniku požadavku |
| `weight_material` | váha materialu |
| `cart_load_capacity` | nosnost vozíku |
| `cart_slots` | počet slotů ve vozíku |
| `mode` | určuje zda je vozík v režimu "pouze-vykládka" |

request_uptime# specifikace

## source_station
| source_station | startovaci stanice |
| --- | --- |
| 1 | A |
| 2 | B |
| 3 | C |

## destination_station
| destination_station | konečná stanice |
| --- | --- |
| 1 | A |
| 2 | B |
| 3 | C |

## cart_load_capacity
| cart_load_capacity | nosnost vozíku |
| --- | --- |
| 1 | 50 |
| 2 | 150 |
| 3 | 500 |

## cart_slots
| cart_slots | počet slotů ve vozíku |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 | 
| 4 | 4 | 

## mode
| mode | určuje zda je vozík v režimu "pouze-vykládka" |
| --- | --- | 
| 1 | `true` |
| 2 | *false* |

## weight_material
| weight_material | určuje zda se material vejde do vozíku váhově |
| --- | --- |
| 1 | `true` |
| 2 | *false* |

## request_uptime
| request_uptime | čas od naložení materialu na vozík |
| --- | --- |
| 1 | <=1 |
| 2 | 1-2 |
| 3 | >2 |

## Constraints
```
source_station.1 -> !destination_station.1
source_station.2 -> !destination_station.2
source_station.3 -> !destination_station.3
cart_load_capacity.1 -> !cart_slots.1
cart_load_capacity.3 -> !cart_slots.3
cart_load_capacity.3 -> !cart_slots.4
request_uptime.1 -> weight_material.1 and mode.2
request_uptime.2 -> mode.1 and weight_material.1
request_uptime.3 -> mode.1 and weight_material.2 
```

# Combine tabulka
při využití nástroje combiner se objevila chyba, kdy nástroj pro poslední 4 kombinace vyignorovla constrain `source_station.1 -> !destination_station.1`, tyto řádky jsem tedy ručně vymazal

| Test Case ID | cart_slots | source_station | destination_station | request_uptime | cart_load_capacity | weight_material | mode |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | A | B | 00:01:00 | 150 | true | false |
| 2 | 1 | B | A | 00:01:01 | 500 | true | true |
| 3 | 1 | C | A | 15:45:42 | 150 | false | true |
| 4 | 2 | A | C | 00:01:01 | 50 | true | true |
| 5 | 2 | B | A | 00:00:44 | 50 | true | false |
| 6 | 2 | C | B | 00:01:01 | 500 | true | true |
| 7 | 3 | A | B | 14:08:53 | 50 | false | true |
| 8 | 3 | B | C | 00:01:00 | 150 | true | false |
| 9 | 3 | C | A | 00:00:52 | 50 | true | false |
| 10 | 4 | A | B | 00:01:00 | 50 | true | false |
| 11 | 4 | B | A | 12:28:37 | 150 | false | true |
| 12 | 4 | C | A | 00:01:01 | 150 | true | true |
| 13 | 1 | A | C | 12:28:34 | 500 | false | true |
| 14 | 4 | A | C | 00:00:28 | 50 | true | false |

# Testy
| test ID | popis | pokrytí CEG | pokrytí combine | výsledek |
| --- | --- | --- | --- | --- |
| 1 | spracování požadavku do jedné minuty od vytvoření | 1 | 1,5,8,12,13,15