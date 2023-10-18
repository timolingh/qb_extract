# import re
# import io
# from datetime import datetime
# import hashlib
import pandas as pd
from sqlalchemy import create_engine

def connect_to_db(cxn_parameters, echo=False):
    if 'db_name' in cxn_parameters.keys():
        db_user = cxn_parameters['db_user']
        db_password = cxn_parameters['db_password']
        db_user = cxn_parameters['db_user']
        db_host = cxn_parameters['db_host']
        db_port = cxn_parameters['db_port']
        db_name = cxn_parameters['db_name']
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}', echo=echo)
    else:
        db_user = cxn_parameters['db_user']
        db_password = cxn_parameters['db_password']
        db_host = cxn_parameters['db_host']
        db_port = cxn_parameters['db_port']
        engine = create_engine(f"quickbooks_2:///?URL=http://{db_host}:{db_port}&User={db_user}&Password={db_password}", echo=echo)

    return engine

def quickbooks_to_dataframe(stmt, engine):
    df = pd.read_sql_query(stmt, engine)
    return df

def data_to_source(df, fpath):
    nrows = df.shape[0]
    if nrows > 0:
        df.to_pickle(fpath)
        return 0
    else:
        return 1
    
def data_to_landing(df, engine, table_name, schema_name):
    nrows = df.shape[0]
    if nrows > 0:
        try:
            df.to_sql(table_name, engine, schema_name, index=False, if_exists='replace')
            return 0
        except Exception as e:
            return str(e)
    else:
        return 0

def get_existing_qb_keys(engine, schema, table):
    try:
        existing_hashes = pd.read_sql_table(
            table, engine, schema=schema, columns=['ID']
            ).drop_duplicates()
    except ValueError:
        existing_hashes = pd.DataFrame({'ID': []})

    return existing_hashes

def staging_to_prod(engine, source_df, target_schema, target_table):

    prod_df = source_df.copy()

    ## Existing hashes in the target prod table
    existing_hashes = get_existing_qb_keys(engine, target_schema, target_table)
    new_prod_df = prod_df.loc[~prod_df['ID'].isin(existing_hashes['ID']), :]
    nrows_before = prod_df.shape[0]
    nrows_after = new_prod_df.shape[0]
    print(f'Before rows: {nrows_before}; After rows: {nrows_after}')

    ## Write to db
    try:
        new_prod_df.to_sql(target_table, engine, target_schema, index=False, if_exists='append')
        return 0
    except Exception as e:
        return str(e)

## Debugging section
def main():

    import os
    import pandas as pd
    from dotenv import load_dotenv

    load_dotenv()
    cxn_parameters = {
        'db_user': os.getenv('DB_USER'),
        'db_password': os.getenv('DB_PASSWORD'),
        'db_host': os.getenv('DB_HOST'),
        'db_port': os.getenv('DB_PORT'),
        'db_name': os.getenv('DB_NAME')
    }
    
    engine = connect_to_db(cxn_parameters)
    df = pd.read_sql_query("select * from Bills limit 10", engine)
    print(df.head())

if __name__ == "__main__":
    main()