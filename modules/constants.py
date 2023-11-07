'''
This file holds the constants 

-----
'''
import pandas as pd

all = [
    'DATA_DIR',
    'BANK_STATEMENTS_DIR',
    'CLASSIFIED_TRANSACTIONS','_DIR',
    'CLASSIFICATION_JSON_DIR',
    'CLASSIFICATION_JSON_DIR_LVL_1',
    'CLASSIFICATION_JSON_DIR_LVL_2',
]

ROOT_DIR = ""
DATA_DIR = 'data/'
BANK_STATEMENTS_DIR = DATA_DIR + 'bank_statements/'
UNSORTED_BANK_STATEMENTS_DIR = BANK_STATEMENTS_DIR + 'unsorted/'
CLASSIFIED_TRANSACTIONS_DIR = DATA_DIR + 'classified_transactions/'
CLASSIFICATION_JSON_DIR = DATA_DIR + 'classification/'




CLASSIFICATION_JSON_DIR_LVL_1 = CLASSIFICATION_JSON_DIR + "level_1.json"
CLASSIFICATION_JSON_DIR_LVL_2 = CLASSIFICATION_JSON_DIR + "level_2.json"
CLASSIFICATION_JSON_DIR_LVL_3 = CLASSIFICATION_JSON_DIR + "level_3.json"

HISTORIC_CLASSIFICATIONS = CLASSIFICATION_JSON_DIR + 'historic_classifications.csv'


# Mini funciton to format a dir as follows:
#     """ CLASSIFIED_TRANSACTIONS_DIR + #'yyyy-mm-dd + '_classified_output_' + dd-mmm-yyyy.csv"""
TRANSACTIONS_OUTPUT_DIR = (lambda date: 
        f"{CLASSIFIED_TRANSACTIONS_DIR}{pd.to_datetime(date).to_period('W-SUN').start_time.strftime('%Y-%m-%d')}_classified_output_"
        f"{pd.to_datetime(date).to_period('W-SUN').start_time.strftime('%d-%b-%Y')}.csv"
    )

ACCOUNT_NUMBERS = {
    '000822269': 'pink_card',
    '001617284': 'blue_card',
    '000834315': 'green_card',
    '000822270': 'input',
    # 'savings': 'bb',
    # 'holiday': 'bh',
    # 'outings': 'bo',
}


# accounts that appear in the list
COMMON_STATEMENT_ACCOUNTS = {
    'pink_card': 'bd',
    'blue_card': 'be',
    'green_card': 'br',
    'input': 'bs',
}

# accounts to store statements of
STATEMENT_ACCOUNTS = COMMON_STATEMENT_ACCOUNTS | {
    'savings': 'bb',
    'holiday': 'bh',
    'outings': 'bo',
  }

# all accounts
ALL_ACCOUNT_LIKE = STATEMENT_ACCOUNTS | {
    'loan': '2=-l',
    'on me wallet': 'ow',
    'on me coins': 'oc',
    'home wallet': 'hw',
    'home coins': 'hc',
}




MOVEMENT_TYPES = ['input','output','transfer','work']


SAVED_TRANSACTION_COLUMNS =          ['movement',    'amount',   'change',   'total' ,           'tax',                  'where',   'code',  'description_short',    'date']
SAVED_TRANSACTION_COLUMNS_TRANSFER = ['movement',    'total',    'where',    'transfer_account', 'description_short',    'date']
SAVED_TRANSACTION_COLUMNS_NEEDED = ['movement','amount','tax','where','code','description_short','date','transfer_account']
SAVED_CLASSIFICATION_COLUMNS_NEEDED = ['movement','tax','date','where','description_full','code','description_short','transfer_account']
SAVED_CLASSIFICATION_COLUMNS = ['movement','total','tax','date','where','description_full','code','description_short','submitted_date','transfer_account']



# PINK_CARD_STATEMENT = BANK_STATEMENTS_DIR + 'pink_card.csv'
# BLUE_CARD_STATEMENT = BANK_STATEMENTS_DIR + 'blue_card.csv'