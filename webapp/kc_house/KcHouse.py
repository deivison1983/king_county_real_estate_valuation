import pickle
import inflection
import pandas as pd
import numpy as np
import math
import datetime


class KcHouse( object ):
    
    def __init__( self ):
        self.home_path = ''
        self.bedrooms_scaler      = pickle.load( open( self.home_path + 'parameters/bedrooms_scaler.pkl','rb' ) )
        self.bathrooms_scaler     = pickle.load( open( self.home_path + 'parameters/bathrooms_scaler.pkl','rb' ) )
        self.floors_scaler        = pickle.load( open( self.home_path + 'parameters/floors_scaler.pkl','rb' ) )
        self.yr_built_scaler      = pickle.load( open( self.home_path + 'parameters/yr_built_scaler.pkl','rb' ) )
        self.year_scaler          = pickle.load( open( self.home_path + 'parameters/year_scaler.pkl','rb' ) )
        self.lat_scaler           = pickle.load( open( self.home_path + 'parameters/lat_scaler.pkl','rb' ) )
        self.long_scaler          = pickle.load( open( self.home_path + 'parameters/long_scaler.pkl','rb' ) )
        self.sqft_living_scaler   = pickle.load( open( self.home_path + 'parameters/sqft_living_scaler.pkl','rb' ) )
        self.sqft_lot_scaler      = pickle.load( open( self.home_path + 'parameters/sqft_lot_scaler.pkl','rb' ) )
        self.sqft_above_scaler    = pickle.load( open( self.home_path + 'parameters/sqft_above_scaler.pkl','rb' ) )
        self.sqft_basement_scaler = pickle.load( open( self.home_path + 'parameters/sqft_basement_scaler.pkl','rb' ) )
        self.yr_renovated_scaler  = pickle.load( open( self.home_path + 'parameters/yr_renovated_scaler.pkl','rb' ) )
        self.sqft_living15_scaler = pickle.load( open( self.home_path + 'parameters/sqft_living15_scaler.pkl','rb' ) )
        self.sqft_lot15_scaler    = pickle.load( open( self.home_path + 'parameters/sqft_lot15_scaler.pkl','rb' ) )
        self.season_scaler        = pickle.load( open( self.home_path + 'parameters/season_scaler.pkl','rb' ) )
        self.zipcode_scaler       = pickle.load( open( self.home_path + 'parameters/zipcode_scaler.pkl','rb' ) )
        
        
    def data_cleaning( self, df1 ):
        
           
        ## 1.3 Data Type

        # Convert data in datetime variable
        df1['date'] = pd.to_datetime(df1['date'])
        
        return df1

    def featuring_engineering( self, df2 ): 
        
        ## 2.4 Feature Engineering
        
        #basement
        df2['basement'] = df2.apply(lambda x: 0 if ( x['sqft_basement'] == 0)  else 1, axis =1 ).astype(int)
        
        # price_sqft
        #df2['price_sqft'] = df2.apply( lambda x: x['price'] / x['sqft_living'], axis = 1 )   

        #year
        df2['year'] = df2['date'].dt.year.astype(str)
        
        #month
        df2['month'] = df2['date'].dt.month
        
        #day
        df2['day'] = df2['date'].dt.day
        
        #season of year
        df2['season'] = df2.apply( lambda x: 'spring' if x['date'] in pd.date_range( start = x['year'] + '/3/21' , end= x['year'] + '/6/20'  , freq='D' ) else
                                             'summer' if x['date'] in pd.date_range( start = x['year'] + '/6/21' , end= x['year'] + '/9/20'  , freq='D' ) else
                                             'fall'   if x['date'] in pd.date_range( start = x['year'] + '/9/21' , end= x['year'] + '/12/20' , freq='D' ) else 
                                             'winter', axis = 1 )
        
        #sqft_living compare
        df2['sqft_living_compare'] = df2.apply( lambda x: 1 if x['sqft_living'] > x['sqft_living15'] else 0, axis = 1 )
        
        #sqft_lot compare
        df2['sqft_lot_compare']    = df2.apply( lambda x: 1 if x['sqft_lot'] > x['sqft_lot15'] else 0, axis = 1 )
        
        #city
        dic_zip = {'98001': 'Auburn','98002': 'Auburn','98003': 'Federal Way','98004': 'Bellevue',
           '98005': 'Bellevue','98006': 'Bellevue','98007': 'Bellevue','98008': 'Bellevue',
           '98009': 'Bellevue','98010': 'Black Diamond','98011': 'Bothell','98013': 'Burton',
           '98014': 'Carnation','98015': 'Bellevue','98019': 'Duvall','98022': 'Enumclaw',
           '98023': 'Federal Way','98024': 'Fall City','98025': 'Hobart','98027': 'Issaquah',
           '98028': 'Kenmore','98029': 'Issaquah','98030': 'Kent','98031': 'Kent','98032': 'Kent',
           '98033': 'Kirkland','98034': 'Kirkland','98035': 'Kent','98038': 'Maple Valley',
           '98039': 'Medina','98040': 'Mercer Island','98041': 'Bothell','98042': 'Kent',
           '98045': 'North Bend','98047': 'Pacific','98050': 'Preston','98051': 'Ravensdale',
           '98052': 'Redmond','98053': 'Redmond','98055': 'Renton','98056': 'Renton',
           '98057': 'Renton','98058': 'Renton','98059': 'Renton','98062': 'Seahurst',
           '98063': 'Federal Way','98064': 'Kent','98065': 'Snoqualmie','98070': 'Vashon',
           '98071': 'Auburn','98072': 'Woodinville','98073': 'Redmond','98074': 'Sammamish',
           '98075': 'Sammamish','98077': 'Woodinville','98083': 'Kirkland','98089': 'Kent',
           '98092': 'Auburn','98093': 'Federal Way','98101': 'Seattle','98102': 'Seattle',
           '98103': 'Seattle','98104': 'Seattle','98105': 'Seattle','98106': 'Seattle','98107': 'Seattle',
           '98108': 'Seattle','98109': 'Seattle','98111': 'Seattle','98112': 'Seattle','98113': 'Seattle',
           '98114': 'Seattle','98115': 'Seattle','98116': 'Seattle','98117': 'Seattle','98118': 'Seattle',
           '98119': 'Seattle','98121': 'Seattle','98122': 'Seattle','98124': 'Seattle','98125': 'Seattle',
           '98126': 'Seattle','98127': 'Seattle','98129': 'Seattle','98131': 'Seattle','98133': 'Seattle',
           '98134': 'Seattle','98136': 'Seattle','98138': 'Seattle','98139': 'Seattle','98141': 'Seattle',
           '98144': 'Seattle','98145': 'Seattle','98146': 'Seattle','98148': 'Seattle','98154': 'Seattle',
           '98155': 'Seattle','98158': 'Seattle','98160': 'Seattle','98161': 'Seattle','98164': 'Seattle',
           '98165': 'Seattle','98166': 'Seattle','98168': 'Seattle','98170': 'Seattle','98174': 'Seattle',
           '98175': 'Seattle','98177': 'Seattle','98178': 'Seattle','98181': 'Seattle','98185': 'Seattle',
           '98188': 'Seattle','98190': 'Seattle','98191': 'Seattle','98194': 'Seattle','98195': 'Seattle',
           '98198': 'Seattle','98199': 'Seattle','98224': 'Baring','98288': 'Skykomish'}
        
        df2['zipcode'] = df2['zipcode'].astype(str)
        df2['city'] = df2['zipcode'].map(dic_zip)
        df2['city'] = df2['city'].apply( lambda x: inflection.underscore(x).replace(' ', '_') )
        
        #road
        df2['road'].fillna('not_available', inplace = True )
        
        #avenue
        df2['avenue'] = df2['road'].str.contains('Avenue', regex = False)
        df2['avenue'] = df2['avenue'].apply( lambda x: 1 if (x==True) else 0 ).astype(int)
        
