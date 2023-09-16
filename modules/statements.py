
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
        try:
            history = pd.read_csv(ROOT_DIR + HISTORIC_CLASSIFICATIONS,header=0)\
            
            print('history contains: ' + str(history.shape))
            selected_history = history[history['description_full'] == transaction['description']]
            print('matching history: ' + str(selected_history.shape))
            # print('matchin codes: ' + str(selected_history['code']))
            # print('mode of codes: ' + str(selected_history['code'].mode().values))
            code = selected_history['code'].mode().values[0]
            current_movement_type = selected_history['movement'].mode().values[0]
            short_description = selected_history['description_short'].mode().values[0]

            code_half = code.split('=')[1].split('-')
            selected_levels = [code[0]] + [*(code_half[0])]


            description_tag = {'tag': code_half[1][0],'name': code_half[1][1:]} if len(code_half) > 1 else {'tag':None,'name': None}

            prediction = {
                'description_tag':description_tag,
                'selected_levels':selected_levels,
                'short_description':short_description,
                'current_movement_type':current_movement_type
            }
            
            return prediction
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

