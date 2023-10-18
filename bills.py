import pandas as pd
import os 
import datetime
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy import column
from pathlib import Path

## My modules
import etl_utils as etl
from tables import *

def main():

    ## Application parameters
    lookback_days = 30
    # datapath = "C:/Users/Tim/iCloudDrive/qb_data"
    main_path = "./"

    load_dotenv()

    ## QB connection
    qb_cxn_parameters = {
        'db_user': os.getenv('DB_USER'),
        'db_password': os.getenv('DB_PASSWORD'),
        'db_host': os.getenv('DB_HOST'),
        'db_port': os.getenv('DB_PORT')
    }
    
    qb_engine = etl.connect_to_db(qb_cxn_parameters)

    ## PostgreSQL
    pg_cxn_parameters = {
        'db_user': os.getenv('PG_DB_USER'),
        'db_password': os.getenv('PG_DB_PASSWORD'),
        'db_host': os.getenv('PG_DB_HOST'),
        'db_port': os.getenv('PG_DB_PORT'),
        'db_name': os.getenv('PG_DB_NAME')
    }
    
    pg_engine = etl.connect_to_db(qb_cxn_parameters)

    ## Create all the tables in tables.py
    metadata_obj.create_all(qb_engine)

    ## Extract
    datefilter = datetime.date.today() + datetime.timedelta(days=-lookback_days)
    stmt = select(tbl_bills).filter(column("DueDate") >= datefilter)
    df = etl.quickbooks_to_dataframe(stmt, qb_engine)

    ## Placde a copy on local disk
    landing_path = Path(main_path) / "data" / "raw_bills.pkl"
    etl.data_to_source(df, landing_path)

    ## Insert the datframe into PG
    table_name = 'lfg_bills'
    table_schema = 'landing'
    etl.data_to_landing(df, pg_engine, table_name, table_schema)




if __name__ == "__main__":
    main()