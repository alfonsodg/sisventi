SISVENTI
--------

Point of Sales System with a lot of features for any usage.  Includes 
warehouse management, payable accounts and receivable accounts.

Offers a curses based sales interface and a web based administration /
operation interface.


Requirements
============

    - Unix/Linux with kernel 2.4 or above


Dependencies
============

    - Python 2.5 - 2.7
    - pymysql/MySQLdb modules


Coupons
=======

Mode 0: Applies discount to any product in the sales list
Mode 1: Applies fixed discount to all the invoice



Invoice Formatting
==================
You need to create the invoice as a text file, using the following
variables to access the internal values (field size adjustable
according to the brackets):
re.findall("\[\*.*?\*\]&*", value)
re.search("\[\*.*?\*\]&*", value).group()
re.compile("definicion").sub("mal", value)
[(elem,re.search("\[\*%s?\*\]&*" % elem, value).group()) for elem in parte]

[*ST*] = Store
[*PB*] = Payment Box
[*DA*] = Date
[*DT*] = Date and Time
[*DX*] = Document Type
[*DI*] = Document Number (ID)
[*DF*] = Document Number (FULL)
[*UI*] = User ID
[*UN*] = User Full Name
[*PI*] = Payment Method ID
[*PM*] = Payment Method Name
[*CI*] = Costumer ID
[*CN*] = Costumer Name
[*PQ*] = Product Quantity
[*PN*] = Product Name
[*PA*] = Product Amount
[*ST*] = Sub Total Value
[*T#(NAME)*] = Tax Name - Replace (NAME) with the proper value
[*T=(NAME)*] = Tax Value - Replace (NAME) with the proper value
[*FT*] = Full Total Value
[*MO*] = Money (Symbol)
[*MA*] = Money Aux (Symbol)
[*M1R*] = Money Receive Value
[*M1B*] = Money Return Value
[*M2R*] = Aux Money Receive Value
[*M2B*] = Aux Money Return Value
[*SN*] = Serial Number
[*DT*] = Distribution Type (0=None,1=Table,2=Delivery)
[*PP*] = Points Program Message
[*D1*] = Delivery Order No.
[*D2*] = Delivery Costumer
[*D3*] = Delivery Address
[*D4*] = Delivery Reference
[*D5*] = Delivery Phone


License
=======

Under GPL / v2
