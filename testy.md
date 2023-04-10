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
| `free_weight` | určuje zda je volná váhová kapacita |
| `free_slots` | určuje zda je volný dostatečný počet slotu ve vozíku |
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

## free_slots
| free_slots | určuje zda je volný dostatečný počet slotu ve vozíku |
| --- | --- | 
| 1 | `true` |
| 2 | *false* |

## mode
| mode | určuje zda je vozík v režimu "pouze-vykládka" |
| --- | --- | 
| 1 | `true` |
| 2 | *false* |

## free_weight
| free_weight | určuje zda se material vejde do vozíku váhově |
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
request_uptime.1 -> free_weight.1 and mode.2 and free_slots.1
request_uptime.2 -> mode.1 and free_weight.1 and free_slots.1
request_uptime.3 -> mode.1 and (free_weight.2 or free_slots.2)
```

# Combine tabulka

| Test Case ID | source_station | destination_station | request_uptime | mode | free_weight | free_slots |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | A | B | 00:01:00 | false | true | true |
| 2 | A | C | 00:01:01 | true | true | true |
| 3 | B | A | 00:00:28 | false | true | true |
| 4 | B | C | 19:26:41 | true | false | false |
| 5 | C | A | 00:01:01 | true | true | true |
| 6 | C | B | 16:59:33 | true | false | true |
| 7 | C | A | 00:01:00 | false | true | true |
| 8 | B | A | 18:47:57 | true | true | false |
| 9 | A | B | 00:01:01 | true | true | true |
| 10 | B | A | 00:01:01 | true | true | true |
| 11 | A | B | 18:47:56 | true | false | false |
| 12 | A | C | 00:00:56 | false | true | true |
| 13 | B | A | 12:28:34 | true | false | true |
| 14 | C | A | 14:30:12 | true | true | false |

# Testy
| test ID | popis | pokrytí CEG | pokrytí combine | výsledek |
| --- | --- | --- | --- | --- |
| 1 | spracování požadavku do jedné minuty od vytvoření | 1 | 1,5,8,12,13,15