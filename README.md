# ProjectManagement

## Project Core Team T101.A (alphabetical order)

|Name | Email | Role |
| --- | --- | --- |
| Ivan Hernández | ivan.hernandez04@estudiant.upf.edu | Technical Responsible |
| Bruno Manzano | bruno.manzano01@estudiant.upf.edu | Audiovisual Responsible |
| Paula Mateos | paula.mateos01@estudiant.upf.edu | Project Manager |
| Martí Oms | marti.oms01@estudiant.upf.edu | Creative Responsible |
| Yuyan Wang | yuyan.wang01@estudiant.upf.edu | Implementation Responsible |

## Disclaimer

This document and all content within are proprietary to Project Core Team T101.A and are intended solely for the use of authorized individuals within the project. Unauthorized sharing, copying, or use of this document, in whole or in part, is prohibited without explicit consent from the Project Core Team T101.A.

**Control Information**
* Version: 1.0
* Date of Issue: 5 November 2024
* Responsible Party: Yuyan Wang (Implementation Responsible)
* Approval Status: Internal Use Only
* Access Permissions: Restricted to Project Core Team T101.A and approved collaborators

## Project Proposal

Aigües Barcelona Data Challenge 

The project “Anàlisi de la petjada hídrica dels turistes a Barcelona” aims to meticulously analyse the water footprint of tourists in Barcelona.

The project addresses the increasing demand for water due to mass tourism in Barcelona, with a focus on the commercial sector. The growing number of tourists—8.27 million in 2023, in contrast to the city’s 1.62 million residents—places a significant burden on the city's water resources, potentially accounting for up to 15.68% of the daily water consumption.

Given this pressure, especially during peak tourist seasons when the city's population nearly doubles, this project seeks to analyse the water footprint linked to tourism. By leveraging historical data and external variables, the team will develop a predictive model capable of forecasting water demand fluctuations. The results will provide actionable insights and recommendations for AGBAR to optimise water management, ensuring that Barcelona can sustainably meet the needs of both residents and tourists.

This collaboration with AGBAR aligns with our goal of applying data science and engineering skills to real-world challenges, particularly in managing critical urban resources like water. The outcomes of this project will contribute to the city's long-term sustainability and resilience in the face of growing tourism.

The deliverables related with this project is defined in this following image:

![Work Breakdown Structure](./data/WBS.png)

## Data sources
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


## Structure of the data folder

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

## How to Run the Notebooks

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
