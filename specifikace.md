Pokud je požadováno přemístění nákladu z jednoho místa do druhého, vozík si materiál vyzvedne do 1 minuty.

    - AMB_STATEMENT, "je požadováno" je nejednoznačné
    - AMB_REFERENCE, "náklad" a "material" odkazuje na stejný objekt
    - AMB_SUBJECT, "místo" je nejednoznačné
    - UNSPECIFIED_SUBJECT, vyzvednutí do 1 min od jakého okamžiku 
    - OMISSION, chybí důsledek této specifikace
  
*Pokud je nastaven požadavek na přemístění materiálu z jedné stanice do druhé a vozík si vyzvedne material do jedné minuty od jeho založení, tak bude tento material naložen na vozík.*

Pokud se to nestihne, materiálu se nastavuje prioritní vlastnost.

    - AMB_SUBJECT, "to" je nejednozačné označení.
    - AMB_TEMPORAL, není jednoznačné co se do kdy nestihne
    - AMB_REFERENCE, není jednoznačné kterému materiálu se nastavuje priorita
    - UNSPECIFIED_SUBJECT, není jednoznačné jak se nastaví prioritní vlastnost
    - AMB_STATEMENT, není jednoznačné pro co se nastavuje priorita

*Pokud se požadavek nestihne vykonat do jedné minuty, tak se materiálu v tomto požadavku nastaví atribut priority na 1 pro přemístění*

Každý prioritní materiál musí být vyzvednutý vozíkem do 1 minuty od nastavení prioritního požadavku.

    - AMB_SUBJECT, není jednoznačné co je prioritní materiál
    - DANGLING_ELSE, není zde napsáno co se stanu pokud material není vyzvednut
    - OMISSION, chybí důsledek této specifikace

*Pokud má material nastaven prioritní atribut na 1 a je vyzvednut do 1 minuty vozíkem s prioritním požadavkem, tak vozík tento material naloží. Pokud se tento požadavek nestihne vykonat do 1 minuty od nastavení požadavku, tak se tento požadavek ukládá do logu nestihnutých požadavků a systém čeká na jeho dokončení.*

Pokud vozík nakládá prioritní materiál, přepíná se do režimu pouze-vykládka.

    - AMB_SUBJECT, není jednoznačné co je prioritní materiál
    - UNSPECIFIED_SUBJECT, není specifikováno co je režim "pouze-vykládka"
    - DANGLING_ELSE, není specifikováno co vozík dělá s neprioritními materialy

*Pokud vozík nakládá materiál, který má nastavenou prioritu na 1, tak si nastavuje atribut režimu na "pouze-vykládka", který znamená, že vozík ignoruje jakýkoliv požadavek na nakládání materiálu a vykládá pouze materiály ve svých slotech, které mají nastavený prioritní atribut na 1. Pokud vozík nakládá materiál, který má nastaven prioritní atribut na 0 tak se do režimu "pouze-vykládka" nepřepíná.*

V tomto režimu zůstává, dokud nevyloží všechen takový materiál.

    - AMB_SUBJECT, není jednoznačné v jakém režimu
    - AMB_SUBJECT, není jednoznačné kdo v tomto režimu zůstává
    - AMB_SUBJECT, není jednoznačné co znamená "takový materiál"

*Když je atribut "režim" vozíku nastaven na "pouze-vykládka", tak v něm zůstává dokud v některém ze svých slotů má materiál, který má nastaven prioritní atribut na 1.*

Normálně vozík během své jízdy může nabírat a vykládat další materiály v jiných zastávkách.

    - AMB_SUBJECT, není jednoznačné co znamená "normálně"
    - DANGLING_ELSE, chybí specifikace pro ostatní režimy
    - AMB_REFERENCE, není konsistentní výraz "zastávka"

*Pokud vozík není v režimu "pouze-vykládka", tak během své jízdy může nakládat a vykládat jiné materiály v jiných stanicích. Pokud je v režimu "pouze-vykládka" tak se chová dle specifikace výše.*

Na jednom místě může vozík akceptovat nebo vyložit jeden i více materiálů.

    - AMB_SUBJECT, není jednoznačné označení "místo"
    - AMB_REFERENCE, není konsistentní označení "akceptovat"
    - AMB_LOGIC, označení "nebo" zde není vhodné protože implikuje výběr.

*Vozík může v jedné stanici naložit i vyložit jeden i více materiálů*

Pořadí vyzvednutí materiálů nesouvisí s pořadím vytváření požadavků.

    - AMB_REFERENCE, označení "vyzvednutí" není konsistentní
    - AMB_STATEMENT, není jednozančné čeho se týká "vytvoření požadavku"

*Pořadí naložených materiálů na vozík nesouvisí s pořadím vytvoření požadavků na přepravu materiálu.*

Vozík neakceptuje materiál, pokud jsou všechny jeho sloty obsazené nebo by jeho převzetím byla překročena maximální nosnost.

    - AMB_REFERENCE, není konsistentní označení "neakceptuje"
    - AMB_REFERENCE, není konsistentní označení "převzetí"
    - UNSPECIFIED_SUBJECT, nespecifikováno k čemu se vztahuje maximální nosnost
    - UNSPECIFIED_SUBJECT, nespeficikováno co dělat pokud se material nevejde do slotů v případě kdy zabere více slotů

*Vozík nenaloží materiál, pokud množství slotů, které zabere material je větší než počet volných slotů na vozíku nebo by jeho naložením byla překročena maximální nosnost daného vozíku.*