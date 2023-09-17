
import pandas as pd
import traceback
import os

from .constants import *


__all__ = ['Statements']
    
#  ███████ ████████  █████  ████████ ███████ ███    ███ ███████ ███    ██ ████████ ███████ 
#  ██         ██    ██   ██    ██    ██      ████  ████ ██      ████   ██    ██    ██      
#  ███████    ██    ███████    ██    █████   ██ ████ ██ █████   ██ ██  ██    ██    ███████ 
#       ██    ██    ██   ██    ██    ██      ██  ██  ██ ██      ██  ██ ██    ██         ██ 
#  ███████    ██    ██   ██    ██    ███████ ██      ██ ███████ ██   ████    ██    ███████ 
#  
class Statements:
    def __init__(self, root_dir = ROOT_DIR, accounts = STATEMENT_ACCOUNTS.keys()):

        self.root_dir = root_dir
        self.statments = {}
        self.accounts = accounts

    def __all__(self):
        return ['load_statement','get_transaction']
    
    
    #  █   █▀█ ▄▀█ █▀▄    █▀ ▀█▀ ▄▀█ ▀█▀ █▀▄▀█ █▀▀ █▄ █ ▀█▀ 
    #  █▄▄ █▄█ █▀█ █▄▀ ▄▄ ▄█  █  █▀█  █  █ ▀ █ ██▄ █ ▀█  █  
    #  
    def load_statment(self, account):
        data = pd\
            .read_csv(self.root_dir + BANK_STATEMENTS_DIR + '/' + account + '.csv', header=0)\
            .rename(columns={
                'Date': 'date',
                'Description':'description',
                'Debits and credits':'amount'
            })[['date','description','amount']]
        
        data.loc[:,'date'] = pd.to_datetime(data.loc[:,'date'], format="%d/%m/%Y").apply(lambda x: x.strftime('%e-%b-%Y'))

        return data
    
    
    #  █▀▀ █▀▀ ▀█▀    ▀█▀ █▀█ ▄▀█ █▄ █ █▀ ▄▀█ █▀▀ ▀█▀ █ █▀█ █▄ █ 
    #  █▄█ ██▄  █  ▄▄  █  █▀▄ █▀█ █ ▀█ ▄█ █▀█ █▄▄  █  █ █▄█ █ ▀█ 
    #  
    def get_transaction(self, account, transaction_number):
        '''
        
        
        returns
        -------
        data, message, status_code
            data: dictionary
                'transaction': dictionary for transaction
                'prediction':  dictionary for prediction

            message: string
                string response 

            status_code: int
                https status code
        '''
        
        if account not in self.accounts:
            return [], "sorry, could not find this account", 400

        if not(account in self.statments.keys()):
            try:
                self.statments[account] = self.load_statment(account)
            except Exception as e:
                traceback.print_exc()
                return [], "sorry, error loading statement", 400
            
        if transaction_number >= self.statments[account].shape[0]:
            return {'max_transactions': str(self.statments[account].shape[0])}, "no more transactions!", 206
            # return {'transaction': 'asdfasdf', 'prediction': "adsf"}, "no more transactions!", 206
        
        transaction = self.statments[account].iloc[transaction_number].to_dict()
        prediction = self.predict_transaction(transaction)
        
        return {'transaction': transaction, 'prediction': prediction}, 'Found transaction', 200
        
        # return 'asdf', 'no more transactions!', 204
    
    
    #  █▀█ █▀█ █▀▀ █▀▄ █ █▀▀ ▀█▀    ▀█▀ █▀█ ▄▀█ █▄ █ █▀ ▄▀█ █▀▀ ▀█▀ █ █▀█ █▄ █ 
    #  █▀▀ █▀▄ ██▄ █▄▀ █ █▄▄  █  ▄▄  █  █▀▄ █▀█ █ ▀█ ▄█ █▀█ █▄▄  █  █ █▄█ █ ▀█ 
    #  
    def predict_transaction(self, transaction):
        ''''
        current does a basic prediction algorithm atm. 

        parameters
        ----
        transaction
            full row of from statements, including date, description amount etc..

        return
        -----
        prediction
            predicted values to be sent to front end, in a dictionary format of
            {
                'description_tag': {'tag': 'x', 'name': 'bob'},
                'selected_code': [1,'s','f'],
                'description_short': 'asdf',
                'movement': 'input',
            }
        '''
        try:
            history = pd.read_csv(ROOT_DIR + HISTORIC_CLASSIFICATIONS,header=0)\
            
            print('history contains: ' + str(history.shape))
            selected_history = history[history['description_full'] == transaction['description']]
            print('matching history: ' + str(selected_history.shape))
            # print('matchin codes: ' + str(selected_history['code']))
            # print('mode of codes: ' + str(selected_history['code'].mode().values))
            
            # if nothing was selected
            if selected_history.shape[0] == 0:
                print('Nothing to predict')
                return None
                    

            predicted = {}
            for column in ['code','movement','description_short']:

                #
                matching_values = selected_history[column].mode().values
                if matching_values:
                    
                    # selects the most common element
                    predicted[column] = matching_values[0]

                    # if predicting the code, does some manipulations to split it up
                    if column == 'code':
                        code_half = predicted[column].split('=')[1].split('-')
                        predicted['selected_code'] = [predicted[column][0]] + [*(code_half[0])]
                        predicted['description_tag'] = {'tag': code_half[1][0],'name': code_half[1][1:]} if len(code_half) > 1 else {'tag':None,'name': None}

            
            # sets output, adds null if no data
            prediction = {}
            for parameter in ['description_tag','selected_code','description_short','movement']:
                prediction[parameter] = predicted[parameter] if parameter in predicted else None

            return prediction
        
        # if there was any error, returns nothing
        except Exception as e:
            traceback.print_exc()
            return None
        


    #     
    #  █▀█ █▀█ █▀ ▀█▀    ▀█▀ █▀█ ▄▀█ █▄ █ █▀ ▄▀█ █▀▀ ▀█▀ █ █▀█ █▄ █ 
    #  █▀▀ █▄█ ▄█  █  ▄▄  █  █▀▄ █▀█ █ ▀█ ▄█ █▀█ █▄▄  █  █ █▄█ █ ▀█ 
    #  
    def post_transaction(self, data):
        '''
        takes a dictionary of data and returns results from trying to insert said data
        
        parameters
        ------
        data
            transaction to insert
            # data example = {"movement":null,"amount":52.5,"where":"blue_card","code":"2-F","desc":"test","date":"22/08/2023"}

        returns
        -------
        message, status_code
            message: string
                string response 

            status_code: int
                https status code
        
        '''

        # checking input is a dictionary 
        if type(data) != dict:
            return 'invalid input', 400

        # asserts the data is in the correct format
        for item in list(set(SAVED_TRANSACTION_COLUMNS_NEEDED) | set(SAVED_CLASSIFICATION_COLUMNS_NEEDED)):
            if item not in data.keys():
                print('missing data')
                return 'missing data: ' + item, 400

        if not data['movement'] in MOVEMENT_TYPES:
            print('invalid movement')
            return 'invalid movement type: ' + str(data['movement']), 400
        
        data['change'] = data['change'] if 'change' in data else 0
        data['tax'] = data['tax'] if 'tax' in data else 0

        data['total'] = float(data['amount']) - float(data['change'])
        # adds todays date
        data['submitted_date'] = pd.Timestamp.now()

        # printing data
        print('data: ' + str(data))

        # inserting transaction to output
        if self._insert_transaction(data) == -1:
            return 'error inserting transaction', 500
        
        # saving transaction to list
        if self._save_classification(data) == -1:
            return 'error saving transaction', 500
        
        return 'success saving transaction', 202
    

    
    #     █▀ ▄▀█ █ █ █▀▀    █▀▀ █   ▄▀█ █▀ █▀ █ █▀▀ █ █▀▀ ▄▀█ ▀█▀ █ █▀█ █▄ █ 
    #  ▄▄ ▄█ █▀█ ▀▄▀ ██▄ ▄▄ █▄▄ █▄▄ █▀█ ▄█ ▄█ █ █▀  █ █▄▄ █▀█  █  █ █▄█ █ ▀█ 
    #  
    def _save_classification(self,data):
        # saves the file to the classification list
        try:
            file_name = ROOT_DIR + HISTORIC_CLASSIFICATIONS

            if os.path.exists(file_name):
                classifications = pd.read_csv(file_name, header = 0)
            else:
                classifications = pd.DataFrame(columns = SAVED_CLASSIFICATION_COLUMNS)

            classifications.loc[len(classifications)] = [data[key] for key in SAVED_CLASSIFICATION_COLUMNS]

            classifications\
                .sort_values(
                    ['movement','date'],
                    ascending = [True, True]
                )\
                .to_csv(file_name, index= False)
            
            return 1
        except Exception as e:
            traceback.print_exc()
            return -1

    
    #     █ █▄ █ █▀ █▀▀ █▀█ ▀█▀    ▀█▀ █▀█ ▄▀█ █▄ █ █▀ ▄▀█ █▀▀ ▀█▀ █ █▀█ █▄ █ 
    #  ▄▄ █ █ ▀█ ▄█ ██▄ █▀▄  █  ▄▄  █  █▀▄ █▀█ █ ▀█ ▄█ █▀█ █▄▄  █  █ █▄█ █ ▀█ 
    #  
    def _insert_transaction(self, data):
        # inserts the data into transaction file
        try:
            
            file_name = ROOT_DIR + TRANSACTIONS_OUTPUT_DIR

            if os.path.exists(file_name):
                transactions = pd.read_csv(file_name, header = 0)
            else:
                transactions = pd.DataFrame(columns = SAVED_TRANSACTION_COLUMNS)

            # converts full name to short hand
            data['where'] = ALL_ACCOUNT_LIKE[data['where']]

            # saves data
            transactions.loc[len(transactions)] = [(data[key] if key in data else '') for key in SAVED_TRANSACTION_COLUMNS]


            transactions\
                .sort_values(
                    ['movement','date'],
                    ascending = [True, True]
                )\
                .to_csv(file_name, index = False)

            return 1
        except Exception as e:
            traceback.print_exc()
            return -1

