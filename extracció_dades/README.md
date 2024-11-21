# ProjectManagement

## Extracció de dades

El projecte parteix del dataset **daily_dataset.csv** proporcionat per AGBAR, que inclou dades detallades sobre el consum d’aigua a nivell diari i per secció censal. Aquest dataset constitueix la base principal del nostre model i conté els camps següents:  
- **Secció censal, districte i municipi**: per identificar zones geogràfiques concretes de consum.  
- **Data**: per analitzar la distribució temporal del consum d’aigua.  
- **Ús**: que especifica si l’aigua és utilitzada per a fins domèstics, industrials, comercials, o altres.  
- **Nombre de comptadors**: que indica quants dispositius registren el consum a cada secció.  
- **Consum acumulat (L/dia)**: volum d’aigua consumit diàriament en litres.  

Aquestes dades són indispensables per entendre la variabilitat del consum en funció de la geografia i del tipus d’ús. Tanmateix, per desenvolupar un model que integri els efectes del turisme i d’altres factors externs, necessitem ampliar aquesta informació amb noves fonts de dades:  

1. **Dades meteorològiques**:  
   - **Temperatura màxima i mínima diària**: el clima influeix directament en el consum d’aigua. Per exemple, en dies de calor intensa, el consum augmenta, especialment a zones turístiques amb activitats a l’aire lliure.  
   - **Precipitacions acumulades**: els dies de pluja redueixen el consum d’aigua en activitats a l’exterior, com el reg o les dutxes a platges i piscines.  

   Aquestes dades són crucials per ajustar el model als patrons estacionals i climàtics, que tenen un gran impacte en el consum d’aigua.  

2. **Dades de turisme**:  
   - **Pernoctacions diàries**: necessitem saber quants turistes s’allotgen a la ciutat cada dia. Aquesta informació reflecteix l'impacte del turisme en zones concretes i ajuda a identificar com els fluxos de visitants contribueixen al consum d’aigua en serveis com hotels, restaurants i activitats recreatives.  

   El turisme és un dels factors principals que volem analitzar. Per això, aquestes dades són essencials per segmentar el consum d’aigua atribuïble als visitants, diferenciant-lo del consum residencial o d'altres usos.  

La integració d’aquestes dades ens permetrà desenvolupar un model predictiu que connecti el consum d’aigua amb variables climàtiques i turístiques, oferint prediccions més precises i útils per a la gestió sostenible dels recursos hídrics. Així, podrem respondre preguntes clau, com l’impacte específic del turisme en zones determinades o l’efecte de condicions meteorològiques extremes en el consum global.  

### Extracció Inicial

#### Dades meteorològiques i precipitacions:

  Per millorar l'anàlisi, integrem dades meteorològiques, això ho fem per afegir valors que tinguin trascendencia en el consum de l'aigua, ja que el nombre de turistes no és l'únic que afecta al consum. És per això que hem decidit incloure les temperatures màximes i mínimes diàries i els nivells de precipitació. Les dades utilitzades s'obtenen de la API de la AEMET: https://www.aemet.es/ca/datos_abiertos/AEMET_OpenData

  Aquestes dades es grupen per data per calcular els valors mitjans, aquesta mitjana l'hem de fer ja que la base de dades utilitzada compta amb diferents observatoris des d'on es mesuren les dades, i per tant aquestes varien, però nosaltres preferim una mitjana per temes de simplicitat. A continuació, fusionem aquesta informació amb les dades netejades de consum d’aigua utilitzant la data com a clau. Aquest pas permet enllaçar els patrons meteorològics amb l’ús d’aigua, facilitant l’estudi de la seva influència en les tendències de consum.

  ##### Mesures de temperatura i precipitació
  Les dades meteorològiques que utilitzem són:
  - **Temperatura mínima** (*tmin*): És la temperatura més baixa registrada durant un interval de temps (normalment, un dia).
  - **Temperatura màxima** (*tmax*): És la temperatura més alta registrada durant el mateix interval.
  - **Precipitacions acumulades** (*prec*): La quantitat total de pluja o neu fosa mesurada durant un període mesurada en mm.

  ##### Estacions
  Nosaltres hem decidit utilitzar les tres estacions de Barcelona i després fer la mitjana d'elles per un millor resultat. Si és volgués, es podria fer només amb una. Les estacions són les següents:
  - **Estació 0076 - Barcelona, Fabra**
  - **Estació 0201D - Barcelona, Port Olímpic**
  - **Estació 0201X - Barcelona Drassanes**

  El codi per a l'extracció inicial es pot trobar a: [Extracció inicial de dades AEMET](extracció_dades\extracció_AEMET_inicial.py)


