from sqlalchemy import Table, Column
from sqlalchemy import String, DateTime, Date, Numeric
from sqlalchemy import MetaData

metadata_obj = MetaData()

## Vendors
tbl_vendors = Table(
    "Vendors",
    metadata_obj,
    Column("ID"),
    Column("Name"),
    Column("AccountNumber"),
    Column("NameOnCheck"),
    Column("TimeModified", DateTime),
    Column("TimeCreated", DateTime)
)

## Bills
## LFG Bills - destination table in PG
tbl_lfg_bills = Table(
	"lfg_bills",
	metadata_obj,
	Column("ID", String),
	Column("VendorName", String),
	Column("VendorId", String),
	Column("ReferenceNumber", String),
	Column("Date", Date),
	Column("DueDate", Date),
	Column("Terms", String),
	Column("TermsId", String),
	Column("AccountsPayable", String),
	Column("AccountsPayableId", String),
	Column("Memo", String),
    Column("LinkedTxnId", String),
    Column("LinkedTxnType", String),
	Column("IsPaid", String),
	Column("TimeModified", DateTime),
	Column("TimeCreated", DateTime),
	Column("OpenAmount", Numeric(20, 4)),
    schema=None
				  
)

tbl_prod_lfg_bills = Table(
	"lfg_bills",
	metadata_obj,
	Column("ID", String),
	Column("VendorName", String),
	Column("VendorId", String),
	Column("ReferenceNumber", String),
	Column("Date", Date),
	Column("DueDate", Date),
	Column("Terms", String),
	Column("TermsId", String),
	Column("AccountsPayable", String),
	Column("AccountsPayableId", String),
	Column("Memo", String),
    Column("LinkedTxnId", String),
    Column("LinkedTxnType", String),
	Column("IsPaid", String),
	Column("TimeModified", DateTime),
	Column("TimeCreated", DateTime),
	Column("OpenAmount", Numeric(20, 4)),
    schema="prod"
				  
)
				  

## Checks
tbl_checks = Table(
	"Checks",
	metadata_obj,
	Column("ID"),
	Column("ReferenceNumber"),
	Column("Account"),
	Column("AccountId"),
	Column("Payee"),
	Column("PayeeId"),
	Column("Date"),
	Column("Amount"),
	Column("Memo"),
	Column("IsToBePrinted"),
	Column("TimeModified", DateTime),
	Column("TimeCreated", DateTime)			   
)

##BillPaymentChecks
tbl_bill_payment_checks = Table(
	"BillPaymentChecks",
	metadata_obj,
	Column("ID"),
	Column("PayeeName"),
	Column("PayeeId"),
	Column("ReferenceNumber"),
	Column("Date"),
	Column("Amount"),
	Column("AccountsPayable"),
	Column("AccountsPayableId"),
	Column("BankAccountName"),
	Column("BankAccountId"),
	Column("IsToBePrinted"),
	Column("Memo"),
	Column("TimeModified", DateTime),
	Column("TimeCreated", DateTime)							
)

##Class
tbl_class = Table(
	"Class",
	metadata_obj,
	Column("ID"),
	Column("Name"),
	Column("FullName"),
	Column("IsActive"),
	Column("ParentRef_FullName"),
	Column("ParentRef_ListId"),
	Column("SubLevel"),
	Column("TimeCreated", DateTime),
	Column("TimeModified", DateTime)		  
)


## Alameda Court tables
tbl_ac_transactions = Table(
    "alameda_court_transactions",
    metadata_obj,
    Column("ID", String),
    Column("TransactionType", String),
    Column("TransactionDate", Date),
    Column("EntityId", String),
    Column("Entity", String),
	Column("AccountId", String),
    Column("Account", String),
    Column("RefNumber", String),
    Column("Amount", Numeric(20, 4)),
    Column("Memo", String),
    Column("TimeCreated", DateTime),
    Column("TimeModified", DateTime)
)

tbl_prod_ac_transactions = Table(
    "alameda_court_transactions",
    metadata_obj,
    Column("ID", String),
    Column("TransactionType", String),
    Column("TransactionDate", Date),
    Column("EntityId", String),
    Column("Entity", String),
	Column("AccountId", String),
    Column("Account", String),
    Column("RefNumber", String),
    Column("Amount", Numeric(20, 4)),
    Column("Memo", String),
    Column("TimeCreated", DateTime),
    Column("TimeModified", DateTime),
    schema="prod"
)

## Create this in the main script.
# metadata_obj.create_all(engine)
