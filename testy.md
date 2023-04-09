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

# specifikace

## source_station
| C0 | startovaci stanice |
| --- | --- |
| 1 | A |
| 2 | B |
| 3 | C |

## destination_station
| C1 | konečná stanice |
| --- | --- |
| 1 | A |
| 2 | B |
| 3 | C |

## cart_load_capacity
| C2 | nosnost vozíku |
| --- | --- |
| 1 | 50 |
| 2 | 150 |
| 3 | 500 |

## cart_slots
| C3 | počet slotů ve vozíku |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 | 
| 4 | 4 | 

## mode
| C4 | určuje zda je vozík v režimu "pouze-vykládka" |
| --- | --- | 
| 1 | `true` |
| 2 | *false* |

## weight_material
| C5 | určuje zda se material vejde do vozíku váhově |
| --- | --- |
| 1 | `true` |
| 2 | *false* |

## request_uptime
| C6 | čas od naložení materialu na vozík |
| --- | --- |
| 1 | <=1 |
| 2 | 1-2 |
| 3 | >2 |

## Constraints
```
C0.1 -> !C1.1
C0.2 -> !C1.2
C0.3 -> !C1.3
C2.1 -> !C3.1
C2.3 -> !C3.3
C2.3 -> !C3.4
C6.1 -> C5.1 and C4.2 and C5.1
C6.2 -> C4.1 and C5.1
C6.3 -> C4.1 and C5.2 
```

# Combine tabulka
| Test Case ID | C3 | C0 | C1 | C2 | C6 | C4 | C5 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | A | B | 150 | 00:00:24 | false | true | 
| 2 | 1 | B | A | 500 | 00:01:01 | true | true | 
| 3 | 1 | C | A | 150 | 18:48:12 | true | false | 
| 4 | 2 | A | C | 50 | 00:01:01 | true | true | 
| 5 | 2 | B | A | 50 | 00:01:00 | false | true | 
| 6 | 2 | C | B | 500 | 14:23:00 | true | false | 
| 7 | 3 | A | B | 50 | 13:01:37 | true | false | 
| 8 | 3 | B | C | 150 | 00:00:28 | false | true | 
| 9 | 3 | C | A | 50 | 00:01:01 | true | true | 
| 10 | 4 | A | B | 50 | 00:01:01 | true | true | 
| 11 | 4 | B | A | 150 | 12:28:34 | true | false | 
| 12 | 4 | C | A | 50 | 00:01:00 | false | true | 
| 13 | 1 | A | C | 500 | 00:00:52 | false | true | 
| 14 | 4 | A | C | 50 | 12:28:37 | true | false | 
| 15 | 2 | A | A | 150 | 00:00:56 | false | true | 
| 16 | 1 | A | A | 150 | 00:01:01 | true | true | 