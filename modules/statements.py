
import pandas as pd
import traceback

from .constants import *


__all__ = ['Statements']

class Statements:
    def __init__(self, root_dir = ROOT_DIR, accounts = STATEMENT_ACCOUNTS):

        self.root_dir = root_dir
        self.statments = {}
        self.accounts = STATEMENT_ACCOUNTS

    def __all__(self):
        return ['load_statement','get_transaction']
    
    #  loads a statement
    def load_statment(self, account):
        return pd\
            .read_csv(self.root_dir + BANK_STATEMENTS_DIR + '/' + account + '.csv', header=0)\
            .rename(columns={
                'Date': 'date',
                'Description':'description',
                'Debits and credits':'amount'
            })[['date','description','amount']]
    

    # gets a transaction
    def get_transaction(self, account, transaction):
        
        if account not in self.accounts:
            return "sorry, could not find this account"

        if not(account in self.statments.keys()):
            try:
                self.statments[account] = self.load_statment(account)
            except Exception as e:
                traceback.print_exc()
                return "sorry, error loading statement"
            
        if transaction > self.statments[account].shape[0]:
            return "no more transactions!"
        
        return self.statments[account].iloc[transaction].to_dict()