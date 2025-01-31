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
tbl_lfg_checks = Table(
	"lfg_checks",
	metadata_obj,
	Column("ID", String),
	Column("FundingAccount", String),
	Column("FundingAccountId", String),
	Column("Payee", String),
	Column("PayeeId", String),
	Column("TransactionDate", Date),
	Column("Amount", Numeric(20, 4)),
    Column("ExpenseLineId", String),
    Column("ExpenseAccountId", String),
    Column("ExpenseAccount", String),
	Column("Memo", String),
	Column("TimeModified", DateTime),
	Column("TimeCreated", DateTime),
    schema=None	   
)

tbl_prod_lfg_checks = Table(
	"lfg_checks",
	metadata_obj,
	Column("ID", String),
	Column("FundingAccount", String),
	Column("FundingAccountId", String),
	Column("Payee", String),
	Column("PayeeId", String),
	Column("TransactionDate", Date),
	Column("Amount", Numeric(20, 4)),
    Column("ExpenseLineId", String),
    Column("ExpenseAccountId", String),
    Column("ExpenseAccount", String),
	Column("Memo", String),
	Column("TimeModified", DateTime),
	Column("TimeCreated", DateTime),
    schema="prod"	   
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

## LFG Transactions
tbl_lfg_transactions = Table(
    "lfg_transactions",
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

tbl_prod_lfg_transactions = Table(
    "lfg_transactions",
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

## LFG Invoices
tbl_lfg_invoices = Table(
    "lfg_invoices",
    metadata_obj,
    Column("ID", String),
	Column("CustomerId", String),
	Column("CustomerName", String),
	Column("AccountsReceivableId", String),
	Column("AccountsReceivable", String),
	Column("ReferenceNumber", String),
    Column("TransactionDate", Date),
	Column("DueDate", String),
	Column("Subtotal", Numeric(20, 4)),
	Column("AppliedAmount", Numeric(20, 4)),
	Column("BalanceRemaining", Numeric(20, 4)),
	Column("Memo", String),
	Column("LinkedTxnId", String),
	Column("LinkedTxnType", String),
	Column("IsPaid", String),
    Column("TimeCreated", DateTime),
    Column("TimeModified", DateTime)    
)

tbl_prod_lfg_invoices = Table(
    "lfg_invoices",
    metadata_obj,
    Column("ID", String),
	Column("CustomerId", String),
	Column("CustomerName", String),
	Column("AccountsReceivableId", String),
	Column("AccountsReceivable", String),
	Column("ReferenceNumber", String),
    Column("TransactionDate", Date),
	Column("DueDate", String),
	Column("Subtotal", Numeric(20, 4)),
	Column("AppliedAmount", Numeric(20, 4)),
	Column("BalanceRemaining", Numeric(20, 4)),
	Column("Memo", String),
	Column("LinkedTxnId", String),
	Column("LinkedTxnType", String),
	Column("IsPaid", String),
    Column("TimeCreated", DateTime),
    Column("TimeModified", DateTime),
	schema="prod"    
)

## Create this in the main script.
# metadata_obj.create_all(engine)
