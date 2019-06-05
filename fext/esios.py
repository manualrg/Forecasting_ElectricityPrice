# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 21:11:28 2019

@author: manualrg

Basic funcions to extract data from ESIOS API: www.esios.ree.es
"""
import requests
import json
import pandas as pd


def get_esios_data(token: str,
					indicator: int = 10258,
					start_dt: str = '2018-06-01',
					end_dt: str = '2018-06-02',
					period: str = 'day',
					agg: str = "sum",
					dev=False
				  ):
	
	url = "https://api.esios.ree.es/indicators/"
	aurl = "?start_date={}".format(start_dt)
	b = "T00:00:00&end_date={}T23:59:59".format(end_dt)
	t = "&time_trunc={}".format(period)
	a = "&time_agg=" + agg
	headers = {'content-Type': 'application/json', 'Authorization': 'Token token={}'.format(token)}

	full_url = url+str(indicator)+aurl+b+a+t
	if dev: print(full_url)
	response = requests.get(full_url, headers=headers, stream=True)
	print("Response regarindg indicator: {} status: {}".format(indicator, response.status_code))
	
	data_dict = json.loads(response.content.decode('UTF-8'))
	data_df = pd.DataFrame(data_dict["indicator"]["values"])
	data_df["indicador"] = data_dict["indicator"]['name']
	data_df["idx"] = indicator
	
	return response, data_dict, data_df
	
def get_esios_multi_data(token: str,
                indicators: list = [10258, 1293],
                start_dt: str = '2018-06-01',
                end_dt: str = '2018-06-02',
                period: str = 'day',
                agg: str = 'sum',
                dev=False
              ):
	indicators = list(set(indicators))
	df_list = []
	dict_multidata = {}
	
	for i in indicators:
		_, dict_data, data_df = get_esios_data(token, i, start_dt, end_dt, period, agg, dev)
		df_list.append(data_df)
		dict_multidata.update(dict_data)
		
	return dict_multidata, pd.concat(df_list,axis=0)
	
def get_esios_hourly_data(token: str,
					indicator: int = 600,
					start_dt: str = '2018-06-03',
					end_dt: str = '2018-06-03',
					period: str = 'hour',
					dev=False
				  ):
	
	url = "https://api.esios.ree.es/indicators/"
	aurl = "?start_date={}".format(start_dt)
	b = "T00:00:00&end_date={}T23:59:59".format(end_dt)
	t = "&time_trunc={}".format(period)
	headers = {'content-Type': 'application/json', 'Authorization': 'Token token={}'.format(TOKEN)}

	Miurl = url+str(indicator)+aurl+b+t
	if dev: print(Miurl)
	response = requests.get(Miurl, headers=headers, stream=True)
	print("Response regarindg indicator: {} status: {}".format(indicator, response.status_code))
	
	data_dict = json.loads(response.content.decode('UTF-8'))
	data_df = pd.DataFrame(data_dict["indicator"]["values"])
	data_df["indicador"] = data_dict["indicator"]['name']
	data_df["idx"] = indicator
	
	return response, data_dict, data_df
	