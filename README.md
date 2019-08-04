# Forecasting electricity daily SPOT market price in Spain

## Description
This repository is a Data Science project which main goal is to build a Machine Learning model to forecast electricity spot market daily price.
The framework contains every step in a DS project, from data ingestion, to visualization and analysis, and finally training and evaluation a ML model. 

## Index
1. Import data from external APIs
	01_importData_quandl
	02_importData_ESIOS
2. EDA (Exploratoy Data Analysis) and Feature Engineering
	03_EDA_FeatEng
3. Model Building and evaluation

## Technology

Python 3.6

Libraries in main distributions, such as Anaconda:
* pandas (0.23.4)
* numpy (1.15.4)
* scikit-learn (0.20.1)
* scipy (1.1.0)
* matplotlib (3.0.2)
* seaborn (0.9.0)

Install libraries with pip:
* https://docs.quandl.com/docs/python-installation ```pip install quandl```
* https://xgboost.readthedocs.io/en/latest/build.html# ```pip install xgboost``` 
* https://pypi.org/project/requests/ ```pip install requests```
* https://docs.python.org/3/library/json.html ```pip install json```

## Import Data
Electricity market data (REE ESIOS API):
https://www.esios.ree.es/en
* Daily price is set at daily auctions in a pool market. This market is said to be marginal, because there is a matching bid that sets current day price. 
* P48 generation by technology: It is also called PHO (Programa Horario Operativo) and it is the definitive schedulled generation program

REE is the TSO (Transmission System Operator) in Spain, it is a public enterprise which owns, builds and operates high voltage transmission lines. Moreover, at a system operation level, it is responsible of running several auctions and adjustment mechanisms. Regarding SPOT market (run by OMIE), REE delivers data though its website ESIOS. OMIE is responsible of running several auctions, such as spot and intraday.


Financial data (Quandl API):
https://www.quandl.com/
* EUA (European Emission Allowances, CO2): Important when marginal generator is a coal or natural gas utility
* Coal API2: There are many kinds of coal (antracite, lignite, etc.), so finantial analysis firms deviced this index arranging European data
* Natural Gas TTF: It stands for Title Transfer Facility, it is a Virtual Trading point in the Netherlands, and also a price reference in European HG markets (like Henry Hub or NBP)

## EDA (Exploratory Data Analysis) and Feature Engineering
Analyze time series data, explore the main drivers of spot price and how they interact and finally, compute new features.

## Model Building
Train several model like linear regression, random forest and XGBs, tunning hyperparamenters with cross-validation and grid search. After selecting the best one, a residual analysis is carreid out
