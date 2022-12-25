## Setup
1) Once you are inside the code repository open your command prompt
2) run the command **pip install -r requirements.txt** to install the dependencies

## Starting the server
- Once you are in the code repository after installing the dependencies
- Run the following command in command prompt
- **uvicorn main:app --reload**

## Testing the api
- Once the server is started you can go to http://127.0.0.1:8000/docs over a browser
- You will be able to execute available api calls and do the needed steps after pressing **Try it out** before executing the end point according to the instructions present at each end point
- You can also use postman to test the end points

## Testing flow
- We will be using the post call first post_data to load the data into database
- Later we can use get calls to retrieve the desired output

## DataModel
- We will be using sqllite
- We will have two tables 
  1) RRN
  2) Transactions
- RRN table will have unique RRN numbers where it is a primary key and column name is **rrn**
- Transactions table will have all the transactions data
  - tid is a primary key which is a integer(serial)
  - txn_date is a column where transaction date is stored in YYYY-MM-DD format
  - ifsc_code is a column where ifsc_code of that particular bank transaction is stored
  - bank_name is a column where bank name of that transaction is stored
  - account_holder is a column where we store name of the customer
  - transaction_type is a column where we store type of the transaction
  - amount is a column where we store the amount relevant to that particular transaction

