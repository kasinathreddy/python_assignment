from sqlalchemy import Column, ForeignKey, String, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


# Creating RRN table
class Rrn(base):
    __tablename__ = 'RRN'

    rrn = Column('rrn', Integer, primary_key=True)

    def __init__(self, rrn):
        self.rrn = rrn


# Creating TRANSACTIONS table
class Transactions(base):
    __tablename__ = 'TRANSACTIONS'

    tid = Column('tid', Integer, primary_key=True)
    txn_date = Column('txn_date', Date)
    rrn = Column('rrn', Integer, ForeignKey('RRN.rrn'))
    ifsc_code = Column('ifsc_code', Integer)
    bank_name = Column('bank_name', String)
    account_holder = Column('account_holder', String)
    transaction_type = Column('transaction_type', String)
    amount = Column('amount', Float)

    def __init__(self, txn_date, rrn, ifsc_code, bank_name, account_holder, transaction_type, amount):
        self.txn_date = txn_date
        self.rrn = rrn
        self.ifsc_code = ifsc_code
        self.bank_name = bank_name
        self.account_holder = account_holder
        self.transaction_type = transaction_type
        self.amount = amount
