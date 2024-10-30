import os 
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy import column
from pathlib import Path
import xmltodict
from quickbooks_desktop.session_manager import SessionManager

## My modules
from xml_query import TransactionQuery, QbResp
import etl_utils as etl
from qb_path import *
from tables import *

def main():

    ## Application parameters
    lookback_days = 14
    qb_path = Path(linkage_file)

    ## Postgres secrets
    load_dotenv(override=True)
    pg_cxn_parameters = {
        'db_user': os.getenv('PG_DB_USER'),
        'db_password': os.getenv('PG_DB_PASSWORD'),
        'db_host': os.getenv('PG_DB_HOST'),
        'db_port': os.getenv('PG_DB_PORT'),
        'db_name': os.getenv('PG_DB_NAME')
    }
    
    pg_engine = etl.connect_to_db(pg_cxn_parameters)

    ## Create tables in tables.py
    tbl_lfg_transactions.create(pg_engine.connect().execution_options(schema_translate_map={None: "landing"}, isolation_level="AUTOCOMMIT"), checkfirst=True)
    tbl_lfg_transactions.create(pg_engine.connect().execution_options(schema_translate_map={None: "staging"}, isolation_level="AUTOCOMMIT"), checkfirst=True)
    tbl_prod_lfg_transactions.create(pg_engine.connect().execution_options(isolation_level="AUTOCOMMIT"), checkfirst=True)

    ## Extract
    transaction_query = TransactionQuery(days_lookback=lookback_days)
    session = SessionManager(company_file=qb_path)
    my_results = session.send_xml(transaction_query.xml_root)
    results_dict = xmltodict.parse(my_results).get("QBXML").get("QBXMLMsgsRs")

    ## Transform
    transaction_response = QbResp.transaction_response(results_dict)
    dict_sourcedata = transaction_response.transform_data()


    ## Insert the datframe into PG landing schma
    _ = etl.qb_data_to_landing(pg_engine, tbl_lfg_transactions, dict_sourcedata)

    ## Copy the same data to staging - No transformation
    _ = etl.qb_data_to_staging(pg_engine, tbl_lfg_transactions, dict_sourcedata)

    ## copy new data from staging to prod while updating records
    _ = etl.delete_stale_prod(pg_engine, tbl_lfg_transactions, tbl_prod_lfg_transactions)
    _ = etl.delete_dup_staging(pg_engine, tbl_lfg_transactions, tbl_prod_lfg_transactions)
    _ = etl.staging_to_prod(pg_engine, tbl_lfg_transactions, tbl_prod_lfg_transactions)


if __name__ == "__main__":
    main()