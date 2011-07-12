SISVENTI
--------


Point of Sales System with a lot of features for any usage and business
needs.  Includes warehouse management, payable accounts and receivable
accounts.  All easy and fast without hard configurations or problems.

Offers a curses based sales interface and a web based administration /
operation interface for fast input.


Author
======

    Alfonso de la Guarda Reyes <alfonsodg@gmail.com>
    Lima, November 2001


Slogan
======

"Anyone can use it"


Requirements
============

    - Unix/Linux with kernel 2.4 or above
    - Hardware good for run Linux


Dependencies
============

    - Python 2.5 - 2.7
    - MySQL 5.0 or above
    - pymysql/MySQLdb modules


Features
========

    - Item Sales
    - Warehouse
    - Receipes (Product composition)
    - Payable Accounts
    - Receivable Accounts


Install
=======

- Install web2py http://www.web2py.com/examples/default/download
- Inside the applications directory clone the project branch
    ALERT: replace the sqlhtml.py included in the gluon directory for
           the provided in the branch (gluon/sqlhtml.py)
- Create the database
- Before create the tables, modify de file under models/db.py and
    change the mysql user, password and database according to your
    needs
- Start the project inside web2py, wait.... (table creation)
- Now, input demo data which contains basic configurations from
    databases/sisventi.sql
- Use the demo user and password : root/root
- The web interface offers admin features:
    http://URLWEB2PY:PORT/sisventi
- The curses interfaces are 3:
    * pysis.py - POS Sales
    * sisgerp.py - Warehouse Management
    * admin.py - POS Administration and Reports
    Adjust the data.cfg and dist.cfg according to your needs
    Just run in the terminal


Demo
====

    - Visual web-based admin / reporting:
        http://ictec.biz:8000/sisventi

    - Curses based operation modules:
        * POS ssh sales@ictec.biz  passwd: y2iCaj.
        * Warehouse ssh warehouse@ictec.biz passwd: y2iWar.


Operation
=========

    - Web interface is easy, just browse
    - Curses interface is easy too... for a product selection in the
      POS just press "space bar" and search any product (sample data
      in spanish).  For warehouse just try with the (i) or (3) options
      pressing [ENTER] most of the cases.


POS Conf
========
datos_modo = Master Sales Genere
modo_control = User Login After Sale
modo_decimal = 0:INT / 1:FLOAT
modo_almacen = Warehouse transactions
genero_producto = Master Warehouse Genere
almacen_key = Depreceated
almacen = Warehouse ID (if you need multiple warehouse just apply a
    colon , The first warehouse will be discounted)
moneda_aux = Auxiliar Money
costumer_manage = Costumer management in each operation
stock_alerta = Revisa saldo en almacen
doc_pedido = Document id por request and pre-order
cash_var = Commercial condition for sale (credit or cash)


Compositions
===========
List of Modes
1 = Sales
2 = Production


Document Types
==============
List of Modes
0 = Automatic Sales
1 = Warehouse
5 = Manual Sales


Coupons
=======

Mode 0: Applies discount to any product in the sales list
Mode 1: Applies fixed discount to all the invoice



Invoice Formatting
==================
You need to create the invoice as a text file, using the following
variables to access the internal values (field size adjustable
according to the brackets):


[*ST*] = Store
[*PB*] = Payment Box
[*DA*] = Date
[*DT*] = Date and Time
[*DX*] = Document Type
[*DI*] = Document Number (ID)
[*DP*] = Document Prefix
[*DS*] = Document Suffix
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
[*NT*] = Sub Total Value
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
[*DQ*] = Distribution Name
[*PP*] = Points Program Message
[*D1*] = Delivery Order No.
[*D2*] = Delivery Costumer
[*D3*] = Delivery Address
[*D4*] = Delivery Reference
[*D5*] = Delivery Phone
[*TD*] = Tax Debug
[*Q1*] = Coupons Codes
[*Q2*] = Coupons IDs
[*DZ*] = Distribution Type (0=None,1=Table,2=Delivery)
[*ED*] = External Document
[*VT*] = Date Sales
[*PD*] = Payment Details
[*CC*] = Comercial Condition
[*Z1*] = doccli
[*Z2*] = nomcli
[*Z3*] = dircli
[*Z4*] = refcli
[*Z5*] = telcli
[*Z6*] = texto1
[*Z7*] = texto2
[*Z8*] = texto3
[*Z9*] = norden
[*KI*] = Costumer Internal ID

Sample files:
default.txt
factura.txt


License
=======

Under GPL / v2
Propietary on demand when OSI / FSF licenses are not compatible with
    your desires
