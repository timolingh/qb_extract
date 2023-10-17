from sqlalchemy import Table, Column
from sqlalchemy import String, Integer, DateTime, Date
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
tbl_bills = Table(
	"Bills",
	metadata_obj,
	Column("ID"),
	Column("VendorName"),
	Column("VendorId"),
	Column("ReferenceNumber"),
	Column("Date", Date),
	Column("Amount"),
	Column("DueDate", Date),
	Column("Terms"),
	Column("TermsId"),
	Column("AccountsPayable"),
	Column("AccountsPayableId"),
	Column("Memo"),
	Column("IsPaid"),
	Column("TimeModified", DateTime),
	Column("TimeCreated", DateTime),
	Column("OpenAmount")
				  
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


## Create this in the main script.
# metadata_obj.create_all(engine)