#### Dades del turisme:

  Aquesta base de dades inclou les pernocatacions mensuals a Barcelona i el tipus d'allotjament:Establiments Hotelers, Albergs o Habitatges d'Ús Turístic, però aquests ultims els unificarem tots en un ja que per ara no és una dada relevant.

  Però aquestes dades son mensulas, i nosaltres tenim el consum diari i volem fer una predicció diaria. Per tant, hem de distribuir totes les pernoctacions mensuals entre els diferents dies del mes, però com? Es evident que no tots els dies del mes venen les mateixes persones a Barcelona, els caps de setmana, per exemple, acostument a haver més visitants. La idea que vam tenir per fer la distribució va ser dividir entre dies del mes i afegir soroll (noise) a la distribució. Per tal d'afegir soroll necessitavem un indicador del nombre de turistes diaris, en vam torbar un parell. El primer era un dataset dels vols que arrivaben i marxaven cada dia, però englovaba tota Espanya, pel que vam acabar descartant aquesta via. L'altre indicador que vam trobar va ser un dataset de les transaccions diaries fetes amb targetes de BBVA i transaccions fetes a TPVs de BBVA. Es pot accedir a aquestes dades des de: https://dades.ajuntament.barcelona.cat/consum-privat/index.Rmd.


  Evidentment son dades anonimitzades, però tenen un indicador més que és clau, segmenten entre transaccions fetes per extrangers i espanyols. Concretament hi ha un dataset amb el percentatge de transaccions fetes per estrangers i un altre amb el total de transaccions, de la combinació hem tret el nombre de transaccions fetes per turistes. Hem assumit que un turista espanyol es comporta com un tusista estranger.Així, hem pogut obtenir una distribució per aplicar soroll a les pernoctacions.

  A continuació el codi i els passos seguits per integrar les dades de transaccions turístiques i pernoctacions al conjunt de dades de consum d’aigua per analitzar l’impacte del turisme en l’ús d’aigua. El procés consisteix en:  

  1. **Carregar i netejar les dades**:  
    - Importem els conjunts de dades relacionats amb les transaccions turístiques (`dataset_targetes.csv`), les transaccions totals (`total_transactions.csv`) i les pernoctacions (`pernoctacions_2019_2024.csv`).  
    - Filtrarem les dades per als anys 2021–2023 i formatem les dates de manera consistent.  
    - Calculem una nova columna (`total_tourist_transactions`) que escala les transaccions de turistes estrangers segons el volum total de transaccions.  
  2. **Agrupar dades mensuals**:  
    - Agrupem les transaccions turístiques per mesos per calcular el total de transaccions mensuals.  
    - Distribuïm els totals mensuals entre els dies individuals mitjançant percentatges diaris de transaccions, assegurant una assignació proporcional de les pernoctacions mensuals (`pernoctacions`) a cada dia.  
  3. **Combinar i unificar dades**:  
    - Fusionem les dades de consum d’aigua amb les dades turístiques diàries (`resultado_df`) per integrar l’efecte del turisme a l’anàlisi.  
    - Realitzem agregacions per secció censal, data i altres factors clau per simplificar el conjunt de dades, mantenint mètriques rellevants com el consum total d’aigua i les pernoctacions turístiques.  

  El resultat és un conjunt de dades unificat que vincula el consum d’aigua amb variables meteorològiques i turístiques, permetent una anàlisi exhaustiva de com aquests factors afecten les tendències diàries de consum d’aigua.


## Escalavilitat

#### Dades meteorològiques i precipitacions:

  L'API d'AEMET (Agencia Estatal de Meteorología) permet accedir a dades meteorològiques en temps real o històriques proporcionades per les seves estacions meteorològiques. Per accedir a aquestes dades, cal obtenir una **clau d'API** des del seu portal oficial. Aquesta clau s'inclou en les sol·licituds per autenticar-les.

  ##### Funcionament bàsic
  1. **Autenticació**: Cada sol·licitud a l'API ha d'incloure la clau generada.
  2. **Endponts**: L'API ofereix diferents punts d'accés per a dades com ara:
    - Prediccions meteorològiques.
    - Observacions històriques.
    - Dades puntuals per estació meteorològica.
  3. **Resposta**: Les dades es tornen en format JSON, amb valors com ara temperatures, precipitacions, velocitat del vent, etc.

  Per continuar tenint la informació del temps actualitzada podeu fer servir el següent codi: [Extracció mensual de dades AEMET](extracció_dades\extracció_AEMET.py)
  - Recordeu d'afegir la vostra **API key** proporcionada per **AEMET**.
  - El codi està fet per treure les dades meteorològiques de l'últim mes. Per canviar els dies seleccionats, modifiqueu la secció sota # Calcular les dates per l'últim mes
  - El codi està pensat per treure en format csv les dades necessàries de l'últim mes. Si es volgués, també es podria afegir les noves línies al csv global.

  Per a més informació visiteu: https://opendata.aemet.es/centrodedescargas/inicio

#### Dades del turisme:
