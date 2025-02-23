import datetime
from lxml import etree

class TransactionQuery:
    """
    Builds the main XML to submit to QB request processor

    Attributes:
    - max_results (int): The maximum number of results to retrieve. Defaults to 0.
    - days_lookback (int): The number of days to look back for bill queries. Defaults to 0.
    - xml_root (Element): The xml root element for the bill query. 
      This is the main output from this class.
    - QuickBooks SDK online doc: https://static.developer.intuit.com/qbSDK-current/common/newosr/index.html
    - Note.  Tags must be entered in order.
   
    """

    def __init__(self, max_results: int=0, days_lookback: int=0):
        # The xml root
        self.xml_root = etree.Element("TransactionQueryRq")
        self.max_results: int = max_results
        self.days_lookback: int = days_lookback

        if self.max_results:
            max_returned = etree.SubElement(self.xml_root, "MaxReturned")
            max_returned.text = f"{self.max_results}"

        if self.days_lookback:
            start_date = (datetime.date.today() + datetime.timedelta(days=-self.days_lookback)).strftime("%Y-%m-%d")
            end_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            date_range_filter = etree.SubElement(self.xml_root, "TransactionModifiedDateRangeFilter")
            from_modified_date = etree.SubElement(date_range_filter, "FromModifiedDate")
            to_modified_date = etree.SubElement(date_range_filter, "ToModifiedDate")
            from_modified_date.text = start_date
            to_modified_date.text = end_date

        transaction_type_filter = etree.SubElement(self.xml_root, "TransactionTypeFilter")
        transaction_types = ["BillPaymentCheck", "Check", "ReceivePayment"]
        for transaction_type in transaction_types:
            txn_type_filter = etree.SubElement(transaction_type_filter, "TxnTypeFilter")
            txn_type_filter.text = transaction_type


class BillQuery:
    """

    Builds the main XML to submit to QB request processor

    Attributes:
    - max_results (int): The maximum number of results to retrieve. Defaults to 0.
    - days_lookback (int): The number of days to look back for bill queries. Defaults to 0.
    - xml_root (Element): The xml root element for the bill query. 
      This is the main output from this class.
    - QuickBooks SDK online doc: https://static.developer.intuit.com/qbSDK-current/common/newosr/index.html
    - Note.  Tags must be entered in order.
    """

    def __init__(self, max_results: int=0, days_lookback: int=0):
        # The xml root
        self.xml_root = etree.Element("BillQueryRq")
        self.max_results: int = max_results
        self.days_lookback: int = days_lookback
        
        if self.max_results:
            max_returned = etree.SubElement(self.xml_root, "MaxReturned")
            max_returned.text = f"{self.max_results}"

        if self.days_lookback:
            start_date = (datetime.date.today() + datetime.timedelta(days=-self.days_lookback)).strftime("%Y-%m-%d")
            end_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            date_range_filter = etree.SubElement(self.xml_root, "ModifiedDateRangeFilter")
            from_modified_date = etree.SubElement(date_range_filter, "FromModifiedDate")
            to_modified_date = etree.SubElement(date_range_filter, "ToModifiedDate")
            from_modified_date.text = start_date
            to_modified_date.text = end_date

        ## This filters for only CS bills.  Instead, pull all bills into the DB 
        # account_filter = etree.SubElement(self.xml_root, "AccountFilter")
        # af_listid = etree.SubElement(account_filter, "ListID")
        # af_listid.text = "800001BC-1447797951" 
 
        paid_status = etree.SubElement(self.xml_root, "PaidStatus")
        paid_status.text = "All"

        # Linked transactions
        include_linked_txns = etree.SubElement(self.xml_root, "IncludeLinkedTxns")
        include_linked_txns.text = "true"

class CheckQuery:
    def __init__(self, max_results: int=0, days_lookback: int=0):
        # The xml root
        self.xml_root = etree.Element("CheckQueryRq")
        self.max_results: int = max_results
        self.days_lookback: int = days_lookback

        if self.max_results:
            max_returned = etree.SubElement(self.xml_root, "MaxReturned")
            max_returned.text = f"{self.max_results}"

        if self.days_lookback:
            start_date = (datetime.date.today() + datetime.timedelta(days=-self.days_lookback)).strftime("%Y-%m-%d")
            end_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            date_range_filter = etree.SubElement(self.xml_root, "ModifiedDateRangeFilter")
            from_modified_date = etree.SubElement(date_range_filter, "FromModifiedDate")
            to_modified_date = etree.SubElement(date_range_filter, "ToModifiedDate")
            from_modified_date.text = start_date
            to_modified_date.text = end_date

        # Include line items
        include_line_items = etree.SubElement(self.xml_root, "IncludeLineItems")
        include_line_items.text = "true"

        # Linked transactions
        include_linked_txns = etree.SubElement(self.xml_root, "IncludeLinkedTxns")
        include_linked_txns.text = "true"

