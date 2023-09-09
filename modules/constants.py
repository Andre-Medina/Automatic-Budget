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

HISTORIC_CLASSIFICATIONS = CLASSIFICATION_JSON_DIR + 'historic_classifications.csv'





STATEMENT_ACCOUNTS = {
    'pink_card': 'bd',
    'blue_card': 'be',
  }
ALL_ACCOUNT_LIKE = STATEMENT_ACCOUNTS | {
    'loan': '2=-l'
} 



MOVEMENT_TYPES = ['input','output','transfer','work']


SAVED_TRANSACTION_COLUMNS = ['amount','change','total','tax','where','code','description_short','date']
SAVED_TRANSACTION_COLUMNS_NEEDED = ['amount','where','code','description_short','date']
SAVED_CLASSIFICATION_COLUMNS_NEEDED = ['movement','date','where','description_full','code','description_short']
SAVED_CLASSIFICATION_COLUMNS = ['movement','date','where','description_full','code','description_short']


# PINK_CARD_STATEMENT = BANK_STATEMENTS_DIR + 'pink_card.csv'
# BLUE_CARD_STATEMENT = BANK_STATEMENTS_DIR + 'blue_card.csv'