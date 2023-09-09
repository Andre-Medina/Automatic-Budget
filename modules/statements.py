
import pandas as pd
import traceback
import os

from .constants import *


__all__ = ['Statements']

class Statements:
    def __init__(self, root_dir = ROOT_DIR, accounts = STATEMENT_ACCOUNTS.keys()):

        self.root_dir = root_dir
        self.statments = {}
        self.accounts = accounts

    def __all__(self):
        return ['load_statement','get_transaction']
    
    #  loads a statement
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
    

    # gets a transaction
    def get_transaction(self, account, transaction):
        
        if account not in self.accounts:
            return "sorry, could not find this account"

        if not(account in self.statments.keys()):
            try:
                self.statments[account] = self.load_statment(account)
            except Exception as e:
                traceback.print_exc()
                return "sorry, error loading statement", 400
            
        if transaction > self.statments[account].shape[0]:
            return "no more transactions!", 204
        
        return self.statments[account].iloc[transaction].to_dict()
    

    # 
    def post_transaction(self, data):
        # data example = {"movement":null,"amount":52.5,"where":"blue_card","code":"2-F","desc":"test","date":"22/08/2023"}

        if type(data) != dict:
            return 'invalid input', 400

        # asserts the data is in the correct format
        for item in list(set(SAVED_TRANSACTION_COLUMNS_NEEDED) | set(SAVED_CLASSIFICATION_COLUMNS_NEEDED)):
            if item not in data.keys():
                return 'missing data: ' + item, 400

        if not data['movement'] in MOVEMENT_TYPES:
            return 'invalid movement type: ' + str(data['movement']), 400
        
        data['change'] = data['change'] if 'change' in data else 0
        data['tax'] = data['tax'] if 'tax' in data else 0

        data['total'] = float(data['amount']) - float(data['change'])

        if self._insert_transaction(data) == -1:
            return 'error inserting transaction', 500
        
        if self._save_classification(data) == -1:
            return 'error saving transaction', 500
        
        return 'success saving transaction', 202
    


    def _save_classification(self,data):
        # saves the file to the classification list
        file_name = ROOT_DIR + HISTORIC_CLASSIFICATIONS

        if os.path.exists(file_name):
            classifications = pd.read_csv(file_name)
        else:
            classifications = pd.DataFrame(columns = SAVED_CLASSIFICATION_COLUMNS)

        classifications.loc[len(classifications)] = [data[key] for key in SAVED_CLASSIFICATION_COLUMNS]

        classifications.to_csv(file_name, index= False)



    def _insert_transaction(self, data):
        # inserts the data into transaction file

        file_name = ROOT_DIR + CLASSIFIED_TRANSACTIONS_DIR + data['movement'] + '.csv'

        if os.path.exists(file_name):
            transactions = pd.read_csv(file_name)
        else:
            transactions = pd.DataFrame(columns = SAVED_TRANSACTION_COLUMNS)

        # converts full name to short hand
        data['where'] = ALL_ACCOUNT_LIKE[data['where']]

        transactions.loc[len(transactions)] = [(data[key] if key in data else '') for key in SAVED_TRANSACTION_COLUMNS]

        transactions.to_csv(file_name, index= False)



