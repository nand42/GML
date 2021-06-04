from datetime import time
import matplotlib
from matplotlib.colors import Colormap
import pandas as pd
import matplotlib.pyplot as plt
from ast import literal_eval
from pandas.plotting import radviz
import numpy as np
import plotly.graph_objects as go
import os 


class Ester:
    def __init__(self):
        # tester checks
        self._verbose = False
        self._test_import_data = False
        self._test_session_name = False
        self._test_create_dataframe = False
        self._test_setup_dataframe = False
        # startup
        self.clear_screen()
        self.session_name = self.ask_session_name()
        self.datapath = self.ask_for_input_file()

    def clear_screen(self):
        lambda : os.system('clear')

    def import_data(self):
        # store the data
        data = list()
        # store the broken rows
        broken_row = list()
        # read in the file
        with open(self.datapath, 'r', encoding='utf-8') as f:
            # read the rows
            rows = f.readlines()
            for row in rows:
                # try to convert a row from a string to dict
                try:
                    row = literal_eval(row)
                    data.append(row)
                except SyntaxError:
                    broken_row.append(row)
                    continue
        self.rdata = data
        self._test_import_data = True
        if self._verbose:
            print('[done] import_data')
        return self.rdata
    
    def ask_for_input_file(self):
        self.datapath = input('Enter input file path: ')
        return self.datapath

    def ask_session_name(self):
        self.session_name = input('Enter the session name: ')
        self._test_session_name = True
        return self.session_name

    def create_dataframe(self):
        # checks if data source has been imported
        if self._test_import_data == False :
            self.import_data()
        
        # convert data to a dataframe
        self._rawdf = pd.DataFrame(self.rdata, columns=['time', 'longitude', 'latitude', 'altitude', 'name'])
        # set test value True
        self._test_create_dataframe = True
        if self._verbose:
            print('[done] create_dataframe')
        return self._rawdf
        
    def setup_dataframe(self):
        # checks if the dataframe has been created
        if self._test_create_dataframe == False :
            self.create_dataframe()
        df = self._rawdf
        #remove duplicate row
        df = pd.DataFrame.drop_duplicates(self._rawdf, keep='first')
        # convert coordinates x,y (longitude,latitude) data in float64 with e-5 precision
        df['longitude'] = df['longitude'].apply(lambda x : round(float(x.replace('.', '.')),5))
        df['latitude'] = df['latitude'].apply(lambda x : round(float(x.replace('.', '.')),5))
        # convert altitude in float64 with e-2 precision
        df['altitude'] = df['altitude'].apply(lambda x : round(float(x.replace(',', '.')),2))
        # write new datafram on class
        self.dataframe = df
        # set test value True
        self._test_setup_dataframe = True
        if self._verbose:
            print('[done] setup_dataframe')

    def get_dataframe(self):
        # checks if the dataframe has been created
        if self._test_setup_dataframe == False :
            self.setup_dataframe()
        if self._verbose:
            print('[done] get_dataframe')
        return self.dataframe
    
    def generate_map(self):
        # test session name (should already has one)
        if self._test_session_name == False:
            self.ask_session_name()
        # ask for the name, answere NO by default
        ask = input('Do you need a specific name for the plot? (y/N)')
        if ask == 'y':
            sname = input('Enter the name: ')
            name_img = 'GML_map_'+ str(self.session_name) + '_' + str(sname) +'.pdf'
        else:
            name_img = 'GML_map_'+ str(self.session_name) +'.pdf'
        # get the dataframe
        df = self.get_dataframe()
        # generate the plot 
        plt.scatter(x=df['longitude'], y=df['latitude'], c=df['altitude'], cmap='viridis')
        plt.ticklabel_format(useOffset=False)
        plt.colorbar()
        # save pdf image
        plt.savefig(name_img)
        # show pdf image 
        plt.show()
        if self._verbose:
            print('[done] generate_map')

