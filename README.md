### Membres del grup

|Name | Email | Role |
| --- | --- | --- |
| Ivan Hernández | ivan.hernandez04@estudiant.upf.edu | Technical Responsible |
| Bruno Manzano | bruno.manzano01@estudiant.upf.edu | Audiovisual Responsible |
| Paula Mateos | paula.mateos01@estudiant.upf.edu | Project Manager |
| Martí Oms | marti.oms01@estudiant.upf.edu | Creative Responsible |
| Yuyan Wang | yuyan.wang01@estudiant.upf.edu | Implementation Responsible |


### Com executar el codi

Això s'ha demostrat que funciona a MacOS.

0. L'enfocament recomanat seria crear un entorn virtual Python3 i activar-lo; no obstant això, no és estrictament necessari. Pots passar al següent pas si no vols utilitzar un entorn virtual.

    ```
    $ python -m venv <nomVenv>
    $ source <elTeuCamíPerActivarVenv:perExemple.nomVenv/bin/activate>
    ```

1. Instal·la els paquets necessaris. Proporcionem el fitxer `requirements.txt`.

    ```
    $ pip install -r requirements.txt
    ```

2. Utilitza el Python3 corresponent com a *Jupyter Notebook Kernel*.

3. Asseguret que la teva carpeta de dades segueixi aquesta estructura (crea la carpeta local_data). La resta de carpetes deixe-les com estan.

    ```
    data/
    ├── census_geo.geojson
    ├── dataset_targetes.csv
    ├── pernoctacons_2019_2024.csv
    ├── population_barcelona_districts.csv
    ├── prothet_performance.png
    ├── temperature_precipitation.csv
    ├── total_transacions.csv
    ├── WBS.png
    └── local_data/  # Aquesta carpeta no estarà present a la carpeta/repositori donat per problemes de mida, si us plau assegura't de crear-la i afegir-hi el fitxer *daily_dataset.csv* d'AGBAR.
        └── daily_dataset.csv

    ```

4. Ja ho tens tot preparat per executar Final_Notebook_dropbydrop.ipynb, on trobaras el nostre treball complet així com explicacions i acces a la simulació.

### Com executar directament a Jupyter

Amb el següent comand s'obrirà una pestanya de Jupyter al motor de cerca per defecte.
```
    $ jupyter-lab&
```

### Hi ha dues opcions per executar el codi:
 #### 1- Executar la final notebook