#         aux2 = df2[['id','city','avenue']]
#         df2 = pd.merge(df2,aux2, left_index = True, right_index = True )
#         cols_old = ['id_y']
#         df2 = df2.drop( cols_old, axis = 1)
#         df2.columns = ['id', 'date', 'price', 'bedrooms', 'bathrooms', 'sqft_living','sqft_lot', 'floors','waterfront',
#                        'view', 'condition', 'grade', 'sqft_above', 'sqft_basement', 'yr_built','yr_renovated',
#                        'zipcode', 'lat', 'long', 'sqft_living15', 'sqft_lot15', 'basement','price_sqft', 'year',
#                        'month', 'day','season', 'sqft_living_compare', 'sqft_lot_compare','city', 'avenue']
        
        
        
        # 3.0 FILTRAGEM DE VARIAVEIS

        ## 3.1 Filtragem de linhas

        df2 = df2[ df2['bedrooms'] < 33 ]

        return df2

    def data_preparation( self, df5 ):

        ## 5.1.2 Rescaling
        
        # min-max
        df5['bedrooms']      = self.bedrooms_scaler.transform(      df5[['bedrooms']].values )
        df5['bathrooms']     = self.bathrooms_scaler.transform(     df5[['bathrooms']].values )
        df5['floors']        = self.floors_scaler.transform(        df5[['floors']].values )
        df5['yr_built']      = self.yr_built_scaler.transform(      df5[['yr_built']].values)
        df5['year']          = self.year_scaler.transform(          df5[['year']].values )
        df5['lat']           = self.lat_scaler.transform(           df5[['lat']].values )
        df5['long']          = self.long_scaler.transform(          df5[['long']].values )
        
        ## Robust 
        df5['sqft_living']   = self.sqft_living_scaler.transform(   df5[['sqft_living']].values )
        df5['sqft_lot']      = self.sqft_lot_scaler.transform(      df5[['sqft_lot']].values )
        df5['sqft_above']    = self.sqft_above_scaler.transform(    df5[['sqft_above']].values )
        df5['sqft_basement'] = self.sqft_basement_scaler.transform( df5[['sqft_basement']].values )
        df5['yr_renovated']  = self.yr_renovated_scaler.transform(  df5[['yr_renovated']].values )
        df5['sqft_living15'] = self.sqft_living15_scaler.transform( df5[['sqft_living15']].values)
        df5['sqft_lot15']    = self.sqft_lot15_scaler.transform(    df5[['sqft_lot15']].values)

        ## 5.2 Enconding
        
        # label enconding
        df5['season']  = self.season_scaler.transform( df5['season'] )
        df5['zipcode'] = self.zipcode_scaler.transform(df5['zipcode'] )
        
        # frequency enconding
        
        city_freq ={'seattle': 41.53248195446974,'kenmore': 1.3094577086803627,'sammamish': 3.7016472330186936,'redmond': 4.529890801406626,
                    'federal_way': 3.604478993151953,'maple_valley': 2.729964834351286,'bellevue': 6.510272071071626,'duvall':0.8791412178419398,
                    'auburn': 4.21987784564131,'mercer_island': 1.3048306496390893,'kent': 5.56635202665186,'issaquah': 3.3916342772533774,
                    'renton': 7.389413288913567,'vashon': 0.5459929668702573,'kirkland': 4.52063668332408,'black_diamond': 0.4627059041273367,
                    'north_bend': 1.022580048121414,'woodinville': 2.179344808439756,'snoqualmie': 1.4343883027947435,
                    'enumclaw':1.082731815657968,'fall_city': 0.3747917823431427,'bothell': 0.9022765130483066,
                    'carnation': 0.5737553211178975,'medina': 0.23135295206366835}
        df5['city'] = df5['city'].map(city_freq)
        
        
        ## 5.3 Transformacao

        ### 5.3.2 Nature Transformation

        #month
        df5['month_sin'] = df5['month'].apply( lambda x: np.sin( x * ( 2 * np.pi / 12 ) ) )
        df5['month_cos'] = df5['month'].apply( lambda x: np.cos( x * ( 2 * np.pi / 12 ) ) )
        
        # day
        df5['day_sin'] = df5['day'].apply( lambda x: np.sin( x * ( 2 * np.pi / 30 ) ) )
        df5['day_cos'] = df5['day'].apply( lambda x: np.cos( x * ( 2 * np.pi / 30 ) ) )
        
        cols_selected = ['sqft_living','sqft_lot','waterfront','view','grade','sqft_above','yr_built','zipcode','lat',
                         'long','sqft_living15','sqft_lot15']
        
        return df5[ cols_selected ]
    
    def get_prediction( self, model, original_data, test_data ):
        
        #prediction
        pred = model.predict( test_data )
        
        #join pred into the original data
        original_data['prediction'] = np.expm1( pred )
        
        return original_data.to_json( orient = 'records', date_format = 'iso' )
