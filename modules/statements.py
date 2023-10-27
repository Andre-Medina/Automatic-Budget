
import pandas as pd
import traceback
import os

from .constants import *
from difflib import SequenceMatcher

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

        from . import select_most_recent
        data = pd\
            .read_csv(select_most_recent(self.root_dir + BANK_STATEMENTS_DIR + account + '/'), header=0)\
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

        if pd.isna(transaction['amount']) or (transaction['amount'] == 'nan'):
            transaction['amount'] = 0

        prediction = self.predict_transaction(transaction)
        classified = self.find_if_classified(transaction, account)
        
        return {'transaction': transaction, 'prediction': prediction, 'classified': classified}, 'Found transaction', 200
        
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
            selected_history = history[history['description_full'].apply(lambda x: is_same_transaction( x, transaction['description']))]
            

            print('matching history: ' + str(selected_history.shape))
            # print('matchin codes: ' + str(selected_history['code']))
            # print('mode of codes: ' + str(selected_history['code'].mode().values))
            
            # if nothing was selected
            if selected_history.shape[0] == 0:
                print('Nothing to predict')
                return None
                    

            predicted = {}
            for column in ['code','movement','description_short','transfer_account','tax']:

                #
                matching_values = selected_history[column].mode().values
                print(matching_values)

                if len(matching_values):
                    
                    # selects the most common element
                    predicted[column] = matching_values[0]

                    # if predicting the code, does some manipulations to split it up
                    if column == 'code':
                        code_half = predicted[column].split('=')[1].split('-')
                        predicted['selected_code'] = [predicted[column][0]] + [*(code_half[0])]

                        if len(code_half) > 1:
                            if code_half[1][0] in ['l','t']:
                                predicted['code_tag'] = {'selected_tag': [code_half[1][0]],'extra': code_half[1][1:]} # {'selected_tag':None,'name': None}
                            else:
                                predicted['code_tag'] = {'selected_tag': [*(code_half[1])], 'extra': None}
                        else:
                            predicted['code_tag'] = None

            print('Predictions:')
            print(predicted)

            # some type issue
            predicted['tax'] = int(predicted['tax'])


            # sets output, adds null if no data
            prediction = {}
            for parameter in ['code_tag','selected_code','description_short','movement','transfer_account','tax']:
                prediction[parameter] = predicted[parameter] if parameter in predicted else None
                
            print(prediction)

            return prediction
        
        # if there was any error, returns nothing
        except Exception as e:
            print('prediction errored out')
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

        
        # converts full name to short hand
        data['where'] = ALL_ACCOUNT_LIKE[data['where']]

        # saving transaction to list
        response, status = self._save_classification(data)
        if status != 202:
            return response, status
        
        # inserting transaction to output
        response, status = self._insert_transaction(data)
        if status != 202:
            return response, status
        
        
        return 'success saving transaction', 202
    
    
    #  █▀▀ █ █▄ █ █▀▄    █ █▀▀    █▀▀ █   ▄▀█ █▀ █▀ █ █▀▀ █ █▀▀ █▀▄ 
    #  █▀  █ █ ▀█ █▄▀ ▄▄ █ █▀  ▄▄ █▄▄ █▄▄ █▀█ ▄█ ▄█ █ █▀  █ ██▄ █▄▀ 
    #  
    def find_if_classified(self, transaction, where):

        try:
            file_name = ROOT_DIR + HISTORIC_CLASSIFICATIONS

            # checks there is data
            if os.path.exists(file_name):
                classifications = pd.read_csv(file_name, header = 0)
            else:
                return False

            # simplifying where
            where = ALL_ACCOUNT_LIKE[where]

            # finds matching classifications
            limited_classified = classifications.query(f"\
                date == @transaction['date'] &\
                where == @where &\
                description_full == @transaction['description']\
                ")

            # returns true if it found data and false if it was empty
            return limited_classified.shape[0] > 0
        
        # prints error and returns false otherwise
        except Exception as e:
            traceback.print_exc()
            return False

    
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
            
            return 'success saving classification', 202
        except Exception as e:
            traceback.print_exc()
            return 'error saving classification', 500

    
    #     █ █▄ █ █▀ █▀▀ █▀█ ▀█▀    ▀█▀ █▀█ ▄▀█ █▄ █ █▀ ▄▀█ █▀▀ ▀█▀ █ █▀█ █▄ █ 
    #  ▄▄ █ █ ▀█ ▄█ ██▄ █▀▄  █  ▄▄  █  █▀▄ █▀█ █ ▀█ ▄█ █▀█ █▄▄  █  █ █▄█ █ ▀█ 
    #  
    def _insert_transaction(self, data):
        # inserts the data into transaction file
        try:
            
            file_name = ROOT_DIR + TRANSACTIONS_OUTPUT_DIR(data['date'])
            print(file_name)

            if os.path.exists(file_name):
                transactions = pd.read_csv(file_name, header = 0)
                
                # changes actual total columns numerics to ints, transfer column puts strings in 'total' column 
                transactions.loc[transactions['movement'] != 'transfer','total'] = pd.to_numeric(transactions.loc[transactions['movement'] != 'transfer','total'], errors='coerce').replace(pd.NA, 0)
            else:
                transactions = pd.DataFrame(columns = SAVED_TRANSACTION_COLUMNS)

            if data['movement'] == 'output':
                data['change'] *= -1
                data['amount'] *= -1
                data['total'] *= -1


            def assert_no_dupelicates(transactions, data):
                if data['movement'] != 'transfer':
                    selected_transactions = transactions.query(f"\
                        movement == @data['movement'] &\
                        total == @data['total'] &\
                        where == @data['where'] &\
                        description_short == @data['description_short'] &\
                        code == @data['code'] &\
                        date == @data['date']")
                else:
                    selected_transactions = transactions.query(f"\
                        movement == @data['movement'] &\
                        amount == @data['total'] &\
                        change == @data['where'] &\
                        total == @data['transfer_account'] &\
                        where == @data['date']")
                
                return len(selected_transactions) > 0
                   
            # TODO: allowing adding duplicates, issue with tutoring on the same day
            #           added check description is the same
            if assert_no_dupelicates(transactions, data):
                return 'duplicated transaction', 500

            insert_data = []
            for i in range(max(len(SAVED_TRANSACTION_COLUMNS), len(SAVED_TRANSACTION_COLUMNS_TRANSFER))):
                if i < len( (SAVED_TRANSACTION_COLUMNS if data['movement'] != 'transfer' else SAVED_TRANSACTION_COLUMNS_TRANSFER) ):
                    key = (SAVED_TRANSACTION_COLUMNS if data['movement'] != 'transfer' else SAVED_TRANSACTION_COLUMNS_TRANSFER)[i]
                    insert_data.append(data[key] if key in data else "")
                else:
                    insert_data.append("")
                
            # inserts the data
            transactions.loc[len(transactions)] = insert_data
            # if data['movement'] != 'transfer':
            #     # saves data
            #     transactions.loc[len(transactions)] = [(data[key] if key in data else '') for key in SAVED_TRANSACTION_COLUMNS]
            # else:
            #     transactions.loc[len(transactions)] = [(data[key] if key in data else '') for key in SAVED_TRANSACTION_COLUMNS_TRANSFER]

            transactions\
                .sort_values(
                    ['movement','date'],
                    ascending = [True, True]
                )\
                .to_csv(file_name, index = False)

            return 'success inserting transaction', 202
        except Exception as e:
            traceback.print_exc()
            return 'error inserting transaction', 500

def is_same_transaction(existing, target):

    ratio_threshold = 0.65
    if (target[0:8] == 'Transfer') or (existing[0:8] == 'Transfer'):
        ratio_threshold = 0.65

    if (
        (('Transfer from Andre Medina' == existing[0:26]) and ('Transfer to Andre Medina' == target[0:24])) or
        (('Transfer from Andre Medina' == target[0:26]) and ('Transfer to Andre Medina' == existing[0:24]))
    ):
        ratio_threshold = 0.99
        


    # print(SequenceMatcher(None, existing, target).ratio())
    return SequenceMatcher(None, existing, target).ratio() > ratio_threshold