class InvoiceQuery:
    def __init__(self, max_results: int=0, days_lookback: int=0):
        # The xml root
        self.xml_root = etree.Element("InvoiceQueryRq")
        self.max_results: int = max_results
        self.days_lookback: int = days_lookback
        
        if self.max_results:
            max_returned = etree.SubElement(self.xml_root, "MaxReturned")
            max_returned.text = f"{self.max_results}"

        if self.days_lookback:
            start_date = (datetime.date.today() + datetime.timedelta(days=-self.days_lookback)).strftime("%Y-%m-%d")
            end_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            date_range_filter = etree.SubElement(self.xml_root, "ModifiedDateRangeFilter")
            from_modified_date = etree.SubElement(date_range_filter, "FromModifiedDate")
            to_modified_date = etree.SubElement(date_range_filter, "ToModifiedDate")
            from_modified_date.text = start_date
            to_modified_date.text = end_date
 
        paid_status = etree.SubElement(self.xml_root, "PaidStatus")
        paid_status.text = "All"

        # Linked transactions
        include_linked_txns = etree.SubElement(self.xml_root, "IncludeLinkedTxns")
        include_linked_txns.text = "true"

class QbResp:

    """
    Represents a QuickBooks Response handler.

    Attributes:
    - raw_data (dict): The raw response data received.
    - response_spec (dict): Specification for transforming the raw data.
    - transformed_data (list): Transformed data based on the response specification.

    Methods:
    - transform_data(): Transforms the raw data based on the specified mapping.
    - enh_get(row_data: dict, map_key: str) -> Union[str, int, float, None]: 
        Static method to safely retrieve nested dictionary values.
    - bill_response(data): Class method to generate a response with predefined specifications.
    """

    def __init__(self, raw_data: dict, response_spec: dict = {}) -> None:
        self.raw_data = raw_data
        self.response_spec = response_spec
        self.exploded_data = []
        self.transformed_data = []

    def explode_data(self, key_to_explode) -> list[dict]:
        response_tag = self.response_spec.get("response_tag")
        records_tag = self.response_spec.get("records_tag")

        if self.raw_data.get(response_tag).get('@statusMessage').lower() == 'status ok':
            rows = self.raw_data.get(response_tag).get(records_tag)
            for row in rows:
                row_data = {}
                if not(isinstance(row.get(key_to_explode), list)):
                    for key, val in row.items():
                        row_data[key] = val
                    self.exploded_data.append(row_data)
                else:
                    for split_item in row.get(key_to_explode):
                        for key, val in row.items():
                            row_data[key] = val
                        row_data[key_to_explode] = split_item
                        self.exploded_data.append(row_data)

        return self.exploded_data    

    def transform_data(self) -> list[dict]:
        response_tag = self.response_spec.get("response_tag")
        records_tag = self.response_spec.get("records_tag")

        if self.raw_data.get(response_tag).get('@statusMessage').lower() == 'status ok':
            if len(self.exploded_data) > 0:
                self.raw_data[records_tag] = self.exploded_data
            rows = self.raw_data.get(response_tag).get(records_tag)
            for row in rows:
                field_map = self.response_spec.get("field_map")
                row_dict = {}

                for orig_field in field_map.keys():
                    val = self.enh_get(row, orig_field)
                    new_key = field_map.get(orig_field)
                    row_dict[new_key] = val

                self.transformed_data.append(row_dict)
    
        return self.transformed_data
    
    @staticmethod
    def enh_get(row_data: dict, map_key: str) -> str | int | float | None:
        keys = map_key.split(".")
        data = row_data
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key)
            else:
                data = None

        return data
    
    @classmethod
    def bill_response(cls, data):
        response_spec = {
            "response_tag": "BillQueryRs",
            "records_tag": "BillRet",
            "field_map": {
                "TxnID": "ID",
                "VendorRef.ListID": "VendorId",
                "VendorRef.FullName": "VendorName",
                "APAccountRef.ListID": "AccountsPayableId",
                "APAccountRef.FullName": "AccountsPayable",
                "RefNumber": "ReferenceNumber",
                "TxnDate": "Date",
                "DueDate": "DueDate",
                "AmountDue": "OpenAmount",
                "TermsRef.ListID": "TermsId",
                "TermsRef.FullName": "Terms",
                "Memo": "Memo",
                "LinkedTxn.TxnID": "LinkedTxnId",
                "LinkedTxn.TxnType": "LinkedTxnType",
                "IsPaid": "IsPaid",
                "TimeCreated": "TimeCreated",
                "TimeModified": "TimeModified"
            }
        }

        return cls(data, response_spec)

    @classmethod
    def transaction_response(cls, data):
        response_spec = {
            "response_tag": "TransactionQueryRs",
            "records_tag": "TransactionRet",
            "field_map": {
                "TxnID": "ID",
                "TxnType": "TransactionType",
                "TxnDate": "TransactionDate",
                "EntityRef.ListID": "EntityId",
                "EntityRef.FullName": "Entity",
                "AccountRef.ListID": "AccountId",
                "AccountRef.FullName": "Account",
                "RefNumber": "RefNumber",
                "Amount": "Amount",
                "Memo": "Memo",
                "TimeCreated": "TimeCreated",
                "TimeModified": "TimeModified"
            }
        }

        return cls(data, response_spec)

    @classmethod
    def invoice_response(cls, data):
        response_spec = {
            "response_tag": "InvoiceQueryRs",
            "records_tag": "InvoiceRet",
            "field_map": {
                "TxnID": "ID",
                "CustomerRef.ListID": "CustomerId",
                "CustomerRef.FullName": "CustomerName",
                "ARAccountRef.ListID": "AccountsReceivableId",
                "ARAccountRef.FullName": "AccountsReceivable",
                "RefNumber": "ReferenceNumber",
                "TxnDate": "TransactionDate",
                "DueDate": "DueDate",
                "Subtotal": "Subtotal",
                "AppliedAmount": "AppliedAmount",
                "BalanceRemaining": "BalanceRemaining",
                # "AmountDue": "OpenAmount",
                # "TermsRef.ListID": "TermsId",
                # "TermsRef.FullName": "Terms",
                "Memo": "Memo",
                "LinkedTxn.TxnID": "LinkedTxnId",
                "LinkedTxn.TxnType": "LinkedTxnType",
                "IsPaid": "IsPaid",
                "TimeCreated": "TimeCreated",
                "TimeModified": "TimeModified"
            }
        }

        return cls(data, response_spec)

    @classmethod
    def check_response(cls, data):
        response_spec = {
            "response_tag": "CheckQueryRs",
            "records_tag": "CheckRet",
            "field_map": {
                "TxnID": "ID",
                "AccountRef.ListID": "FundingAccountId",
                "AccountRef.FullName": "FundingAccount",
                "PayeeEntityRef.ListID": "PayeeId",
                "PayeeEntityRef.FullName": "Payee",
                "TxnDate": "TransactionDate",
                "Amount": "Amount",
                # "ExpenseLineRet.TxnLineID": "ExpenseLineId",
                # "ExpenseLineRet.AccountRef.ListID": "ExpenseAccountId",
                # "ExpenseLineRet.AccountRef.FullName": "ExpenseAccount",
                "TimeCreated": "TimeCreated",
                "TimeModified": "TimeModified"
            }
        }
        return cls(data, response_spec)
    
    @classmethod
    def expense_response(cls, data):
        response_spec = {
            "response_tag": "CheckQueryRs",
            "records_tag": "CheckRet",
            "field_map": {
                "ExpenseLineRet.TxnLineID": "ID",
                "TxnID": "LinkedTxnID",
                "PayeeEntityRef.ListID": "PayeeId",
                "PayeeEntityRef.FullName": "Payee",
                "TxnDate": "TransactionDate",
                "ExpenseLineRet.AccountRef.ListID": "ExpenseAccountId",
                "ExpenseLineRet.AccountRef.FullName": "ExpenseAccount",
                "Amount": "Amount",
                "Memo": "Memo",
                "TimeCreated": "TimeCreated",
                "TimeModified": "TimeModified"
            }
        }
        return cls(data, response_spec)





    
   

    
                




        
            

