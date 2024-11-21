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

Aigües Barcelona Data Challenge 

The project “Anàlisi de la petjada hídrica dels turistes a Barcelona” aims to meticulously analyse the water footprint of tourists in Barcelona.

The project addresses the increasing demand for water due to mass tourism in Barcelona, with a focus on the commercial sector. The growing number of tourists—8.27 million in 2023, in contrast to the city’s 1.62 million residents—places a significant burden on the city's water resources, potentially accounting for up to 15.68% of the daily water consumption.

Given this pressure, especially during peak tourist seasons when the city's population nearly doubles, this project seeks to analyse the water footprint linked to tourism. By leveraging historical data and external variables, the team will develop a predictive model capable of forecasting water demand fluctuations. The results will provide actionable insights and recommendations for AGBAR to optimise water management, ensuring that Barcelona can sustainably meet the needs of both residents and tourists.

This collaboration with AGBAR aligns with our goal of applying data science and engineering skills to real-world challenges, particularly in managing critical urban resources like water. The outcomes of this project will contribute to the city's long-term sustainability and resilience in the face of growing tourism.

The deliverables related with this project is defined in this following image:

![Work Breakdown Structure](./data/WBS.png)

## 2. Data Processing:

The project is based on the **daily_dataset.csv** dataset provided by AGBAR, which includes detailed data on daily water consumption at the census section level. This dataset serves as the primary foundation for our model and contains the following fields:  

- **Census section, district, and municipality**: to identify specific geographical areas of consumption.  
- **Date**: to analyze the temporal distribution of water consumption.  
- **Usage**: specifying whether the water is used for domestic, industrial, commercial, or other purposes.  
- **Number of meters**: indicating how many devices record consumption in each section.  
- **Accumulated consumption (L/day)**: the volume of water consumed daily in liters.  

These data are essential to understanding consumption variability based on geography and type of usage. However, to develop a model that integrates the effects of tourism and other external factors, we need to enrich this information with additional data sources:  

1. **Weather data**:  
   - **Daily maximum and minimum temperatures**: Climate directly influences water consumption. For example, on extremely hot days, consumption increases, especially in tourist areas with outdoor activities.  
   - **Accumulated precipitation**: Rainy days reduce water usage in outdoor activities such as irrigation or showers at beaches and pools.  

   These data are crucial for adjusting the model to seasonal and climatic patterns, which significantly impact water consumption.  

2. **Tourism data**:  
   - **Daily overnight stays**: We need to know how many tourists stay in the city each day. This information reflects the impact of tourism in specific areas and helps identify how visitor flows contribute to water usage in services such as hotels, restaurants, and recreational activities.  

   Tourism is one of the main factors we aim to analyze. Therefore, this data is essential for segmenting water consumption attributable to visitors, distinguishing it from residential or other uses.  

Integrating these data sources will allow us to develop a predictive model that links water consumption to climatic and tourism variables, providing more precise and useful predictions for sustainable water resource management. This will enable us to answer key questions, such as the specific impact of tourism in certain areas or the effect of extreme weather conditions on overall consumption.  

For more information go to: [extracció_dades](/extracció_dades)

## 3. Model
  # TO DO


## 4. Simulació
 # TO DO
 Per més informació: [Simulació](/display)


## 5. Altres


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
