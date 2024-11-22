# ProjectManagement

### Project Core Team T101.A (alphabetical order)

|Name | Email | Role |
| --- | --- | --- |
| Ivan Hernández | ivan.hernandez04@estudiant.upf.edu | Technical Responsible |
| Bruno Manzano | bruno.manzano01@estudiant.upf.edu | Audiovisual Responsible |
| Paula Mateos | paula.mateos01@estudiant.upf.edu | Project Manager |
| Martí Oms | marti.oms01@estudiant.upf.edu | Creative Responsible |
| Yuyan Wang | yuyan.wang01@estudiant.upf.edu | Implementation Responsible |

### Disclaimer

This document and all content within are proprietary to Project Core Team T101.A and are intended solely for the use of authorized individuals within the project. Unauthorized sharing, copying, or use of this document, in whole or in part, is prohibited without explicit consent from the Project Core Team T101.A.

### How to Run the Notebooks

# AFEGIR LES DUES OPCIONS DE COM CORRER EL CODI (PER WINDOWS, LINUX I MACOS): 
 ## 1- DEMO NOTEBOOK AMB TOT.
 ## 2- .PY AMB EL CODI BEN ESTRUCTURAT (QUAN ESTIGUI FET)

This has been proven to be working on MacOS.

0. The recommended approach would be to create a Python3 virtual environment and activate it; however it is not essentially needed. Skip to next step if you don't want to use a venv.

    ```
    $ python -m venv <nameVenv>
    $ source <youPathToVenvActivate:e.g.nameVenv/bin/activate>
    ```

1. Install the necessary packages. We are providing the requirements.txt file.

    ```
    $ pip install -r requirements.txt
    ```

2. Use the corresponding Python3 as the Jupyter Notebook Kernel.
3. And you would be ready to go :)

### How to run the report on jupyter directlly

With the following command a jupyter tab will open on the default search engine.

```
    $ jupyter-lab&
```


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

   El turisme és un dels factors principals que volem analitzar. Per això, aquestes dades són essencials per segmentar el consum d’aigua atribuïble als visitants, diferenciant-lo del consum residencial o d'altres usos.  

La integració d’aquestes dades ens permetrà desenvolupar un model predictiu que connecti el consum d’aigua amb variables climàtiques i turístiques, oferint prediccions més precises i útils per a la gestió sostenible dels recursos hídrics. Així, podrem respondre preguntes clau, com l’impacte específic del turisme en zones determinades o l’efecte de condicions meteorològiques extremes en el consum global.   

Per més informació sobre la extracció de dades: [extracció_dades](/extracció_dades)

## 3. Model
  # TO DO


## 4. Simulació
 # TO DO
 Per més informació: [Simulació](/display)


## 5. Altres

### Escalabilitat del projecte
 Poder continuar utilitzant el project un cop acabat el challenge és un dels grans aspectes a integrar. 
 - Per veure l'escalabiltat de les dades utilitzades: [escalabilitat de les dades](/extracció_dades/README.md#2-Escalabilitat)
 - Per veure l'escalabilitat del model: [escalabilitat del model](/models/README.md)


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


### Structure of the data folder

We assume that the data folder looks like:

```
data/
├── census_geo.geojson
├── districts_geo.geojson
├── gencat_turism.xlsx
├── pernoctacons_2019_2024.csv
├── temperature_precipitation.csv
├── tourism_flux.csv
├── tourism_temp_bcn.csv
├── targetes_preprocessed.csv  # generated after running targetes.ipynb or downloading from git
├── dataset_targetes.csv
├── total_transacions.csv
└── local_data/  # this folder will not be in the repo for sizing issues
    ├── daily_dataset.csv
    └── old/
        ├── dades_datachallenge.csv
        ├── daily_dataset_economic_activity.csv
    └── merged_cleaned_data.csv  # generated after running data_processing.ipynb
```
