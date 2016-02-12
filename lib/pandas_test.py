# -*- coding: utf-8 -*-
import os, pandas
			
the_data = (os.path.dirname(os.path.realpath(__file__)) + 
	'/dataframe.csv')
the_score = pandas.read_csv(
	the_data, 
	header=0,
	names=['soprano','alto','tenor','bass'], 
	index_col=0,
	encoding='utf-8')

print the_score.head(10)