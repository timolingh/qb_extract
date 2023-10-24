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
    lookback_days = 5
    # datapath = "C:/Users/Tim/iCloudDrive/qb_data"
    # main_path = "./"

    load_dotenv(override=True)

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
    
    pg_engine = etl.connect_to_db(pg_cxn_parameters)

    ## Create tables in tables.py
    # metadata_obj.create_all(qb_engine)
    tbl_bills.create(qb_engine, checkfirst=True)    
    tbl_lfg_bills.create(pg_engine.connect().execution_options(schema_translate_map={None: "landing"}, isolation_level="AUTOCOMMIT"), checkfirst=True)
    tbl_lfg_bills.create(pg_engine.connect().execution_options(schema_translate_map={None: "staging"}, isolation_level="AUTOCOMMIT"), checkfirst=True)
    tbl_prod_lfg_bills.create(pg_engine.connect().execution_options(isolation_level="AUTOCOMMIT"), checkfirst=True)

    ## Extract
    datefilter = datetime.date.today() + datetime.timedelta(days=-lookback_days)
    stmt = select(tbl_bills).filter(column("DueDate") >= datefilter)
    with qb_engine.connect() as conn:
        sourcedata = conn.execute(stmt).fetchall()

    dict_sourcedata = [row._mapping for row in sourcedata]

    ## Insert the datframe into PG landing  schma
    _ = etl.qb_data_to_landing(pg_engine, tbl_lfg_bills, dict_sourcedata)

    ## Copy the same data to staging - No transformation
    _ = etl.qb_data_to_staging(pg_engine, tbl_lfg_bills, dict_sourcedata)

    ## copy new data from staging to prod while updating records
    _ = etl.delete_stale_prod(pg_engine, tbl_lfg_bills, tbl_prod_lfg_bills)
    _ = etl.delete_dup_staging(pg_engine, tbl_lfg_bills, tbl_prod_lfg_bills)
    _ = etl.staging_to_prod(pg_engine, tbl_lfg_bills, tbl_prod_lfg_bills)


if __name__ == "__main__":
    main()