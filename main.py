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
    cxn_parameters = {
        'db_user': os.getenv('DB_USER'),
        'db_password': os.getenv('DB_PASSWORD'),
        'db_host': os.getenv('DB_HOST'),
        'db_port': os.getenv('DB_PORT'),
        'db_name': os.getenv('DB_NAME')
    }
    
    engine = etl.connect_to_db(cxn_parameters)

    ## Create all the tables in tables.py
    metadata_obj.create_all(engine)

    ## Bills Raw Data
    datefilter = datetime.date.today() + datetime.timedelta(days=-lookback_days)
    stmt = select(tbl_bills).filter(column("DueDate") >= datefilter)
    df = etl.quickbooks_to_dataframe(stmt, engine)
    landing_path = Path(main_path) / "data" / "raw_bills.pkl"
    etl.data_to_staging(df, landing_path)


if __name__ == "__main__":
    main()