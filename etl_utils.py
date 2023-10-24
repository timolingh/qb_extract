# import re
# import io
# from datetime import datetime
# import hashlib
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy import select, delete, join, and_

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

def qb_data_to_landing(engine, table, values):
    with engine.connect().execution_options(schema_translate_map={None: "landing"}, isolation_level="AUTOCOMMIT") as conn:
        ## Truncate the table before insert
        fq_name = table.fullname
        conn.execute(text(f"truncate table {fq_name}"))
        conn.execute(table.insert(), values)

    return 0

def qb_data_to_staging(engine, table, values):
    with engine.connect().execution_options(schema_translate_map={None: "staging"}, isolation_level="AUTOCOMMIT") as conn:
        ## Truncate the table before insert
        fq_name = table.fullname
        conn.execute(text(f"truncate table {fq_name}"))
        conn.execute(table.insert(), values)

    return 0

def run_statement(engine, stmt):
    with engine.connect().execution_options(schema_translate_map={None: "staging"}, isolation_level="AUTOCOMMIT") as conn:
        conn.execute(stmt)
    
    return 0


def delete_stale_prod(engine, source_table, prod_table):
    j = join(prod_table, source_table, 
                and_(prod_table.c.ID == source_table.c.ID, prod_table.c.DateModified < source_table.c.DateModified)
                )
    stale_id_stmt = select(prod_table.c.ID).select_from(j)
    del_stmt = prod_table.delete().where(prod_table.c.ID.in_(stale_id_stmt))
    run_statement(engine, del_stmt)
    return 0

def delete_dup_staging(engine, source_table, prod_table):
    j = join(source_table.c.ID == prod_table.c.ID)
    in_prod_stmt = select(prod_table.c.ID).select_from(j)
    del_stmt = source_table.delete().where(source_table.c.ID.in_(in_prod_stmt))
    run_statement(engine, del_stmt)
    return 0

def staging_to_prod(engine, source_table, prod_table):
    stmt = prod_table.insert().values(source_table.select())
    run_statement(engine, stmt) 
    return 0   

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