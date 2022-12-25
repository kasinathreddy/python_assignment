from models import Rrn, Transactions
from fastapi import HTTPException
from sqlalchemy import func
import pandas as pd


# Query execution portion
class QueryExec:
    def __init__(self, orm_session):
        self.orm_session = orm_session

    def post_data_query_rrn(self, cleaned_data):
        """

        :param cleaned_data: cleaned_data is extracted data from user input
        :return: None

        - Inserts unique RRN number to RRN table
        """
        try:
            existing_rrn = self.orm_session.query(Rrn.rrn).all()
            existing_rrn = pd.DataFrame({'rrn_exist': list(map(lambda x: x[0], existing_rrn))})
            temp = pd.DataFrame(cleaned_data['RRN'].drop_duplicates())
            temp.columns = ['RRN']
            temp['RRN'] = temp['RRN'].apply(lambda x: Rrn(rrn=x))
            temp['rrn_num'] = temp['RRN'].apply(lambda x: x.rrn)
            temp = pd.merge(temp, existing_rrn, how='left', left_on='rrn_num', right_on='rrn_exist')
            temp = temp[temp.isnull().any(axis=1)]
            rrn_params = temp['RRN'].to_list()
            print(rrn_params)
            # doing a left join and filtering to get unique RNN which need to be inserted
            self.orm_session.add_all(rrn_params)
            self.orm_session.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f'Failed to insert into Rrn table due to {e}')

    def post_data_query_transactions(self, cleaned_data):
        """

        :param cleaned_data: cleaned_data is extracted data from user input
        :return: None

        - Inserts cleaned_data into TRANSACTIONS table
        """
        try:
            txn_params = cleaned_data.apply(lambda x: Transactions(*list(x)), axis=1).to_list()
            self.orm_session.add_all(txn_params)
            self.orm_session.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f'Failed to insert into Transactions table due to {e}')

    def get_record_count(self):
        try:
            record_cnt = self.orm_session.query(func.count(Transactions.tid)).all()
            record_cnt = record_cnt[0][0]
            return record_cnt
        except Exception as e:
            raise HTTPException(status_code=400, detail=f'Failed to get number of records due to {e}')

    def get_unique_bank_count(self):
        try:
            bank_cnt = self.orm_session.query(func.count(Transactions.bank_name.distinct())).all()
            bank_cnt = bank_cnt[0][0]
            return bank_cnt
        except Exception as e:
            raise HTTPException(status_code=400, detail=f'Failed to get number of unique banks due to {e}')

    def get_transactions_in_given_range(self, from_date, to_date):
        try:
            transactions_cnt = self.orm_session.query(func.count(Transactions.txn_date)). \
                filter(Transactions.txn_date >= from_date, Transactions.txn_date <= to_date).all()
            transactions_cnt = transactions_cnt[0][0]
            return transactions_cnt
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"""Failed to get number of transactions between {from_date}
                                and {to_date} due to {e}""")

    def get_customer_names(self):
        try:
            customer_names = self.orm_session.query(Transactions).values(Transactions.account_holder.distinct())
            customer_names = list(map(lambda x: x[0], customer_names))
            return customer_names
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to retrieve customer names due to {e}")

    def get_transactions_summary(self):
        try:
            summary = self.orm_session.query(Transactions) \
                .group_by(Transactions.transaction_type) \
                .values(Transactions.transaction_type, func.count(Transactions.transaction_type))
            summary = {i[0]: i[-1] for i in summary}
            return summary
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to retrieve transaction summary due to {e}")

    def get_transaction_amount_summary(self):
        try:
            summary = self.orm_session.query(Transactions) \
                .group_by(Transactions.transaction_type) \
                .values(Transactions.transaction_type, func.sum(Transactions.amount))
            summary = {i[0]: i[-1] for i in summary}
            return summary
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to retrieve transaction amount summary due to {e}")

    def get_total_transaction_amount(self):
        try:
            total_amnt = self.orm_session.query(func.sum(Transactions.amount)).all()
            total_amnt = total_amnt[0][0]
            return total_amnt
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"Failed to retrieve total transaction amount summary due to {e}")
