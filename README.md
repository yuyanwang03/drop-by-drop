# ProjectManagement

## Project Core Team T101.A (alphabetical order)

|Name | Email | Role |
| --- | --- | --- |
| Ivan Hernández | ivan.hernandez04@estudiant.upf.edu |  |
| Bruno Manzano | bruno.manzano01@estudiant.upf.edu | |
| Paula Mateos | paula.mateos01@estudiant.upf.edu | Project Manager |
| Martí Oms | marti.oms01@estudiant.upf.edu | |
| Yuyan Wang | yuyan.wang01@estudiant.upf.edu | |

## Project Proposal

Aigües Barcelona Data Challenge 

## Structure of the data folder

We assume that the data folder looks like:

```
> data 
	census_geo.geojson
	districts_geo.geojson
	gencat_turism.xlsx
	temperature_precipitation.csv
  pernoctacons_2019_2024.csv
  tourism_flux.csv
	tourism_temp_bcn.csv
    > local_data (this folder will not be in the repo for sizing issues)
        > old
            dades_datachallenge.csv
            daily_dataset_economic_activity.csv
            daily_dataset.csv
        daily_dataset_economic_activity.csv
        daily_dataset.csv
        hours_lecture.parquet
        merged_data.csv (generated after running the data_processing_merge.ipynb)
      
    
```
## Data sources
 - gencat_turism: Generalitat de Catalunya.
   https://empresa.gencat.cat/ca/treb_ambits_actuacio/turisme/coneixement_planificacio/estadistiques-turistiques/index.html
   https://empresa.gencat.cat/web/.content/001-departament/04-serveis/04_estudis_estadistica/Turisme/Demanda-turistica/Turisme-estranger-Frontur/evolucio_frontur.xlsx
 - temperature_precipitation: API de AEMET.
   https://www.aemet.es/ca/portada
 - tourism_flux: Eurocontrol
   https://www.eurocontrol.int/Economics
 - https://github.com/martgnz/bcn-geodata/blob/master/seccio-censal/seccio-censal.geojson
