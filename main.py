# importing needed modules
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO
import pandas as pd
from query_execution import QueryExec
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import base

engine = create_engine("sqlite:///transactions.db", echo=True)
base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})
query_exec = QueryExec(session)


def process_data(input_df):
    input_df['TXN DATE'] = pd.to_datetime(input_df['TXN DATE'])
    input_df.sort_values(by='TXN DATE', inplace=True)
    # txn / acc_number / rrn / ifsc_number / bank_name / acc_holder_name / txn_type
    # data is given in above format with in NARRATION column, and we are extracting it below
    input_df['NARRATION'] = input_df['NARRATION'].apply(lambda x: list(map(lambda y: y.strip(), x.split('/')[2:])))
    input_df['RRN'] = input_df['NARRATION'].apply(lambda x: int(x[0].strip('RRN:')))
    input_df['IFSC'] = input_df['NARRATION'].apply(lambda x: x[1])
    input_df['BANK'] = input_df['NARRATION'].apply(lambda x: x[2])
    input_df['ACC_HOLDER'] = input_df['NARRATION'].apply(lambda x: x[3].title())
    input_df['TXN_TYPE'] = input_df['NARRATION'].apply(lambda x: x[4])
    input_df = input_df[['TXN DATE', 'RRN', 'IFSC', 'BANK', 'ACC_HOLDER', 'TXN_TYPE', 'AMOUNT']].reset_index(drop=True)
    return input_df


@app.post("/post_data")
def upload(file: UploadFile = File(...)):
    """
    Functionality:
    This end point is responsible for accepting user input data and processes the input data and loads it into database
    - **file** : Needs a csv file as input,and you can upload it by clicking Choose File if testing interactively

    """
    contents = file.file.read()
    buffer = BytesIO(contents)
    df = pd.read_csv(buffer)
    buffer.close()
    file.file.close()
    out = process_data(df)
    query_exec.post_data_query_rrn(out)
    query_exec.post_data_query_transactions(out)
    return JSONResponse(content={"message": "success"})


@app.get("/records")
def get_records():
    """
    Functionality:
    This end point is responsible for returning number of transactions present inside the database
    """
    out = query_exec.get_record_count()
    return JSONResponse(content={"records_count": out})


@app.get("/banks")
def get_banks():
    """
    Functionality:
    This end point is responsible for returning number of unique banks present inside the database
    """
    out = query_exec.get_unique_bank_count()
    return JSONResponse(content={"unique_bank_count": out})


@app.get("/{from_date}/{to_date}")
def get_transactions_in_given_time(from_date, to_date):
    """
    Functionality:
    This end point is responsible for returning number of
    transactions present inside the database provided the from_date and to_date
    - **from_date** : Needs a date from user in YYYY-MM-DD format which
    acts a starting date from where user wants to know the transactions
    - **to_date** : Needs a date from user in YYYY-MM-DD format which
    acts as ending date till where user wants to know the transactions
    """
    out = query_exec.get_transactions_in_given_range(from_date, to_date)
    return JSONResponse(content={f"number of transactions between {from_date} and {to_date}": out})


@app.get("/customer_names")
def get_customer_names():
    """
    Functionality:
    This end point is responsible for returning names of unique customers inside the database
    """
    out = query_exec.get_customer_names()
    return JSONResponse(content={'customer_names': out})


@app.get("/transactions_summary")
def get_transactions_summary():
    """
    Functionality:
    This end point is responsible for returning number of transactions
    according to their type present inside the database
    """
    out = query_exec.get_transactions_summary()
    return JSONResponse(content=out)


@app.get("/transaction_amount_summary")
def get_transaction_amount_summary():
    """
    Functionality:
    This end point is responsible for returning sum of transactional amount
    according to their type present inside the database
    """
    out = query_exec.get_transaction_amount_summary()
    return JSONResponse(content=out)


@app.get("/total_transaction_amount")
def get_total_transaction_amount():
    """
    Functionality:
    This end point is responsible for returning sum of total transactional amount present inside the database
    """
    out = query_exec.get_total_transaction_amount()
    return JSONResponse(content={'total transaction amount': out})
