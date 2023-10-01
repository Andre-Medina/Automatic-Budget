'''
This file holds the constants 

-----
'''

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
CLASSIFIED_TRANSACTIONS_DIR = DATA_DIR + 'classified_transactions/'
CLASSIFICATION_JSON_DIR = DATA_DIR + 'classification/'




CLASSIFICATION_JSON_DIR_LVL_1 = CLASSIFICATION_JSON_DIR + "level_1.json"
CLASSIFICATION_JSON_DIR_LVL_2 = CLASSIFICATION_JSON_DIR + "level_2.json"
CLASSIFICATION_JSON_DIR_LVL_3 = CLASSIFICATION_JSON_DIR + "level_3.json"

HISTORIC_CLASSIFICATIONS = CLASSIFICATION_JSON_DIR + 'historic_classifications.csv'

TRANSACTIONS_OUTPUT_DIR_NEEDS_DATE_AND_DOT_CSV = CLASSIFIED_TRANSACTIONS_DIR + 'classified_output_' # + date.csv



STATEMENT_ACCOUNTS = {
    'pink_card': 'bd',
    'blue_card': 'be',
    'green_card': 'br',
    'input': 'bs',
    'savings': 'bb',
    'holiday': 'bh',
    'outings': 'bo',
  }

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