- Afegir una carpeta dins de **data**, amb el nom de **local_data** i afegir-hi **daily_dataset.csv**
- Executar la llibreta [**Final_Notebook_dropbydrop.ipynb**](Final_Notebook_dropbydrop.ipynb.py)
 #### 2- Executar utilitzant els .py:
  ##### 2.1 - Executar data_processing.py:
   - Obtenir les dades amb les quals correr el progama.
   - Per informació més detallada visita: [obtenir_dades](extracció_dades/README.md#3-Obtenir-dades-inicials)
  ##### 2.2 - Executar l'applicació:
   - Per executar l'applicació, executa el comando següent:
   ```
   streamlit run main.py
   ```
   Per informació més detallada vista: Per informació més detallada visita: [executar l'aplicació](display/README.md#com-executar-la-simulació-streamlit-des-de-la-terminal)




Aquí tens el resum actualitzat amb el model i les recomanacions afegides:

---

## 1. Introduction

### Project Proposal

**Aigües Barcelona Data Challenge**

El projecte aborda l’augment de la demanda d’aigua a causa del turisme massiu a Barcelona, amb un enfocament especial en el sector comercial. L’increment del nombre de turistes—8,27 milions el 2023, en contrast amb els 1,62 milions de residents de la ciutat—imposa una càrrega significativa sobre els recursos hídrics de la ciutat, i podria arribar a representar fins al 15,68% del consum diari d’aigua.

Davant d’aquesta pressió, especialment durant les temporades turístiques altes, quan la població de la ciutat gairebé es duplica, aquest projecte pretén analitzar la petjada hídrica vinculada al turisme. Mitjançant l’ús de dades històriques i variables externes, l’equip desenvoluparà un model predictiu capaç de preveure les fluctuacions de la demanda d’aigua. Els resultats proporcionaran recomanacions pràctiques per a AGBAR per optimitzar la gestió de l’aigua, assegurant que Barcelona pugui satisfer de manera sostenible les necessitats tant dels residents com dels turistes.

Aquesta col·laboració amb AGBAR s’alinea amb el nostre objectiu d’aplicar habilitats de ciència de dades i enginyeria a reptes del món real, especialment en la gestió de recursos urbans crítics com l’aigua. Els resultats d’aquest projecte contribuiran a la sostenibilitat i resiliència a llarg termini de la ciutat davant l’increment del turisme.

Els lliurables relacionats amb aquest projecte es defineixen en la següent imatge:

![Work Breakdown Structure](./data/WBS.png)

## 2. Data Processing:

El projecte parteix del dataset **daily_dataset.csv** proporcionat per AGBAR, que inclou dades detallades sobre el consum d’aigua a nivell diari i per secció censal. Aquest dataset constitueix la base principal del nostre model.

Aquestes dades són indispensables per entendre la variabilitat del consum en funció de la geografia i del tipus d’ús. Tanmateix, per desenvolupar un model que integri els efectes del turisme i d’altres factors externs, necessitem ampliar aquesta informació amb noves fonts de dades:

1. #### Dades meteorològiques:  
   - Temperatura màxima i mínima diària
   - Precipitacions acumulades (mm)

   Aquestes dades són crucials per ajustar el model als patrons estacionals i climàtics, que tenen un gran impacte en el consum d’aigua.  

2. **Dades de turisme**:  
   - Pernoctacions diàries

3. **Habitants de Barcelona**:  
   - Habitants per districte

   El turisme és un dels factors principals que volem analitzar. Per això, aquestes dades són essencials per segmentar el consum d’aigua atribuïble als visitants, diferenciant-lo del consum residencial o d'altres usos.  

La integració d’aquestes dades ens permetrà desenvolupar un model predictiu que connecti el consum d’aigua amb variables climàtiques i turístiques, oferint prediccions més precises i útils per a la gestió sostenible dels recursos hídrics. Així, podrem respondre preguntes clau, com l’impacte específic del turisme en zones determinades o l’efecte de condicions meteorològiques extremes en el consum global.

Per més informació sobre la extracció de dades: [extracció_dades](/extracció_dades)

## 3. Model

El model desenvolupat es basa en tècniques d'aprenentatge automàtic per predir el consum d'aigua en funció de diverses variables com el turisme, les condicions meteorològiques i la població. Utilitzant mètodes com la regressió i els arbres de decisió, el model és capaç de captar patrons complexos en les dades i proporcionar prediccions precises per a la gestió de l’aigua a Barcelona. Això permet preveure les fluctuacions de demanda en diferents àrees de la ciutat i ajustar les estratègies de distribució d’aigua de manera eficient.

A més, el model ofereix la flexibilitat d’adaptar-se a noves variables i de millorar les seves prediccions amb el temps a mesura que es disposa de més dades. Aquest enfocament dinàmic farà possible una gestió hídrica més adaptativa i sostenible.

## 4. Simulació

La simulació facilita la projecció d’escenaris futurs per anticipar pics de demanda o escassetat, optimitzant els recursos de manera proactiva. Combinant aquestes capacitats amb un estudi estàtic, AGBAR pot identificar patrons a llarg termini i justificar decisions estratègiques basades en dades fiables. Aquesta metodologia dinàmica i estratègica garanteix una gestió hídrica eficient i sostenible.

Per més informació: [Simulació](/display)

## 5. Altres

### Escalabilitat del projecte

Poder continuar utilitzant el projecte un cop acabat el challenge és un dels grans aspectes a integrar.  
- Per veure l'escalabilitat de les dades utilitzades: [escalabilitat de les dades](/extracció_dades/README.md#2-Escalabilitat)
- Per veure l'escalabilitat del model: [escalabilitat del model](/models/README.md)

### Recomanacions

Basat en els resultats obtinguts, es recomana a AGBAR adoptar un enfocament de gestió hídrica flexible que integri tant el turisme com les condicions climàtiques a la seva estratègia a llarg termini. Això inclou ajustar les previsions de consum d’aigua en funció de l’evolució de la demanda turística i implementar tecnologies de monitoratge en temps real per millorar la resposta davant possibles pics de consum. A més, es suggereix col·laborar amb les autoritats locals per establir polítiques de consum d’aigua més sostenibles per als turistes i la població.


**Control Information**
* Version: 1.1
* Date of Issue: 19 November 2024
* Responsible Party: Yuyan Wang (Implementation Responsible)
* Approval Status: Internal Use Only
* Access Permissions: Restricted to Project Core Team T101.A and approved collaborators

**Data sources**
 - gencat_turism: Generalitat de Catalunya.
   https://empresa.gencat.cat/ca/treb_ambits_actuacio/turisme/coneixement_planificacio/estadistiques-turistiques/index.html
   https://empresa.gencat.cat/web/.content/001-departament/04-serveis/04_estudis_estadistica/Turisme/Demanda-turistica/Turisme-estranger-Frontur/evolucio_frontur.xlsx
 - temperature_precipitation: API de AEMET.
   https://www.aemet.es/ca/portada
 - tourism_flux: Eurocontrol
   https://www.eurocontrol.int/Economics
 - https://github.com/martgnz/bcn-geodata/blob/master/seccio-censal/seccio-censal.geojson
 - Oficina Municipal de Dades: Ajuntament de Barcelona.
   https://dades.ajuntament.barcelona.cat/consum-privat/index.Rmd



### Descàrrec de responsabilitat

Aquest document i tot el contingut que conté són propietat del **Project Core Team T101.A** i estan destinats exclusivament a l'ús d'individus autoritzats dins del projecte. La distribució, còpia o ús no autoritzat d’aquest document, total o parcial, està prohibit sense el consentiment explícit del **Project Core Team T101.A**.