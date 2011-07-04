#!/usr/bin/env python


#####
#Call external functions.  The CompatMysqldb was added to the original pacakage, read the installation procedures.
#####
import curses # manages the windows
import time # manages the time
import string # manages the strings
import os # manages the os
import MySQLdb # manages the MySQL DB
import sys
import re
import signal
import types
#import traceback
import fpformat
import locale
import calendar
import md5
import logging
#import tarfile
#import zipfile
#import glob
from curses import panel
#####

#####
signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGTSTP, signal.SIG_IGN)
signal.signal(signal.SIGABRT, signal.SIG_IGN)
#####
logging.basicConfig(filename='sisventi.log', level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')
#####
#Read the db.cfg file (variables for assign the POS and MySQL DB values)
#####
try:
    in_file=open("dist.cfg","r") # Opens the file
    params=in_file.read().splitlines()
    portimp=params[0]
    empresa=params[1]
    host=params[2] # Start of the DB data, this line assigns the second value to the host variable
    data=params[3] # Same (explanation) as above
    user=params[4]
    pswd=params[5]
    in_file.close() # close the file
except IOError:
    print 'Error al abrir el archivo de configuracion!!!!'
    sys.exit(0)
#####
posn=1
cajn=1

#####
#Initialize Variables and Functions
#####
try:
    conn=MySQLdb.connect(db=data,host=host,user=user,passwd=pswd) # Starts the MySQL DB connection
except:
    print 'Error al conectarse con la base de datos!!!!'
    sys.exit()
conn.autocommit(True)
curs = conn.cursor()
stdscr=curses.initscr() # Initialize the call to the curses function
#curses.curs_set(0) # Assigns an invisible cursor (values goes from 0 to 2)
curses.start_color() # Initialize the color access
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # Assigns the color to the screen
curses.mousemask(curses.ALL_MOUSE_EVENTS) # Calls to the detection of mouse events (moves and clicks)
curses.noecho() # No returns a  character after a keypress
#curses.cbreak() # Read a character one by one
#stdscr.keypad(1) # Recognition of all the keys
stdscr.leaveok(0) # Reduces cursor movement
maxy,maxx=stdscr.getmaxyx() # Obtains the screen dimensions
loc=locale.setlocale(locale.LC_ALL,'')
#####
nomven='I'
fechmu=time.strftime("%Y-%m-%d")



#####
#Checks the proper resolution.  We need al least, 80 characters for 24 lines
#####
if maxy < 24 or maxx < 80:
    curses.echo()
    curses.endwin()
    print "Error!....."
    print "Resolution Error"
    print "Needed at least:"
    print "80 chars x 24 lines"
    sys.exit()


##Build the Panels
def mkpanel(color, rows, cols, tly, tlx):
    win = curses.newwin(rows, cols, tly, tlx)
    pan = panel.new_panel(win)
    if curses.has_colors():
        if color == curses.COLOR_BLUE:
            fg = curses.COLOR_WHITE
        else:
            fg = curses.COLOR_BLACK
        bg=color
        curses.init_pair(color, color, curses.COLOR_BLACK)
        win.bkgdset(ord(' '), curses.color_pair(color))
    else:
        win.bkgdset(ord(' '), curses.A_BOLD)
    return pan


##User Authorization Routine
def aut():
    """
    Authorization scheme
    """
    curses.curs_set(1)
    updat()
    pan = mkpanel(curses.COLOR_WHITE, maxy, maxx, 0, 0)
    win = definewin(pan,0,1)
    msg = "Modulo: Almacenes"
    posx = centrar(maxx, msg)
    win.addstr(1, posx, msg)
    win.addstr(maxy / 2 - 2, maxx / 2 - 10, "Usuario: ")
    curses.echo()
    while 1:
        updat()
        user_ing = win.getstr(maxy / 2 - 2, maxx / 2, 15)
        if user_ing != "":
            break
    win.addstr(maxy / 2 - 1, maxx / 2 - 10, "Password: ")
    curses.noecho()
    while 1:
        pwd_ing = win.getstr(maxy / 2 - 1, maxx / 2, 15)
        if pwd_ing != "":
            break
    pwd_ing = md5.new(pwd_ing).hexdigest()
    sql = """select user.first_name,user.last_name,level.group_id,
        user.id from auth_user user, auth_membership level where
        user.id=level.user_id and user.username='%s' and
        user.password='%s'""" % (user_ing, pwd_ing)
    cnt, rso = query(sql, 0)
    if cnt > 0:
        nombre = "%s %s" % (rso[0], rso[1])
        nombre = nombre[:20]
        nivel_usuario = rso[2]
        id_usuario = rso[3]
        curses.curs_set(0)
        updat()
        return user_ing, nombre, nivel_usuario, id_usuario
    else:
        curses.curs_set(0)
        updat()
        return 0, 'I', 0, 0



##Aligns to right any phrase
def derecha(x,fra):
    posx=x-len(fra)
    return posx


##Aligns to center any phrase
def centrar(x,fra):
    posx=(x/2)-(len(fra)/2)
    return posx


##Do the Query, sending 1 or Multiple results
def query(sql,ndat=1):
    if ndat==5:
        try:
            curs.execute("START TRANSACTION")
            for query in sql:
                curs.execute(query)
            curs.execute("COMMIT")
            return 1
        except MySQLdb.Error,  error:
            curs.execute("ROLLBACK")
            segur("""ERROR. INFORMACION NO 
                REGISTRADA.""")
            logging.debug("Query: %s" % error)
            logging.debug("Query-Detail: %s" % sql)
            return -1
    else:
        try:
            cmd=curs.execute(sql)
            cnt=curs.rowcount
            if ndat==0:
                rso=curs.fetchone()
            else:
                rso=curs.fetchall()
            return cnt,rso
        except MySQLdb.Error, error:
            return -1,error.args[1]
        except:
            return -1,sql


##Builds the Main Menu
def menu(menudata,head=''):
    pan=mkpanel(curses.COLOR_YELLOW,maxy,maxx,0,0)
    datatemp=string.split(menudata,'|')
    opciones={}
    win=definir(pan)
    texto='MENU '+str(head)
    posx=centrar(maxx,texto)
    win.addstr(2,posx,texto)
    texto='----'
    posx=centrar(maxx,texto)
    win.addstr(3,posx,texto)
    cnt=6
    for linea in datatemp:
        dato=string.split(linea,'.')[0]
        dato_tmp,tipo=expresion(dato)
        if tipo=='entero':
            elemento=int(dato)
        else:
            elemento=str(dato)
        valor=ord(dato)
        if not opciones.has_key(valor):
            opciones[valor]=elemento
        posx=centrar(maxx,linea)
        win.addstr(cnt,posx,linea)
        cnt+=1
    updat()
    seleccion=obtc(pan,opciones)
    return seleccion


##Double Function: Gets a Key or Gets an Option
def obtc(pan,opciones={}):
    control={259:'arriba',258:'abajo',331:'insert',10:'enter',27:'escape'}
    for llave in control:
        if not opciones.has_key(llave):
            opciones[llave]=control[llave]
    win=pan.window()
    curses.noecho()
    win.keypad(1)
    while 1:
        c=win.getch()
        if opciones.has_key(c):
            return opciones[c]


##Gets a Key
def obch(pan,pcy=0,pcx=0,estado='n',tipo=0):
    win=pan.window()
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    updat()
    while 1:
        if estado=='v':
            curses.echo()
            curses.curs_set(1)
            updat()
        c=win.getch(pcy,pcx)
        curses.noecho()
        curses.curs_set(0)
        updat()
        if c==curses.KEY_UP and tipo==0:return 'arriba'
        if c==curses.KEY_DOWN and tipo==0:return 'abajo'
        if c==curses.KEY_LEFT  and tipo==0:return 'izquierda'
        if c==curses.KEY_RIGHT  and tipo==0:return 'derecha'
        if c==curses.KEY_BACKSPACE or c==127:return 'backspace'
        if c==10:return 'enter'
        if c==curses.KEY_IC  and tipo==0:return 'insert'
        if c==curses.KEY_DC  and tipo==0:return 'borrar'
        if c==curses.KEY_NPAGE  and tipo==0:return 'spag'
        if c==curses.KEY_PPAGE  and tipo==0:return 'ppag'
        if c==27:return 'escape'
        if (c>47 and c<58) or (c>64 and c<91) or (c>96 and c<123) or c==32 or c==46 or c==45:return chr(c) # retorna numero o letra en mayusculas o minusculas


##Cleans Any Window
def limpiar(pan):
    win=pan.window()
    win.erase()
    updat()
    return


##Defines Any Window
def definir(pan):
    win=pan.window()
    win.erase()
    win.border()
    updat()
    return win


##Refresh Any Window
def updat():
    panel.update_panels()
    curses.doupdate()
    return


##Fills decimals
def cardec(dato,precision=2):
    if type(dato) is types.FloatType:
        dato=round(dato,precision)
        dato=fpformat.fix(dato,precision)
        return str(dato)
    else:
        return str(dato)


##Currency
def tipos_cambio(fecha):
    sql="select valor from tipos_cambio where fecha='"+str(fecha)+"' or fecha='0000-00-00' order by fecha desc limit 1"
    cuenta,resultado=query(sql,0)
    if cuenta==0:
        data=1
    else:
        data=resultado[0]
    return round(float(data),2)


##Selection of Options
def seleccion(cadena,cuenta,campos,rotulo,identif,posy,posx):
    temprom=0
    posdata={}
    datay=[]
    orden=[]
    for w in range(0,cuenta):
        datay=[]
        for z in range(0,campos):
            temprom+=len(str(cadena[w][z]))
            datay.append(str(cadena[w][z]))
        posdata[w]=datay
    if posy==-1:
        tny=cuenta+2
        posy=(maxy-tny)/2
    if posx==-1:
        tnx=(temprom/campos)+2
        posx=(maxx-tnx)/2
    tamy=cuenta+2
    tamx=(temprom/campos)+2
    pan=mkpanel(curses.COLOR_WHITE,tamy,tamx,posy,posx)
    win=definir(pan)
    posicion=0
    orden=posdata.keys()
    orden.sort()
    while 1:
        for w in orden:
            if w==posicion:
                win.addstr(1+w,1,posdata[w][rotulo],curses.A_REVERSE)
            else:
                win.addstr(1+w,1,posdata[w][rotulo])
        opcn=obtc(pan)
        if opcn=='arriba':
            if posicion==0:
                posicion=0
            else:
                posicion=posicion-1
        if opcn=='abajo':
            if posicion==(cuenta-1):
                posicion=(cuenta-1)
            else:
                posicion=posicion+1
        if opcn=='enter':
            return posdata[posicion][rotulo],posdata[posicion][identif]
        if opcn=='escape':
            return 'Anular','Anular'


def poscr(tamwin,tamscr):
    datoscr=(tamscr-tamwin)/2
    return datoscr


def ladocl(data,titulo='',key_val=0,dsc_val=1):
    if len(data)<=0:
        return 'Anular','Anular'
    lineas=[]
    temporal=[]
    for parte in data:
        datos=[]
        datos.append(str(parte[key_val]))
        datos.append(str(parte[dsc_val]))
        temporal.append(len(str(parte[key_val])+'->'+str(parte[dsc_val])))
        lineas.append(datos)
    cuenta=len(lineas)
    sizex=max(temporal)+2
    if sizex>maxx:
        sizex=maxx
    temporal=[]
    if cuenta>=(maxy-2):
        sizey=maxy
        inic_y=0
        term_y=maxy-2
    else:
        sizey=cuenta+2
        inic_y=0#Inicio de Array
        term_y=cuenta #Termino de Array
    posy=poscr(sizey,maxy)
    posx=poscr(sizex,maxx)
    panel=mkpanel(curses.COLOR_YELLOW,sizey,sizex,posy,posx)
    win=definewin(panel,0,1)
    win.addstr(0,1,titulo,curses.A_BOLD)
    sely=1
    while 1:
        py=0
        for cnt in range(inic_y,term_y):
            contenido=lineas[cnt][0]+'->'+lineas[cnt][1]
            py+=1
            condicion=curses.A_NORMAL
            win.addstr(py,1,' '*(sizex-2),condicion)
            if py==sely:
                condicion=curses.A_REVERSE
                valor1=lineas[cnt][0]
                valor2=lineas[cnt][1]
            win.addstr(py,1,str(contenido),condicion)
            updat()
#       opcion=obtc(panel,{ord('n'):'n'})
        opcion=obch(panel)
        if opcion=='arriba':
            if sely>1:
                sely-=1
            else:
                if inic_y>0:
                    sely=1
                    inic_y-=1
                    term_y-=1
        elif opcion=='abajo':
            if sely<sizey-2:
                sely+=1
            else:
                if term_y<cuenta:
                    sely=sizey-1
                    inic_y+=1
                    term_y+=1
        elif opcion=='escape':
            valor1,valor2='Anular','Anular'
            break
        elif opcion=='enter':
            break
        elif opcion=='insert':
            valor_tmp=valor1
            valor1,valor2='insertar',valor_tmp
            break
        elif opcion=='n':
            valor_tmp=valor1
            valor1,valor2='agregar',valor_tmp
            break
    return valor1,valor2


##Prints Strings in Window
def strimpr(texto,py,tx,ubicacion='c'):
    texto=str(texto)
    if ubicacion=='c' or ubicacion=='centrar' or ubicacion=='centro':
        px=centrar(tx,texto)
    else:
        px=derecha(tx,texto)
    win.addstr(py,px,texto)
    return


##Simple true/false question
def segur(msg,posy=-1,posx=-1):
    cuenta=len(msg)+3
    tny=3
    if posy==-1:
        posy=(maxy-tny)/2
    if posx==-1:
        tnx=cuenta
        posx=(maxx-tnx)/2
    pan=mkpanel(curses.COLOR_WHITE,tny,cuenta,posy,posx)
    win=definir(pan)
    win.addstr(1,1,msg)
    updat()
    while 1:
        curses.curs_set(1)
        curses.echo()
        updat()
        resp=win.getch()
        curses.noecho()
        curses.curs_set(0)
        updat()
        if resp==ord('s'):
            return 'si'
        elif resp==ord('n'):
            return 'no'
        elif resp==ord('m'):
            return 'manana'
        elif resp==ord('t'):
            return 'tarde'
        elif resp==ord('i'):
            return 'interno'
        elif resp==ord('o'):
            return 'otros'
        elif resp==ord('g'):
            return 'grabar'
        elif resp==27:
            return 'Anular'
        else:
            return 'exit'


##WareHouse Report
def almacen(apertura,cierre='4',modo=0):
    lineas=[]
    relalm={}
    if modo==5:
        condtiempo=apertura
        parte=float(cierre)
    else:
        condtiempo="a.tiempo>='"+apertura+"' and a.tiempo<='"+cierre+"'"
    sql="select a.codigo,a.precio,sum(a.cantidad),concat(b.nombre,'/',b.descripcion),c.codigo,concat(d.nombre,'/',d.descripcion),c.cantidad,sum(a.cantidad)*c.cantidad from docventa as a,variable as b,listas as c,variable as d where a.codigo=b.codbarras and a.codigo=c.codbarras and c.codigo=d.codbarras and a.estado='B' and "+condtiempo+" and a.pv='"+str(posn)+"' and a.caja='"+str(cajn)+"' and c.nivel=0 group by a.codigo,c.codigo order by a.codigo,c.codigo"
    cuenta,resultado=query(sql)
    for x in range(0,cuenta):
        codigobase=resultado[x][4]
        acumulado=resultado[x][7]
        if relalm.has_key(codigobase):
            provisional=relalm[codigobase]
            del relalm[codigobase]
            relalm[codigobase]=provisional+acumulado
        else:
            relalm[codigobase]=acumulado
    orden=relalm.keys()
    orden.sort()
    for codigob in orden:
        n=0
        for x in range(0,cuenta):
            codigoventas=resultado[x][0]
            precioventa=resultado[x][1]
            cantidadven=resultado[x][2]
            nombreprven=resultado[x][3]
            codigobase=resultado[x][4]
            nombrebase=resultado[x][5][:15]
            cantidbase=resultado[x][6]
            if codigobase==codigob:
                if n==0:
                    if modo==1:
                        prov=agregar_valores([],0,codigob,nombrebase,relalm[codigob])
                        lineas.append(prov)
                        prov=[]
                        prov.append('================================================================')
                        lineas.append(prov)
                        n=1
                    elif modo==0:
                        prov=agregar_valores([],0,codigob,relalm[codigob],nombrebase)
                        lineas.append(prov)
                        n=1
                    elif modo==2:
                        if prodkey.count(codigob)>0:
                            prov=agregar_valores([],0,codigob,relalm[codigob],nombrebase)
                            lineas.append(prov)
                            n=1
                    elif modo==3:
                        if prodkey.count(codigob)>0:
                            prov=agregar_valores([],0,codigob,nombrebase,relalm[codigob])
                            lineas.append(prov)
                            prov=[]
                            prov.append('================================================================')
                            lineas.append(prov)
                            n=1
                    elif modo==5:
                        if prodkey.count(codigob)>0:
                            cantid=float(relalm[codigob])
                            prov=agregar_valores([],0,codigob,cantid,round(cantid/parte),nombrebase)
                            lineas.append(prov)
                            n=1
                if modo==1:
                    prov=agregar_valores([],0,codigoventas,nombreprven,'',cantidadven)
                    lineas.append(prov)
                elif modo==3:
                    if prodkey.count(codigob)>0:
                        prov=agregar_valores([],0,codigoventas,nombreprven,'',cantidadven)
                        lineas.append(prov)
            if x==(cuenta-1):
                if modo==1:
                    for paso in range(0,3):
                        prov=[]
                        prov.append('>---<')
                        lineas.append(prov)
                elif modo==3:
                    if prodkey.count(codigob)>0:
                        for paso in range(0,3):
                            prov=[]
                            prov.append('>---<')
                            lineas.append(prov)
    return lineas


##Prints line into file (text)
def linea(archivo):
    archivo.write('\n')
    return


##Send to Printer
def impresion(nomarch,gaveta):
    pass
    return


##Adds 0 into Decimal Strings
def digit(texto):
    texto=str(texto)
    texto=fpformat.fix(texto,2)
    return texto


##View Cursor from Window
def vc():
    curses.curs_set(1)
    curses.echo()
    updat()
    return


##Hide Cursor from Window
def ec():
    curses.curs_set(0)
    curses.noecho()
    updat()
    return


def definewin(pan,optam=1,opbox=1):
    win=pan.window()
    if opbox == 1:
        win.erase()
        win.box()
    updat()
    if optam==1:
        tamy,tamx=win.getmaxyx()
        return win,tamy,tamx
    else:
        return win


def ingresodato(msg,pan,tamx=20,texto='',tipo=0,clr=0):
    texto = "%s" % texto
    ubicx=len(msg)+3
    tmax=tamx+ubicx
    txtp=0
    if len(texto)>0:
        codobt=texto
        txtp=1
    else:
        codobt=''
    win=definir(pan)
    tmy,tmx=win.getmaxyx()
    win.addstr(1,1,msg+': ',curses.A_UNDERLINE)
    while 1:
        if ubicx>=tmx:
            ubicx=len(msg)+3
        updat()
        if txtp==1:
            win.addstr(1,ubicx,codobt)
            ubicx=ubicx+len(codobt)
            txtp=0
        caracter=obch(pan,1,ubicx,'v',tipo)
        if caracter=='enter':
            if clr==1:
                win.erase()
            return codobt
        elif caracter=='escape':
            return 'Anular'
        elif caracter=='arriba' and tipo==0:
            return 'arriba'
        elif caracter=='abajo' and tipo==0:
            return 'abajo'
        elif caracter=='insert' and tipo==0:
            return 'insert'
        elif caracter=='spag' and tipo==0:
            return 'spag'
        elif caracter=='ppag' and tipo==0:
            return 'ppag'
        if caracter=='backspace':
            ubicx-=1
            if ubicx<=len(msg)+3:
                ubicx=len(msg)+3
            codobt=codobt[:-1]
            win.addstr(1,ubicx,'   ')
            caracter=''
        if (caracter>='0' and caracter<='9') or (caracter>='a' and caracter<='z') or (caracter>='A' and caracter<='Z') or (caracter=='-') or (caracter=='.'):
            ubicx+=1
            codobt+=str(caracter)
            if ubicx >=(tmax):
                ubicx=tmax
                codobt=codobt[:tamx]


def viewtext(texto,pan,psey=0,modo='t'):
    cnt=0
    py=0
    win=definir(pan)
    maxy,maxx = win.getmaxyx()
    lineas=len(texto)
    if lineas>(maxy-2):
        cnt=lineas-(maxy-2)
    if psey>0:
        cnt+=psey
    elif psey<0:
        cnt+=psey
        lineas+=psey
    campos={}
    for elem in texto:
        for posic in range(0,len(elem)):
            if campos.has_key(posic):
                if campos[posic]<len(str(elem[posic])):
                    campos[posic]=len(str(elem[posic]))
            else:
                campos[posic]=len(str(elem[posic]))
    for a in range(cnt,lineas):
        temporal=texto[a]
        py+=1
        ubx=1
        px=0
        if len(temporal)>0:
            for b in range(0,len(temporal)):
                if modo=='t':
                    px=ubx+(b*(maxx/len(temporal)))
                else:
                    if b>=1:
                        px+=2+campos[b-1]
                    else:
                        px+=1
                win.addstr(py,px,str(temporal[b]))
                updat()
    return


def sqlsend(texto,campos,tipo=0):
    sq=''
    p1=''
    partes=string.split(campos,',')
    for b in range(0,len(partes)):
        if tipo==0:
            sq+=(str(partes[b])+"='"+str(texto[b])+"',")
        else:
            p1+=("'"+str(texto[b])+"',")
    sq=sq[:-1]
    p1=p1[:-1]
    if tipo==0:
        cadena=sq
    else:
        cadena="("+campos+") values ("+p1+")"
    return cadena


def winhead(texto,pan):
    win=definir(pan)
    maxy,maxx = win.getmaxyx()
    px=centrar(maxx,texto)
    win.addstr(1,px,texto)
    updat()
    return


def win_def(txt_fld=2,maxy=24,maxx=80):
    panel_top=mkpanel(curses.COLOR_WHITE,3,maxx,0,0)
    panel_text_1=mkpanel(curses.COLOR_WHITE,3,20,3,0)
    mid_sizey=6
    if txt_fld==2.5:
        panel_text_2=mkpanel(curses.COLOR_WHITE,3,40,3,20)
    else:# txt_fld==2:
        panel_text_2=mkpanel(curses.COLOR_WHITE,3,20,3,20)
    if txt_fld>=3:
        panel_text_3=mkpanel(curses.COLOR_WHITE,3,20,3,40)
        panel_text_4=mkpanel(curses.COLOR_WHITE,3,20,3,60)
    if txt_fld==8:
        panel_text_5=mkpanel(curses.COLOR_WHITE,3,20,6,0)
        panel_text_6=mkpanel(curses.COLOR_WHITE,3,20,6,20)
        panel_text_7=mkpanel(curses.COLOR_WHITE,3,20,6,40)
        panel_text_8=mkpanel(curses.COLOR_WHITE,3,20,6,60)
        mid_sizey=9
    panel_mid=mkpanel(curses.COLOR_WHITE,maxy-mid_sizey,maxx,mid_sizey,0)
    if txt_fld==1:
        return panel_top,panel_text_1,panel_mid
    elif txt_fld==2 or txt_fld==2.5:
        return panel_top,panel_text_1,panel_text_2,panel_mid
    elif txt_fld==3:
        return panel_top,panel_text_1,panel_text_2,panel_text_3,panel_mid
    elif txt_fld==4:
        return panel_top,panel_text_1,panel_text_2,panel_text_3,panel_text_4,panel_mid
    elif txt_fld==8:
        return panel_top,panel_text_1,panel_text_2,panel_text_3,panel_text_4,panel_text_5,panel_text_6,panel_text_7,panel_text_8,panel_mid


def borscr(*paneles):
    for panel in paneles:
        win=definir(panel)
        win.erase()
#       panel.hide()
        updat()
    return


def expresion(dato):
    dato=str(dato)
    decimal=re.search('^\d+\.\d+$',dato)
    entero=re.search('^\d+$',dato)
    caracter=re.search('^\D+$',dato)
    alfanumerico=re.search('^[a-zA-Z0-9-.]+$',dato)
    if decimal:
        dato=float(decimal.group(0))
        dato=round(dato,2)
        return dato,'decimal'
    if entero:
        dato=entero.group(0)
        return dato,'entero'
    if caracter:
        dato=caracter.group(0)
        return dato,'caracter'
    if alfanumerico:
        dato=alfanumerico.group(0)
        return dato,'alfanumerico'
    return 'nulo','nulo'


def fecha_ing(modo=1,tipo_msj='n'):
    fecha_base=[]
    mensaje='Fecha (AAMMDD)'
    ventana=''
    for cnt in range(1,modo+1):
        if cnt==1:
            if modo==1:
                tam_x=25
            else:
                tam_x=20
            panel_1=mkpanel(curses.COLOR_WHITE,3,tam_x,0,0)
            ventana=panel_1
            if tipo_msj=='n':
                mensaje='Fecha Ini'
            elif tipo_msj=='b':
                mensaje='Fecha Vta'
        elif cnt==2:
            panel_2=mkpanel(curses.COLOR_WHITE,3,20,0,20)
            ventana=panel_2
            if tipo_msj=='n':
                mensaje='Fecha Fin'
            elif tipo_msj=='b':
                mensaje='Fecha Dep'
        elif cnt==3:
            panel_3=mkpanel(curses.COLOR_WHITE,3,20,0,40)
            ventana=panel_3
        elif cnt==4:
            panel_4=mkpanel(curses.COLOR_WHITE,3,20,0,60)
            ventana=panel_4
        while 1:
            date_stat=0
            if tipo_msj=='i':
                mensaje=mensaje+str(cnt)
            fech_ing=ingresodato(mensaje,ventana,15,'',0,0)
            if fech_ing=='Anular':
                if cnt==1:
                    return 'Anular'
                else:
                    return 'Anular','Anular'
            elif fech_ing=='':
                fech_ing=time.strftime("%Y-%m-%d")
                date_stat=1
            valor,tipod=expresion(fech_ing)
            if len(fech_ing)==6 and tipod=='entero':
                dia=int(fech_ing[4:6])
                fech_ing='20'+fech_ing[0:2]+'-'+fech_ing[2:4]+'-'+fech_ing[4:6]
                dia_cmp=calendar.monthrange(int(fech_ing[0:2]),int(fech_ing[2:4]))
                dia_valid=(int(dia_cmp[1]+1))
                if dia<=dia_valid:
                    date_stat=1
            if date_stat==1 and fecha_base.count(fech_ing)==0:
                fecha_base.append(fech_ing)
                break
    if modo==1:
        return fecha_base[0]
    else:
        return fecha_base


def datesp(titulo,panel,carac,condicion,dato='',tipo=0,clr=0):
    cond=string.split(condicion,',')
    while 1:
        provis=ingresodato(titulo,panel,carac,dato,tipo,clr)
        if provis=='':
            cantp=len(cond)
            if cond[cantp-1]=='vacio':
                cantidad=0
                return cantidad
        tipoc=''
        temp=expresion(provis)
        if len(temp)>0:
            tipoc=temp[1]
            for a in range(0,len(cond)):
                if tipoc==cond[a]:
                    cantidad=provis
                    return cantidad


def datopc(titulo, panel, num_char, valid_keys, valid_data_types,
    sql_cond=''):
    """
    Inputs DATA
    """
    sql_layout = """select if(length(mae.alias)>0,mae.alias,
        concat(mae.nombre,' ',mae.descripcion)) from maestro
        mae where mae.id='%s' %s"""
    if len(sql_cond) > 0:
        sql_cond = "and %s" % sql_cond
    cond1=string.split(valid_keys,',')
    cond2=string.split(valid_data_types,',')
    while 1:
        ingdat = ingresodato(titulo, panel, num_char, '', 0, 0)
        for opc in cond1:
            if ingdat == opc:
                return ingdat,0
        sql = sql_layout % (ingdat, sql_cond)
        cuenta,resultado=query(sql,0)
        if cuenta>0:
            win=definewin(panel,0,0)
            win.addstr(1,len(titulo)+3,' '*num_char)
            win.addstr(1,len(titulo)+3,ingdat)
            return ingdat,1
        tipoc=''
        temp=expresion(ingdat)
        if len(temp)>0:
            tipoc=temp[1]
            for opc in cond2:
                if tipoc == opc:
                    sql = """select id,if(length(alias)>0,
                        concat(alias,' -> ',round(precio,2)),
                        concat(nombre,' ',descripcion,' -> ',
                        round(precio,2))) from maestro where
                        (nombre like '%%%s%%' or descripcion like
                        '%%%s%%' or nombre like '%%%s%%' or descripcion
                        like '%%%s%%') %s order by
                        codbarras asc""" % (ingdat, ingdat,
                        ingdat.upper(), ingdat.upper(), sql_cond)
                    cuenta,resultado=query(sql,1)
                    ingdat,nombre=ladocl(resultado)
                    sql = sql_layout % (ingdat, '')
                    cuenta,resultado=query(sql,0)
                    if cuenta > 0:
                        win = definewin(panel,0,0)
                        win.addstr(1,len(titulo)+3,' '*num_char)
                        win.addstr(1,len(titulo)+3,ingdat)
                        return ingdat, 1


def guias(guia):
    guia_temp=string.split(guia,'-')
    guia_partes=len(guia_temp)
    guia_prefijo=''
    guia_sufijo=''
    if guia_partes==1:
        guia=guia_temp[0]
    elif guia_partes==2:
        guia_prefijo=guia_temp[0]
        guia=guia_temp[1]
    else:
        guia_prefijo=guia_temp[0]
        guia=guia_temp[1]
        guia_sufijo=guia_temp[2]
    return guia_prefijo,guia,guia_sufijo


def sintesis(condicion='',partes='4'):
    if condicion!='':
        condicion="and "+condicion
    sql="select distinct(dv.codigo),concat(vr.nombre,'/',vr.descripcion),sum(dv.cantidad),sum(dv.cantidad/"+partes+") from docventa as dv,variable as vr where dv.codigo=vr.codbarras and pv='"+str(posn)+"' and caja='"+str(cajn)+"' "+condicion
    sql+=" group by codigo"
    cuenta,resultado=query(sql)
    return resultado


def ingr_alm(panel,mensaje='Destino',pre_dato=''):
    while 1:
        dato=ingresodato(mensaje,panel,12,pre_dato,0,0)
        if dato=='Anular':
            return 'Anular', ''
        tam_dato=len(dato)
        modo = 0
        if tam_dato>0:
            condicion_dato=" and almacen='%s'" % dato
        else:
            condicion_dato=''
        sql="""select id,descripcion from almacenes_lista where
            descripcion!='' %s order by
            id asc,modo""" % condicion_dato
        cuenta,resultado=query(sql,1)
        if cuenta>0:
            dato, nomb = ladocl(resultado,'Almacenes')
            if dato!='Anular':
                win=definir(panel)
                win.addstr(1, 1, "%s: %s" % (mensaje, dato))
                sql = """select modo from almacenes_lista where
                    id='%s'""" % (dato)
                cnt, rso = query(sql, 0)
                if cnt > 0:
                    modo = rso[0]
                return dato, modo
            return 'Anular', ''


def ingr_vals(panel_1,panel_2,panel_3):
    cantidad=datesp('Cantidad',panel_1,8,'decimal,entero')
    peso1=datesp('Peso L',panel_2,8,'decimal,entero,vacio')
    peso2=datesp('Peso O',panel_3,8,'decimal,entero,vacio')
    sql = """select neto,tara from pesos_operaciones where
        codbarras='%s'""" % ingdat
    cuenta2,resultado2=query(sql,0)
    peso=float(peso1)+(float(peso2)/16)
    if cuenta2>0:
        neto=float(resultado2[0])
        tara=float(resultado2[1])
        if neto==0:
            neto=1
        if peso>0:
            tempcant=(peso-tara)/neto
        else:
            tempcant=0
        cantidad=round(float(cantidad)+tempcant,2)
    else:
        peso=0
        cantidad=cantidad
    return cantidad,peso


def datos_cons(sql):
    cuenta,resultado=query(sql,1)
    if cuenta>0:
        lineas=[]
        for x in range(0,cuenta):
            temp=resultado[x]
            datemp=[]
            for y in range(0,len(temp)):
                datemp.append(temp[y])
            datemp.append('0')
            lineas.append(datemp)
        tipo=0
    else:
        lineas=[]
        tipo=1
    return lineas,tipo


def sql_seleccion(sql,texto=''):
    cuenta,resultado=query(sql,1)
    if cuenta>0:
        dato,dscp=ladocl(resultado,texto)
        if dato=='Anular':
            return 'Anular','Anular'
        else:
            return dato,dscp
    else:
        return 'Anular','Anular'


def modo_ingr(lineas):
    motip='1'
    for z in range(0,len(lineas)):
        try:
            if lineas[z][0]==ingdat:
                motip='0'
        except:
            pass
    return motip


def agregar_valores(array,eliminar,*campos):
    cadena=[]
    tamano_elim=len(eliminar)
    if tamano_elim>0:
        for posicion in eliminar:
            cadena.append(str(array[posicion]))
    for campo in campos:
        cadena.append(str(campo))
    return cadena


def get_correlativo(modo,documento,edit=0,panel=''):
    prefijo = ''
    correlativo = 0
    sufijo = ''
    port = ''
    layout = ''
    if edit!=2:
        sql = """select prefijo,correlativo+1,sufijo,port,layout from   
            documentos_comerciales where id='%s'""" % (documento)
        cuenta,resultado=query(sql,0)
        if cuenta>0:
            prefijo = resultado[0]
            correlativo = resultado[1]
            sufijo = resultado[2]
            port = resultado[3]
            layout = resultado[4]
    if edit==1 or edit==2:
        if len(str(sufijo))>0:
            sufijo='-'+str(sufijo)
        dato=str(prefijo)+'-'+str(correlativo)+str(sufijo)
        while 1:
            ingdat=ingresodato('Guia',panel,30,dato,0,0)
            if ingdat=='Anular':
                return 'Anular','Anular','Anular'
            else:
                partes=string.split(ingdat,'-')
                elem=len(partes)
                try:
                    if elem==1:
                        correlativo=int(partes[0])
                    elif elem==2:
                        prefijo=partes[0]
                        correlativo=int(partes[1])
                    elif elem==3:
                        prefijo=partes[0]
                        correlativo=int(partes[1])
                        sufijo=partes[2]
                    break
                except:
                    pass
    return str(prefijo),str(correlativo),str(sufijo),str(port),str(layout)


def set_correlativo(doc_modo,tipo_doc,dato,modo=1):
    sql = """update documentos_comerciales set correlativo='%s'
        where id='%s'""" % (dato, tipo_doc)
    if modo == 1:
        exe = query(sql,3)
    else:
        return sql
    return


def conv_dict(cadena):
    data={}
    for parte in cadena:
#       print parte
        data[parte[0]]=parte[1]
#   print cadena
#   sys.exit()
    return data


def format_impresion_kdx(dato1,dato2,dato3,dato4,dato5,dato6,dato7,tamano='10,19,4,10,10,10,5'):
#   for parte in cadena:
#       string.center()
    pass


def cons_almacen(fecha='', producto='', modo_fecha=0, ciclo_fecha=0,
    modo_operacion=0):
    """
    Warehouse Stocks
    """
    if fecha!='':
        mes=fecha[5:7]
    data={}
    #SALDOS
    sql = """select cast(codbarras as UNSIGNED),sum(if(ingreso is
        NULL,0,ingreso)-if(salida is NULL,0,salida)) saldo from
        almacenes where almacen='%s' and estado='1' and
        month(fecha_doc)='%s' group by codbarras order by
        codbarras""" % (alm_base, mes)
    cuenta, resultado = query(sql,1)
    if cuenta > 0:
        for linea in resultado:
            codex = int(linea[0])
            saldx = linea[1]
            data[codex] = saldx
    if modo_operacion==0:
        if producto=='':
            return data
        else:
            producto = int(producto)
            if data.has_key(producto):
                return data[producto]
            else:
                return 0


def kardex(doc_modo,fecha,producto,modo_operacion=0):
    sql = """select concat(n_doc_prefijo,'-',n_doc_base),tiempo,
        operacion_logistica,if(modo='1',round(ingreso,2),'0')
        as ingreso,if(modo='2',round(salida,2),'0')
        as salida,'',if(modo='1',
        almacen_origen,almacen_destino) as alm_ref from almacenes where
        codbarras='%s' and fecha_doc='%s' and estado='1' and
        almacen='%s'""" % (producto, fecha, alm_base)
    cta,krdx=query(sql,1)
    lineas=[]
    ing_total=0
    sal_total=0
    stock_guia=''
    raya=79*'-'
    stock_anterior=cons_almacen(fecha,producto,2)
#   parte=string.ljust(str(producto),53)+string.rjust(str(stock_anterior),10)
    parte=string.ljust(str(producto),12)+'-'+string.center('STOCK ANTERIOR:',19)+'-'+string.center('-',4)+'--'+string.rjust('-',10)+'-'+string.rjust('-',10)+'-'+string.rjust(str(stock_anterior),10)+'--'+string.rjust('',5)
    lineas.append(parte)
    lineas.append(raya)
    for linea in krdx:
        n_guia=str(linea[0])
        fecha_guia=str(linea[1])
        operacion_guia=str(linea[2])
        ingreso_guia=str(str(linea[3]))
        salida_guia=str(linea[4])
        ing_total+=float(ingreso_guia)
        sal_total+=float(salida_guia)
        stock_guia=str((ing_total-sal_total)+stock_anterior)
        almacen_guia=str(linea[6])
        parte=string.ljust(n_guia,12)+' '+string.center(fecha_guia[:19],19)+' '+string.center(operacion_guia,4)+'  '+string.rjust(ingreso_guia,10)+' '+string.rjust(salida_guia,10)+' '+string.rjust(stock_guia,10)+'  '+string.rjust(almacen_guia,4)
        lineas.append(parte)
    parte=string.ljust('-',12)+'-'+string.center('TOTALES:',19)+'-'+string.center('-',4)+'--'+string.rjust(str(ing_total),10)+'-'+string.rjust(str(sal_total),10)+'-'+string.rjust(stock_guia,10)+'--'+string.rjust('',5)
    lineas.append(raya)
    lineas.append(parte)
    return lineas


def dict_list(cadena,modo=0):
    linea=[]
    if modo==0:
        elem=cadena.keys()
    for code in elem:
        sql = """select if(length(mae.alias)>0,mae.alias,
            concat(mae.nombre,' ',mae.descripcion)) from maestro mae
            where mae.id='%s'""" % (code)
        cuenta,resultado=query(sql,0)
        if cuenta>0:
            descrip_prod=str(resultado[0])
        else:
            descrip_prod=''
        temporal=[]
        temporal.append(code)
        temporal.append(descrip_prod)
        temporal.append(cadena[code])
        linea.append(temporal)
    linea.sort()
    return linea


def ver_imprimir(doc_modo,tipo_rep=0,prod_filt="genero=1",head='DISTRIBUCION:0100'):
    panel_top,panel_text_1,panel_text_2,panel_mid = win_def(2)#maxy,maxx
    fecha=fecha_ing(1,'t')
    codigo_prod='GENERAL'
    descrip_prod=''
    if fecha=='Anular':
        return 0
    else:
        if tipo_rep==1:
            prod_filt = "genero=1"
        ingdat, cuenta = datopc('Codigo', panel_text_1, 10,
            'insert,arriba,abajo,Anular', 'caracter', prod_filt)
        if ingdat=='Anular':
            return 0
        elif ingdat=='insert':
            codigo_prod=''
        else:
            sql = """select if(length(mae.alias)>0,mae.alias,
                concat(mae.nombre,' ',mae.descripcion)) from maestro mae
                where mae.id='%s'""" % (ingdat)
            cuenta,resultado=query(sql,0)
            if cuenta>0:
                codigo_prod=str(ingdat)
                descrip_prod=str(resultado[0])
        psey=0
        temc=0
        if tipo_rep==0:
            lineas=kardex(doc_modo,fecha,codigo_prod,0)
            titulo=string.ljust('GUIA',12)+' '+string.center('FECHA',19)+' '+string.center('OPER',4)+'  '+string.rjust('INGRESO',10)+' '+string.rjust('SALIDA',10)+' '+string.rjust('STOCK',10)+'  '+string.center('ALMAC',5)
            titulo_ctrl='Kardex'
        else:
            relacion=cons_almacen(fecha,codigo_prod,3)
            partir=0
            if len(codigo_prod)>0 and tipo_rep==1:
                lineas=[]
                temporal=[]
                temporal.append(str(codigo_prod))
                temporal.append(str(descrip_prod))
                temporal.append(str(relacion))
                lineas.append(temporal)
                partir=1
            if partir==0:
                lineas=dict_list(relacion)
            titulo=string.ljust('CODIGO',16)+string.ljust('DESCRIPCION',50)+string.center('CANTIDAD',14)
            titulo_ctrl='Stocks'
        while 1:
            viewtext(lineas,panel_mid,psey)
            winz=definewin(panel_mid,0,0)
            winz.addstr(0,1,titulo)
            updat()
            ingdat=ingresodato(titulo_ctrl,panel_top,10,'',0,0)
            if ingdat=='Anular':
                break
            elif ingdat=='arriba':
                psey-=1
            elif ingdat=='abajo':
                psey+=1
            elif ingdat=='insert':
                resp=segur("Imprimir?")
                if resp=='si':
                    raya=79*'-'
                    archivo=open('impresion.txt','w')
                    archivo.write(head+'\n')
                    archivo.write('Producto:'+str(codigo_prod)+' '+str(descrip_prod)+'\n\n')
                    archivo.write(raya+'\n')
                    archivo.write(titulo+'\n')
                    archivo.write(raya+'\n')
                    for lin in lineas:
                        try:
                            archivo.write(lin+'\n')
                        except:
                            data=string.ljust(str(lin[0]),16)+string.ljust(str(lin[1]),50)+string.rjust(str(lin[2]),13)
                            archivo.write(data+'\n')
                    archivo.close()
                    try:
                        os.system('lpr '+print_buffer+' impresion.txt')
                        resp=segur("IMPRESION EXITOSA!!!")
                    except:
                        resp=segur("ERROR EN LA IMPRESION!!!")
            else:
                psey=0
            temc=abs(psey)
            if temc>len(lineas):
                psey=0


def anulacion_guia(doc_modo=1,doc_tipo=6,oper_log_pref='1'):
    n_doc_prefijo=''
    n_doc_base=''
    filtro,temp_filt=ing_dat('Guia',0)
    if len(filtro)>0:
        temp=string.split(filtro,'-')
        if len(temp)==2:
            n_doc_prefijo=str(temp[0])
            n_doc_base=str(temp[1])
    query_trans=[]
    sql="""select concat(n_doc_prefijo,'-',n_doc_base),
        concat(almacen_origen,'/',almacen_destino,'-',
        operacion_logistica,'=',codbarras,'->',if(modo=1,ingreso,
        salida)) from almacenes where tipo_doc='%s' and estado='1' and
        n_doc_prefijo='%s' and n_doc_base='%s' and modo_doc='%s'
        and almacen='%s'""" % (doc_tipo,n_doc_prefijo,n_doc_base,
        doc_modo,alm_base)
    cuenta,resultado=query(sql,1)
    if cuenta>0:
        n_doc,op_doc=ladocl(resultado,'Guias')
        if op_doc=='Anular':
            return 0
        mensaje="Anular el Documento:"+str(n_doc)+",Esta Seguro?"
        resp=segur(mensaje)
        if resp =='si':
            temp_doc=string.split(n_doc,'-')
            n_pre=temp_doc[0]
            n_doc=temp_doc[1]
            sql="update almacenes set estado='0' where n_doc_base='"+str(n_doc)+"' and n_doc_prefijo='"+str(n_pre)+"' and (modo='"+str(oper_log_pref)+"1' or modo='"+str(oper_log_pref)+"2') and tipo_doc='"+str(doc_tipo)+"' and estado='1'"
            query_trans.append(sql)
            sql="select concat(n_serie_relacion,'-',n_doc_relacion) from almacenes where n_doc_base='"+str(n_doc)+"' and n_doc_prefijo='"+str(n_pre)+"' and (modo='"+str(oper_log_pref)+"1' or modo='"+str(oper_log_pref)+"2') and tipo_doc='"+str(doc_tipo)+"' and estado='1' and modo_doc='"+str(doc_modo)+"'"
            cuenta2,resultado2=query(sql,0)
            if cuenta2>0:
                if len(resultado2[0])>0:
                    n_doc2=resultado2[0]
                    temp_doc2=string.split(n_doc2,'-')
                    n_pre2=temp_doc2[0]
                    n_doc2=temp_doc2[1]
                    sql="update almacenes set estado='0' where n_doc_base='"+str(n_doc2)+"' and n_doc_prefijo='"+str(n_pre2)+"' and (modo='"+str(oper_log_pref)+"1' or modo='"+str(oper_log_pref)+"2') and tipo_doc='"+str(doc_tipo)+"' and estado='1'"
                    query_trans.append(sql)
            estado=query(query_trans,5)
            if estado==1:
                return 1
            else:
                return -1
        else:
            return 0


def anulacion_ventas():#doc_modo=1,doc_tipo=6,oper_log_pref='1'):
    sql="select documento,nombre from documentos_comerciales where modo=5 and documento!='' order by documento"
    cuenta,resultado=query(sql,1)
    if cuenta>0:
        cod_doc,dscp_doc=ladocl(resultado,'Tipo')
        if cod_doc=='Anular':
            return 0
    filtro,temp_filt=ing_dat('No',0)
    if len(filtro)>0:
        temp=string.split(filtro,'-')
        if len(temp)==2:
            n_doc_prefijo=str(temp[0])
            n_doc_base=str(temp[1])
    query_trans=[]
    sql="select concat(n_doc_prefijo,'-',n_doc_base),concat(codigo,'-',cantidad,'->',total) from docventa where estado='B' and comprobante='"+str(cod_doc)+"' and n_doc_prefijo='"+n_doc_prefijo+"' and n_doc_base='"+n_doc_base+"'" 
    cuenta,resultado=query(sql,1)
    if cuenta>0:
        n_doc,op_doc=ladocl(resultado,'No')
        if op_doc=='Anular':
            return 0
        mensaje="Anular el Documento:"+str(n_doc)+",Esta Seguro?"
        resp=segur(mensaje)
        if resp =='si':
            temp_doc=string.split(n_doc,'-')
            n_pre=temp_doc[0]
            n_doc=temp_doc[1]
            sql="update docventa set estado='A',cv_anul='"+str(codven)+"' where n_doc_base='"+str(n_doc)+"' and n_doc_prefijo='"+str(n_pre)+"' and comprobante='"+str(cod_doc)+"'"
            query_trans.append(sql)
            estado=query(query_trans,5)
            if estado==1:
                return 1
            else:
                return -1
    else:
        mensaje="Desea registrar este documento como Anulado?"
        resp=segur(mensaje)
        if resp=='si':
            fecha=fecha_ing(1,'t')
            if fecha=='Anular':
                return 0
            sql="insert into docventa (n_doc_prefijo,n_doc_base,comprobante,condicion_comercial,estado,cv_ing,cv_anul,fecha_vta) values ('"+n_doc_prefijo+"','"+n_doc_base+"','"+str(cod_doc)+"','1','A','"+str(codven)+"','"+str(codven)+"','"+str(fecha)+"')";
            query_trans.append(sql)
            estado=query(query_trans,5)
            if estado==1:
                return 1
            else:
                return -1
    return 0


def reimpresion_guia(doc_modo=1,doc_tipo=6,oper_log_pref='1'):
    n_doc_prefijo=''
    n_doc_base=''
    filtro,temp_filt=ing_dat('Guia',0)
    if len(filtro)>0:
        temp=string.split(filtro,'-')
        if len(temp)==2:
            n_doc_prefijo=str(temp[0])
            n_doc_base=str(temp[1])
    query_trans=[]
    sql = """select concat(n_doc_prefijo,'-',n_doc_base),
        concat(almacen_origen,'/',almacen_destino,'-',
        operacion_logistica,'=',codbarras,'->',ingreso,salida) from
        almacenes where tipo_doc='%s' and estado='1' and
        n_doc_prefijo='%s' and n_doc_base='%s' and modo_doc='%s' and
        almacen='%s'""" % (doc_tipo,n_doc_prefijo,n_doc_base,
        doc_modo,alm_base)
    cuenta,resultado=query(sql,1)
    if cuenta>0:
        n_doc,op_doc=ladocl(resultado,'Guias')
        if op_doc=='Anular':
            return 0
        mensaje="Reimprimir el Documento: %s, Esta Seguro?" % n_doc
        resp=segur(mensaje)
        if resp =='si':
            temp_doc=string.split(n_doc,'-')
            n_pre=temp_doc[0]
            n_doc=temp_doc[1]
            if doc_tipo==6:
                impresion_guia_interna(doc_modo,doc_tipo,oper_log_pref,n_pre,n_doc)
            elif doc_tipo==5:
                impresion_guia_externa(doc_modo,doc_tipo,oper_log_pref,n_pre,n_doc)


#def impresion_guia_interna(productos,fecha,hora,documento,operacion,almacen,prefijo,num_doc):
def impresion_guia_interna(doc_modo=1,doc_tipo=6,oper_log_pref='1',prefijo='',num_doc='',port_imp='',layout=''):
    sql="""select codbarras,if(modo=1,round(ingreso,2),round(salida,2)),
        date(fecha_doc),time(tiempo),operacion_logistica,modo,
        almacen_origen,almacen_destino,turno from almacenes where
        estado='1' and  n_doc_prefijo='%s' and n_doc_base='%s' and
        modo_doc='%s' and almacen='%s'""" % (prefijo,num_doc,doc_modo,
        alm_base)
    cuenta,resultado=query(sql)
    productos=[]
    for parte in resultado:
        temporal=[]
        temporal.append(str(parte[0]))
        temporal.append(str(parte[1]))
        productos.append(temporal)
        fecha=str(parte[2])
#       hora=str(parte[3])
        operacion=str(parte[4])
        modo=str(parte[5])
        if modo[-1]=='1':
            almacen=str(parte[6])
            documento='Nota de Ingreso'
        else:
            almacen=str(parte[7])
            documento='Nota de Salida'
        turno=str(parte[8])
    fecha=fecha[:10]
    fecha_impresion=time.strftime("%Y-%m-%d")
    hora_impresion=time.strftime("%H:%M:%S")
#   hora=hora[:8]
    sql = """select descripcion from operaciones_logisticas where
        id='%s'""" % operacion
    cuenta,resultado=query(sql,0)
    if cuenta>0:
        descripcion_operacion=resultado[0]
        descripcion_operacion=descripcion_operacion[:20]
    else:
        descripcion_operacion=operacion
    sql = """select descripcion from almacenes_lista where
        id='%s'""" % almacen
    cuenta,resultado=query(sql,0)
    if cuenta>0:
        descripcion_almacen=resultado[0]
        descripcion_almacen=descripcion_almacen[:21]
    else:
        descripcion_almacen=almacen
        
    for n_cop in range(1,3):
        if n_cop==1:
            doc_tipo='ORIGINAL'
        else:
            doc_tipo='COPIA'
        n_arch="guia_int_"+str(prefijo)+"-"+str(num_doc)+".gui"
        archivo=open(n_arch,"w")
        linea=string.ljust(empresa,20)+string.center(' ',17)+string.center(documento,40)
        archivo.write(linea+'\n')
        linea=string.ljust('',20)+string.center(' ',17)+string.center(descripcion_operacion,40)
        archivo.write(linea+'\n')
        linea=string.ljust('',20)+string.center(' ',17)+string.center('N:'+str(prefijo)+'-'+str(num_doc),40)
        archivo.write(linea+'\n')
        linea=string.ljust('Fecha:'+str(fecha),17)+string.ljust('Alm:'+str(almacen)+'-'+str(descripcion_almacen),30)+string.ljust('Oper:'+operacion+'-'+descripcion_operacion,30)
        archivo.write(linea+'\n')
        raya=77*'-'
        archivo.write(raya+'\n')
        linea=string.center('CODIGO',10)+string.center('UNI',3)+string.center('CANTIDAD',10)+' '+string.center('DESCRIPCION',53)
        archivo.write(linea+'\n')
        archivo.write(raya+'\n')
        cnt=0
        for linea in productos:
            cnt+=1
            codigo=str(linea[0])
            cantidad=str(linea[1])
            sql = """select ucase(unm.codigo),if(length(mae.alias)>0,
                mae.alias,concat(mae.nombre,' ',mae.descripcion)) from
                maestro mae left join unidades_medida unm on
                unm.id=mae.unidad_medida where
                mae.id='%s'""" % (codigo)
            cuenta,resultado=query(sql,0)
            unidad_med=resultado[0]
            descripcion=resultado[1]
            linea=string.center(codigo,10)+string.center(unidad_med,3)+string.rjust(cantidad,10)+' '+string.ljust(descripcion,53)
            archivo.write(linea+'\n')
        for parte in range(cnt,20):
            archivo.write('\n')
        archivo.write(raya+'\n')
        linea=string.ljust(str(doc_tipo),37)+string.center('Despacho',20)+string.center('Recibo',20)
        archivo.write(linea+'\n')
        linea=string.ljust('Fecha '+str(fecha_impresion),20)+string.ljust('Hora '+str(hora_impresion),20)+string.ljust('Turno '+str(turno),20)
        archivo.write(linea+'\n\n\n\n')
        archivo.close()
        os.system('lpr '+print_buffer+' '+n_arch)
        time.sleep(1)
        os.remove(n_arch)


#def impresion_guia_externa(productos,fecha,almacen,transportista,vehiculo,prefijo,num_doc,):
def impresion_guia_externa(doc_modo=1,doc_tipo=5,oper_log_pref='1',prefijo='',num_doc='',port_imp='',layout=''):
    #<---Cambiar
#   sql="select codigo,descripcion from guias_plantillas where modo='"+str(doc_modo)+"' and documento='"+str(doc_tipo)+"'"
    sql="select tipo from guias_plantillas where modo='"+str(doc_modo)+"' and documento='"+str(doc_tipo)+"'"
    cuenta,resultado=query(sql)
    if cuenta==1:
        layout_guia=int(resultado[0][0])
#       codigo=resultado[0][0]
#       if codigo=='101':
#           layout_guia=0
#       elif codigo=='401':
#           layout_guia=1
#       else:
#           layout_guia=0
    else:
        layout_guia=0
    #--->Cambiar
#   print cuenta,resultado,layout_guia,codigo
#   sys.exit()
    sql = """select codbarras,if(modo=1,round(ingreso,2),
        round(salida,2)),fecha_doc,tiempo,operacion_logistica,modo,
        almacen_origen,almacen_destino,transportista,vehiculo,turno,
        observaciones from almacenes where estado='1' and
        n_doc_prefijo='%s' and n_doc_base='%s' and modo_doc='%s' and
        almacen='%s'""" % (prefijo,num_doc,doc_modo,alma_base)
    cuenta,resultado=query(sql)
    productos=[]
    for parte in resultado:
        temporal=[]
        temporal.append(str(parte[0]))
        temporal.append(str(parte[1]))
        productos.append(temporal)
        fecha=str(parte[2])
        hora=str(parte[3])
        operacion=str(parte[4])
        modo=str(parte[5])
        if modo[-1]=='1':
            almacen=str(parte[6])
        else:
            almacen=str(parte[7])
        transportista=str(parte[8])
        vehiculo=str(parte[9])
        turno=str(parte[10])
        observac=str(parte[11])
    sql = """select descripcion,doc_id,direccion from almacenes_lista
        where id='%s'""" % almacen
    cuenta,resultado=query(sql,0)
    almacen_descripcion=str(resultado[0])
    ruc=str(resultado[1])
    direccion=str(resultado[2])
    sql = """select nombres,apellidos,direccion,emp_doc_id from
        transportistas where codigo='%s'""" % (transportista)
    cuenta,resultado=query(sql,0)
    transp_nombres=str(resultado[0])
    transp_apellidos=str(resultado[1])
    transp_emp=str(resultado[2])
    sql = """select registro from vehiculos where
        codigo='%s'""" % (vehiculo)
    cuenta,resultado=query(sql,0)
    unidad_movil=str(resultado[0])
    #Generacion de Archivo
    n_arch="guia_ext_"+str(prefijo)+"-"+str(num_doc)+".gui"
    if layout_guia==1:
        archivo=open(n_arch,"w")
        archivo.write('\n\n\n\n\n\n')
        linea=string.rjust('NUTRA S.A.-Tda:'+almacen_descripcion+'-'+str(turno),45)
        archivo.write(linea+'\n')
        linea=string.rjust(observac,45)
        archivo.write(linea+'\n')
        linea=string.rjust('20144215649',20)+string.rjust(str(fecha[:10]),25)
        archivo.write(linea+'\n')
        linea=string.rjust(direccion,45)+string.center(str(prefijo)+'-'+str(num_doc),35)
        archivo.write(linea+'\n\n')
        linea=string.rjust('',50)+string.rjust(transp_nombres+' '+transp_apellidos,27)
        archivo.write(linea+'\n')
        linea=string.rjust('',50)+string.rjust('',27)
        archivo.write(linea+'\n')
        linea=string.rjust('',50)+string.rjust(transp_emp,27)
        archivo.write(linea+'\n')
        linea=string.rjust('',50)+string.rjust(unidad_movil,27)
        archivo.write(linea+'\n')
        archivo.write('\n\n\n')
        for linea in productos:
            codigo=str(linea[0])
            cantidad=str(linea[1])
            sql = """select ucase(unm.codigo),if(length(mae.alias)>0,
                mae.alias,concat(mae.nombre,' ',mae.descripcion)) from
                maestro mae left join unidades_medida unm on
                unm.id=mae.unidad_medida where
                mae.id='%s'""" % (codigo)
            cuenta,resultado=query(sql,0)
            unidad_med=resultado[0]
            descripcion=resultado[1]
            linea=string.rjust(cantidad,10)+' '+string.ljust(unidad_med,10)+string.ljust(codigo+'-'+descripcion,40)
            archivo.write(linea+'\n')
        archivo.close()
    else:
        archivo=open(n_arch,"w")
        archivo.write('\n\n\n\n\n')
        linea=string.rjust('NUTRA S.A.-Tda:'+almacen_descripcion+'-'+str(turno),45)
        archivo.write(linea+'\n')
        linea=string.rjust(observac,45)
        archivo.write(linea+'\n\n')
        linea=string.rjust('20144215649',20)+string.rjust(str(fecha[:10]),25)
        archivo.write(linea+'\n\n')
        linea=string.rjust(direccion,45)+string.center(str(prefijo)+'-'+str(num_doc),35)
        archivo.write(linea+'\n\n\n')
        linea=string.rjust('',50)+string.rjust(transp_nombres+' '+transp_apellidos,27)
        archivo.write(linea+'\n')
        linea=string.rjust('',50)+string.rjust('',27)
        archivo.write(linea+'\n')
        linea=string.rjust('',50)+string.rjust(transp_emp,27)
        archivo.write(linea+'\n')
        linea=string.rjust('',50)+string.rjust(unidad_movil,27)
        archivo.write(linea+'\n')
        archivo.write('\n\n\n')
        for linea in productos:
            codigo=str(linea[0])
            cantidad=str(linea[1])
            sql = """select ucase(unm.codigo),if(length(mae.alias)>0,
                mae.alias,concat(mae.nombre,' ',mae.descripcion)) from
                maestro mae left join unidades_medida unm on
                unm.id=mae.unidad_medida where
                mae.id='%s'""" % (codigo)
            cuenta,resultado=query(sql,0)
            unidad_med=resultado[0]
            descripcion=resultado[1]
            linea=string.rjust(cantidad,10)+' '+string.ljust(unidad_med,10)+string.ljust(codigo+'-'+descripcion,40)
            archivo.write(linea+'\n')
        archivo.close()
    os.system('lpr '+print_buffer+' '+n_arch)
    time.sleep(1)
    os.remove(n_arch)


def win_txt(panel,head,txt):
    win=definir(panel)
    texto=str(head)+':'+str(txt)
    win.addstr(1,1,texto)
    updat()
    return


def panel_input(head,panel,sql):
    dato=ingresodato(head,panel,10,'',1,0)
    if dato=='Anular':
        return -1
    cuenta,resultado=query(sql)
    pass


def linea_dato(msg,win,pan,texto='',pos_y=1):
    texto=str(texto)
    size_y,size_x=win.getmaxyx()
    ubic_x=len(msg)+3
    tam_real_x=size_x-2
    txt_pre=0
    if len(texto)>0:
        dato=texto
        txt_pre=1
    else:
        dato=''
    win.addstr(pos_y,1,msg)
    while 1:
        if ubic_x>=tam_real_x:
            ubic_x=len(msg)+3
        if txt_pre==1:
            win.addstr(pos_y,ubic_x,dato)
            ubic_x+=len(dato)
            txt_pre=0
        updat()
        caracter=obch(pan,pos_y,ubic_x,'v',0)
        if caracter=='enter':
            return dato
        elif caracter=='escape':
            return 'Anular'
        elif caracter=='arriba' or caracter=='abajo' or caracter=='insert' or caracter=='spag' or caracter=='ppag' or caracter=='derecha' or caracter=='izquierda':
            pass
        elif caracter=='backspace':
            ubic_x-=1
            if ubic_x<=len(msg)+3:
                ubic_x=len(msg)+3
            dato=dato[:-1]
            win.addstr(pos_y,ubic_x,'   ')
            caracter=''
        elif (caracter>='0' and caracter<='9') or (caracter>='a' and caracter<='z') or (caracter>='A' and caracter<='Z') or (caracter=='-') or (caracter=='.') or (caracter==' ') or (caracter=='&'):
            ubic_x+=1
            dato+=str(caracter)
            if ubic_x >=(tam_real_x):
                ubic_x=tam_real_x
                dato=dato[:tam_real_x]


def ing_dat(msg,min=4,long=20,posy=-1,posx=-1):
    cuenta=len(msg)+long
    tny=3
    if posy==-1:
        posy=(maxy-tny)/2
    if posx==-1:
        tnx=cuenta
        posx=(maxx-tnx)/2
    pan=mkpanel(curses.COLOR_WHITE,tny,cuenta,posy,posx)
    win=definir(pan)
#   win,y,x=definewin(pan)
    curses.curs_set(1)
    curses.echo()
    win.addstr(0,0,msg)
    updat()
    while 1:
        linea=win.getstr(1,1)
        valor,tipdat=expresion(linea)
        if tipdat=='entero' and len(linea)>=min:
            curses.noecho()
            curses.curs_set(0)
            win.erase()
            updat()
            return linea,tipdat
        elif (tipdat=='alfanumerico' or tipdat=='caracter') and len(linea)>=min:
            curses.noecho()
            curses.curs_set(0)
            win.erase()
            updat()
            return linea,tipdat


def directory_check(msg):
    cliente,tipdat=ing_dat(msg)
    if tipdat=='entero':
        modo_cli=0
        condicion="doc_id like '"+str(cliente)+"%'"
    else:
        modo_cli=1
        condicion="nombre_corto like '%"+string.upper(cliente)+"%'"
    sql="select id,nombre_corto from directorio where "+condicion+" order by doc_id"
    cnt,rso=query(sql)
    if cnt > 0:
        docnum, nombre = ladocl(rso,msg)
        return docnum,nombre
    else:
        return 'ND','ND'


def ventas_proc(txt_fld=8,fech_cnt=1,fech_hea='t'):
    panel_top,panel_text_1,panel_text_2,panel_text_3,panel_text_4,panel_text_5,panel_text_6,panel_text_7,panel_text_8,panel_mid=win_def(txt_fld)#maxy,maxx
    fecha=fecha_ing(fech_cnt,fech_hea)
    if fecha=='Anular':
        return 0
    tienda_head='Tienda'
    caja_head='Caja'
    doc_head='Tipo Doc'
    cond_head='Condicion'
    cliente=''
    detalle_prod=''
    ing_detalle=segur('Ingresos con Detalles?')
    if ing_detalle=='si':
        ing_detalle=1
    else:
        ing_detalle=0
    while 1:
        tienda=ingresodato(tienda_head,panel_text_1,10,'',1,0)
        if tienda=='Anular':
            return 0
        sql="select codigo,nombre from puntos_venta where (codigo='"+str(tienda)+"' or nombre like '%"+str(tienda)+"%') and (codigo!='' or nombre!='') order by codigo"
        cuenta,resultado=query(sql)
        if cuenta==1:
            tienda=resultado[0][0]
            tienda_dscp=resultado[0][1]
            break
        elif cuenta>1:
            tienda,tienda_dscp=ladocl(resultado,'Punto de Venta')
            if tienda=='Anular':
                return 0
            else:
                break
    win_txt(panel_text_1,tienda_head,tienda_dscp)
    sql="select distinct(documento),nombre from documentos_comerciales where modo=5 order by documento"
    cuenta,resultado=query(sql)
    if cuenta>0:
        doc_tipo,doc_tipo_dscp=ladocl(resultado,'Documento')
        if doc_tipo=='Anular':
            return 0
        sql="select copia,detalle,impresion from documentos_comerciales where modo=5 and documento='"+str(doc_tipo)+"'"
        cuenta,resultado=query(sql,0)
        if cuenta>0:
            doc_tipo_copia=str(resultado[0])
            doc_tipo_detalle=str(resultado[1])
            doc_tipo_impresion=str(resultado[2])
            if doc_tipo_detalle=='1':
                while 1:
                    cliente, nomb_cliente = directory_check("Cliente")
                    if cliente=='ND':
                        segur("Debe Registrar el Cliente")
                    elif cliente=='Anular':
                        return 0
                    else:
                        break
    else:
        return 0
    texto_head='Ventas: Tipo:'+str(doc_tipo_dscp)+' - Cliente:'+str(cliente)+' - Fecha:'+str(fecha[:10])
    winhead(texto_head,panel_top)
    while 1:
        num_doc=ingresodato('No.Doc',panel_text_2,10,'',1,0)
        if num_doc=='Anular':
            break
        doc_part=string.split(num_doc,'-')
        try:
            if len(doc_part)==2:
                num_doc_pre=str(doc_part[0])
                num_doc=int(doc_part[1])
            else:
                num_doc_pre=''
                num_doc=int(doc_part[0])
            break
        except Exception,error:
            pass
    if num_doc=='Anular':
        return 0
    sql = """select doc.codigo,concat(mae.nombre,' ',mae.descripcion),
        doc.cantidad,doc.precio,(doc.cantidad*doc.precio) as importe
        from docventa doc left join maestro mae on
        mae.id=doc.codigo where doc.n_doc_prefijo='%s' and
        doc.n_doc_base='%s' and doc.comprobante='%s' and
        doc.pv='%s'""" % (num_doc_pre, num_doc, doc_tipo, tienda)
    lineas,tipo=datos_cons(sql)
    if len(lineas)==0:
        sql="select codigo,descripcion from condiciones_comerciales where modo=0 and condicion!='' order by codigo"
        cuenta,resultado=query(sql)
        if cuenta>0:
            cond_com,cond_com_dscp=ladocl(resultado,'Condicion')
            if cond_com=='Anular':
                return 0
        else:
            return 0    
        win_txt(panel_text_3,cond_head,cond_com_dscp)
        while 1:
            factor_tmp='1.0'
            factor=ingresodato('Factor',panel_text_4,10,factor_tmp,1,0)
            try:
                factor=float(factor)
                break
            except:
                pass
    else:
        sql="select doc.condicion_comercial,con.descripcion from docventa doc left join condiciones_comerciales con on con.codigo=doc.condicion_comercial where doc.n_doc_prefijo='"+str(num_doc_pre)+"' and doc.n_doc_base='"+str(num_doc)+"' and doc.comprobante='"+str(doc_tipo)+"' and doc.pv="+str(tienda)+""
        cuenta,resultado=query(sql,0)
        if cuenta>0:
            cond_com=resultado[0]
            cond_com_dscp=resultado[1]
        else:
            return 0
        win_txt(panel_text_3,cond_head,cond_com_dscp)
        factor=1.0
        win_txt(panel_text_4,'Factor',str(factor))
    psey=0
    temc=0
    while 1:
        viewtext(lineas,panel_mid,psey,'c')
        total_doc=0
        for parte in lineas:
            total_doc+=float(parte[4])
        winhead('Total: '+str(total_doc),panel_text_8)
        ingdat,cuenta=datopc('Codigo',panel_text_5,10,'insert,arriba,abajo,Anular','caracter',"genero=2")
        sql = """select if(length(alias)>0,alias,
            concat(nombre,' ',descripcion)),precio from
            maestro where id='%s'""" % (ingdat)
        cuenta,resultado=query(sql,0)
        if cuenta>0:
            if ing_detalle==1:
                detalle_prod,tipo_detalle_prod=ing_dat('Detalle',0,40)
            nombre_prod=resultado[0]
            precio=round(float(resultado[1])*factor,2)
            cantidad=datesp('Cantidad',panel_text_6,8,'decimal,entero')
            cantidad=float(cantidad)
            imp_temp=float(precio)*float(cantidad)
            importe=datesp('Importe',panel_text_7,8,'decimal,entero',str(imp_temp))
            if importe>0 and cantidad>0:
                try:
                    precio=round(float(importe)/float(cantidad),2)
                except:
                    precio=0
            else:
                precio=0
            if cantidad>0:
                detalle_prod=string.upper(detalle_prod)
                motip=modo_ingr(lineas)
                prov=agregar_valores([],[],ingdat,nombre_prod,cantidad,precio,importe,detalle_prod,motip)
                lineas.append(prov)
        if ingdat=='Anular':
            resp=segur("Esta seguro(a)? ")
            if resp=='si':
                break
        elif ingdat=='insert':
            while 1:
                igv=round((total_doc*19)/125,2)
                igv=ingresodato('IGV',panel_text_5,10,str(igv),1,0)
                try:
                    igv=float(igv)
                    break
                except:
                    pass
            while 1:
                srv=round((total_doc*6)/125,2)
                srv=ingresodato('SRV',panel_text_6,10,str(srv),1,0)
                try:
                    srv=float(srv)
                    break
                except:
                    pass
            total_doc=round(total_doc,2)
            total_neto=round(total_doc-(igv+srv),2)
            detalle_impto='IGV:'+str(round(igv,2))+' SRV:'+str(round(srv,2))
            sql_full=[]
            tiempo=time.strftime("%Y-%m-%d %H:%M:%S")
            for z in range(0,len(lineas)):
                if lineas[z][3]=='0':
                    base=sqlsend(lineas[z],'codigo,cantidad,total',0)
                    sql="update docventa set "+base+",cv_ing='"+str(codven)+"',tiempo='"+str(tiempo)+"' where codigo='"+str(lineas[z][0])+"' and pv='"+str(tienda)+"'"
                else:
                    temporal=lineas[z]
                    temporal=agregar_valores(temporal,[0,2,3,4,5],total_doc,tienda,codven,tiempo,fecha,num_doc_pre,num_doc,doc_tipo,cond_com,total_neto,detalle_impto,'B',cliente)
                    base=sqlsend(temporal,'codigo,cantidad,precio,sub_total_bruto,detalle,total,pv,cv_ing,tiempo,fecha_vta,n_doc_prefijo,n_doc_base,comprobante,condicion_comercial,total_neto,detalle_impto,estado,cliente',1)
                    sql="insert into docventa "+base
                    sql_full.append(sql)
            query(sql_full,5)
            break
        elif ingdat=='arriba':
            psey-=1
        elif ingdat=='abajo':
            psey+=1
        temc=abs(psey)
        if temc>len(lineas):
            psey=0
    return


def data_proc(tipo_mov=1,doc_modo=1,doc_tipo=6,txt_fld=3,fech_cnt=1,
    fech_hea='t',turno_ing=1,masa_ing=1,impresion=1,oper_log='IPT',
    alm_rel='0101',alm_base='0100',oper_log_pref='1',add_data='0|*',
    prod_filt='genero=1'):
    """
    Data Processing
    """
    panel_top,panel_text_1,panel_text_2,panel_text_3,panel_mid=win_def(txt_fld)#maxy,maxx
    fecha=fecha_ing(fech_cnt,fech_hea)
    add_box = add_data.split('|')
    if fecha == 'Anular':
        return 0
    else:
        if turno_ing==1:
            sql = """select id,descripcion from turnos 
                order by turno asc"""
            turno,turno_dscp=sql_seleccion(sql,'Turno')
            if turno=='Anular':
                return 0
        turno = 1
        modo_oper_log=''
        oper_log2=''
        modo_oper_log2=''
        masa=''
        extra_data=''
        extra_oper_log = 0
        alm_ori2=''
        alm_des2=''
        correlativo2 = 0
        transp_codigo = 1
        vehiculo_codigo = 1
        titulo_almacenes = ''
        det_doc_ori = 0
        id_prov = 0
        modo_ori = ''
        modo_des = ''
        modo_ori2 = ''
        modo_des2 = ''
        while 1:
            if oper_log=='':
                oper_log=ingresodato('Operacion',panel_text_1,10,oper_log,1,0)
                if oper_log=='Anular':
                    return 0
                tam_oper_log=len(oper_log)
                if tam_oper_log>=3 and tam_oper_log<=4:
                    condicion_oper_log="operacion='"+str(oper_log)+"' or operacion=ucase('"+str(oper_log)+"')"
                elif tam_oper_log>4:
                    condicion_oper_log="(descripcion like '"+str(oper_log)+"%' or descripcion like ucase('"+str(oper_log)+"%')) and operacion!=''"
                else:
                    condicion_oper_log="operacion!=''"
                sql= """select id,descripcion from 
                    operaciones_logisticas where %s order by
                    modo,descripcion""" % (condicion_oper_log)
                oper_log,oper_log_dscp=sql_seleccion(sql,'Operaciones Logisticas')
                if oper_log=='Anular':
                    return 0
            sql = """select cast(modo as UNSIGNED),operacion_relac,
                almacen_relac,detalle,id from
                operaciones_logisticas where
                id='%s'""" % (oper_log)
            cta, rso = query(sql, 0)
            if cta > 0:
                modo_oper_log = str(rso[0])
                oper_log = str(rso[4])
            else:
                return 0
            if alm_rel=='':
                if rso[0] == 1:
                    alm_ori, modo_ori = ingr_alm(panel_text_1,'Origen')
                    alm_des=alm_base
                    det_doc_ori=rso[3]
                elif rso[0] == 2:
                    alm_ori=alm_base
                    alm_des, modo_des = ingr_alm(panel_text_1,'Destino')
                if modo_ori == 0 or modo_des == 0:
                    id_prov, nombre_prov = directory_check("Proveedor")
                    if id_prov == 'Anular':
                        return 0
                titulo_almacenes = "%s/%s" % (alm_ori, alm_des)
                if alm_ori=='Anular' or alm_des=='Anular':
                    return 0
                if rso[1]!='':
                    almacen_relac=rso[2]
                    sql = """select modo from operaciones_logisticas
                        where id='%s'""" % (rso[1])
                    cta2,rso2=query(sql,0)
                    if cta2==0:
                        return 0
                    else:
                        ##Data
                        if rso2[0]==1:
                            if almacen_relac!='':
                                alm_ori2=almacen_relac
                            else:
                                alm_ori2, modo_ori2 = ingr_alm(panel_text_2,'Origen',almacen_relac)
                            alm_des2=alm_base
                            titulo_almacenes = "%s/%s" % (alm_des,
                                alm_ori2)
                        elif rso2[0]==2:
                            alm_ori2=alm_base
                            if almacen_relac!='':
                                alm_des2=almacen_relac
                            else:
                                alm_des2, modo_des2 = ingr_alm(panel_text_2,'Destino',almacen_relac)
                            titulo_almacenes = "%s/%s" % (alm_ori,
                                alm_des2)
                        oper_log2=str(rso[1])
                        modo_oper_log2=oper_log_pref+str(rso2[0])
                        extra_oper_log=1
                        if alm_ori2=='Anular' or alm_des2=='Anular':
                            return 0
                break
            else:
                alm_ori=alm_rel
                alm_des=alm_base
                titulo_almacenes=str(alm_ori)+'/'+str(alm_des)
                break
        cabecera='Fecha: '+str(fecha)+' - Turno: '+str(turno)+' - Operacion: '+str(oper_log)+'/'+str(oper_log2)+' - Almacenes: '+str(titulo_almacenes)
        if tipo_mov==2:
            transp_data=ingresodato('Transp',panel_text_1,10,'',1,0)
            if transp_data=='Anular':
                return 0
            sql="select id,concat(nombres,' ',apellidos) from transportistas where (nombres like '%"+str(transp_data)+"%' or apellidos like '%"+str(transp_data)+"%') and (nombres!='' or apellidos!='')"
            transp_codigo,transp_descripcion=sql_seleccion(sql,'Transportista')
            if transp_codigo=='Anular':
                return 0
            sql="select id,concat('->',registro,'-',marca,' / ',modelo) from vehiculos where codigo!=''"
            vehiculo_codigo,vehiculo_descripcion=sql_seleccion(sql,'Vehiculos')
            if vehiculo_codigo=='Anular':
                return 0
        if masa_ing==1:
            masa=ingresodato('Masa',panel_text_1,10,'',1,1)
            if masa=='Anular' or masa=='':
                return 0
            cabecera='Fecha: '+str(fecha)+' - Turno: '+str(turno)+ ' - Masa: '+str(masa)+' - Operacion: '+str(oper_log)
        lineas=[]
        psey=0
        temc=0
        winhead(cabecera,panel_top)
        validacion_prod={}
        observaciones=''
        observaciones,tip_observ=ing_dat('Observaciones',0)
        while 1:
            viewtext(lineas,panel_mid,psey)
            ingdat,cuenta=datopc('Codigo',panel_text_1,10,'insert,arriba,abajo,Anular','caracter',prod_filt)
            sql = """select if(length(mae.alias)>0,concat(mae.alias,' ',
                unm.codigo),concat(mae.nombre,' ',mae.descripcion,' ',
                unm.codigo)),mae.unidad_medida_valor from maestro mae
                left join unidades_medida unm on
                unm.id=mae.unidad_medida where
                mae.id='%s'""" % (ingdat)
            cuenta,resultado=query(sql,0)
            if cuenta>0:
                nombre_prod = resultado[0]
                cant_unmd = resultado[1]
                #add_data = mode for additional data
                if add_box[0] == '1':
                    msg_data = add_box[1]
                    while 1:
                        extra_data = ingresodato(msg_data,panel_text_2,30,'',10)
                        if extra_data == 'Anular':
                            return 0
                        cantidad=1
                        break
                else:
                    cantidad=datesp('Cantidad',panel_text_2,8,'decimal,entero','',1,1)
                if add_box[0] == '2':
                    msg_data = add_box[1]
                    elem_data = float(cantidad) * float(cant_unmd)
                    while 1:
                        extra_data = ingresodato(msg_data,panel_text_3,30,elem_data,10)
                        if extra_data == 'Anular':
                            return 0
                        cantidad = float(extra_data)
                        extra_data = ''
                        break                    
                #relacion=cons_almacen(modo_ingreso,modo_salida,fecha,codigo_prod,3)
                #modo_ingreso=oper_log_pref+'1'
                #modo_salida=oper_log_pref+'2'
                stock_individual=cons_almacen(fecha,str(ingdat),3) #modo_ingreso,modo_salida,producto='',fecha='',modo_fecha=0,ciclo_fecha=0,modo_operacion=0
                cantidad=float(cantidad)
                if modo_oper_log[-1]=='2':
                    stock_individual=float(stock_individual)
                else:
                    stock_individual=float(cantidad)
                valid_error=0
                if extra_oper_log==1:
                    stock_individual=cantidad
                if validacion_prod.has_key(ingdat):
                    if round(cantidad,2)>round(stock_individual,2):
                        valid_error=1
                    else:
                        if round(cantidad,2)>0:
                            validacion_prod[ingdat]=[cantidad,nombre_prod,1]
                else:
                    if round(cantidad,2)>round(stock_individual,2):
                        valid_error=1
                    else:
                        if round(cantidad,2)>0:
                            validacion_prod[ingdat]=[cantidad,nombre_prod,1]
                if (valid_error==1 or stock_individual==0 or cantidad==0) and (modo_oper_log[-1]=='2' and modo_oper_log2==''):
                    segur('El Stock de este producto es:'+str(stock_individual))
                    cuenta=0
                    resultado=''
                else:
                    lineas=[]
                    orden_prod=validacion_prod.keys()
                    orden_prod.sort()
                    for valor in orden_prod:
                        cod_tmp=valor
                        cnt_tmp=validacion_prod[valor][0]
                        nom_tmp=validacion_prod[valor][1]
                        mod_tmp=validacion_prod[valor][2]
                        prov=agregar_valores([],[],cod_tmp,cnt_tmp,nom_tmp,mod_tmp)
                        lineas.append(prov)
            if ingdat=='Anular':
                resp=segur("Esta seguro(a)? ")
                if resp=='si':
                    return 0
            elif ingdat=='insert':
                prefijo2=''
                correlativo2 = 0
                sufijo2=''
                query_trans=[]
                tiempo_reg=time.strftime("%Y-%m-%d %H:%M:%S")
                if tipo_mov==1:
                    edit_guia=0
                    if det_doc_ori==1:
                        edit_guia=2
                else:
                    edit_guia=1
                prefijo,correlativo,sufijo,port_imp,layout=get_correlativo(doc_modo,doc_tipo,edit_guia,panel_text_3)
                if correlativo=='Anular':
                    return
                if extra_oper_log==1:
                    prefijo2=prefijo
                    correlativo2=int(correlativo)+1
                    sufijo2=sufijo
                for z in range(0,len(lineas)):
                    if lineas[z][3]=='0':
                        base=sqlsend(lineas[z],'codbarras,ingreso',0)
                        sql = "update almacenes set "+base+",user_ing='"+str(codven)+"',tiempo='"+str(tiempo_reg)+"' where n_doc_base='"+str(correlativo)+"' and codbarras='"+str(lineas[z][0])+"' and turno='"+str(turno)+"' and fecha_doc='"+str(fecha)+"' and estado='1' and operacion_logistica='"+str(oper_log)+"' and modo='"+str(modo_oper_log)+"' and modo_doc='"+str(doc_modo)+"' and tipo_doc='"+str(doc_tipo)+"'"
                        query_trans.append(sql)
                    else:
                        campos_bd = """codbarras,%s,turno,
                            n_doc_prefijo,n_doc_base,user_ing,tiempo,
                            fecha_doc,modo,almacen_origen,
                            almacen_destino,fecha_produccion,estado,
                            masa,operacion_logistica,extra_data,
                            modo_doc,tipo_doc,n_prefijo_relacion,
                            n_doc_relacion,transportista,vehiculo,
                            observaciones,almacen,registro,proveedor"""
                        if modo_oper_log == '1':
                            adic = "ingreso"
                        else:
                            adic = "salida"
                        campos_bd = campos_bd % adic
                        temporal = lineas[z]
                        temporal_x = agregar_valores(temporal, [0,1],
                            turno, prefijo, correlativo, idven,
                            tiempo_reg, fecha, modo_oper_log, alm_ori,
                            alm_des,fecha, '1', masa, oper_log,
                            extra_data, doc_modo, doc_tipo, prefijo2,
                            correlativo2, transp_codigo,
                            vehiculo_codigo, observaciones, alm_base,
                            tiempo_reg, id_prov)
                        base=sqlsend(temporal_x,campos_bd,1)
                        sql = "insert into almacenes %s" % (base)
                        query_trans.append(sql)
                        if extra_oper_log==1:
                            temporal_y = agregar_valores(temporal,
                                [0,1], turno, prefijo2, correlativo2,
                                idven, tiempo_reg, fecha,
                                modo_oper_log2, alm_ori2, alm_des2,
                                fecha, '1', masa, oper_log2, extra_data,
                                doc_modo, doc_tipo, prefijo,
                                correlativo, transp_codigo,
                                vehiculo_codigo, observaciones,
                                alm_base, tiempo_reg, id_prov)
                            base2=sqlsend(temporal_y,campos_bd,1)
                            sql2="insert into almacenes %s" % (base2)
                            query_trans.append(sql2)
                if len(query_trans)>0:
                    if edit_guia!=2:
                        sql=set_correlativo(doc_modo,doc_tipo,correlativo,0)
                        query_trans.append(sql)
                        if extra_oper_log==1:
                            sql=set_correlativo(doc_modo,doc_tipo,correlativo2,0)
                            query_trans.append(sql)
                estado=query(query_trans,5)
                if estado==1:
                    if modo_oper_log[-1] == '1':
                        msg1='Nota de Ingreso'
                        msg2='Nota de Salida'
                        alm1=alm_ori
                        alm2=alm_des2
                    elif modo_oper_log[-1] == '2':
                        msg1='Nota de Salida'
                        msg2='Nota de Ingreso'
                        alm1=alm_des
                        alm2=alm_ori2
                    if tipo_mov==2:
                        if impresion==1:
                            impresion_guia_externa(doc_modo,doc_tipo,oper_log_pref,prefijo,correlativo,port_imp,layout)
                    else:
                        if impresion==1:
                            impresion_guia_interna(doc_modo,doc_tipo,oper_log_pref,prefijo,correlativo,port_imp,layout)
                    if extra_oper_log==1:
                        if impresion==1:
                            impresion_guia_interna(doc_modo,doc_tipo,oper_log_pref,prefijo2,correlativo2,port_imp,layout)
                    return 1
                elif estado==-1:
                    return -1
                elif estado==0:
                    return 0
                return 1
            elif ingdat=='arriba':
                psey-=1
            elif ingdat=='abajo':
                psey+=1
            temc=abs(psey)
            if temc>len(lineas):
                psey=0


panelmenu=mkpanel(curses.COLOR_WHITE,maxy,maxx,0,0)
fecha=time.strftime("%Y-%m-%d")
sumtot=0.00
contad=0


while 1:
    while nomven=='I':
        codven,nomven,nivel,idven=aut()
    while 1:
        print_buffer=''
        modo_almacen=0
        head='Central'
        #opc_menu = """1. Almacenes-Central|2. Almacenes-Produccion|
            #3. Almacenes-Distribucion|4. Almacenes-Mermas|
            #5. Almacenes-Finishing|7. Almacenes-Auxiliares|
            #8. Ventas|9. Salir"""
        opc_menu = """1. Almacen-Central|2. Almacen-Auxiliar|8. Ventas|9. Salir"""
        opcion = menu(opc_menu, head)
        #OPCION 1
        #if opcion==3:
            #modo_almacen=1
            #oper_log_pref='1'
            #doc_modo=1
            #doc_tipo_int=6
            #doc_tipo_ext=5
            #alm_relev='0101'
            #alm_base='0100'
            #head='Distribucion:0100'
        #elif opcion==2:
            #modo_almacen=1
            #oper_log_pref='2'
            #doc_modo=2
            #doc_tipo_int=6
            #doc_tipo_ext=5
            #alm_relev='0101'
            #alm_base='0101'
            #head='Produccion:0101'
        if opcion == 1:
            modo_almacen=1
            oper_log_pref=''
            doc_modo=3
            doc_tipo_int=2
            doc_tipo_ext=5
            alm_relev=''
            alm_base='1'
            head='Central: %s' % (alm_base)
        elif opcion == 2:
            modo_almacen=1
            oper_log_pref=''
            doc_modo=3
            doc_tipo_int=2
            doc_tipo_ext=5
            alm_relev=''
            alm_base='3'
            head='Auxiliar: %s' % (alm_base)
        #if opcion==4:
            #query_trans=[]
            #sql="insert into almacenes (modo,modo_doc,operacion_logistica,tiempo,estado,user_ing,tipo_doc,fecha_doc,n_doc_prefijo,n_doc_base,almacen_origen,almacen_destino,codbarras,ingreso,turno) select 81,8,'IXM',tiempo,estado,user_ing,tipo_doc,fecha_doc,n_doc_prefijo,n_doc_base,'0100','0021',codbarras,cantidad_ing,turno from almacenes where modo_doc=1 and modo=12 and operacion_logistica='SXM' and control=0 and estado=1 and fecha_doc>='2006-08-01';"
            #query_trans.append(sql)
            #sql="update almacenes set control=1 where modo_doc=1 and modo=12 and operacion_logistica='SXM' and control=0 and estado=1 and fecha_doc>='2006-08-01';"
            #query_trans.append(sql)
            #estado=query(query_trans,5)
            #modo_almacen=1
            #oper_log_pref='8'
            #doc_modo=8
            #doc_tipo_int=6
            #doc_tipo_ext=5
            #alm_relev='0003'
            #alm_base='0021'
            #head='Mermas:0021'
        #elif opcion==5:
            #modo_almacen=1
            #oper_log_pref='2'
            #doc_modo=2
            #doc_tipo_int=6
            #doc_tipo_ext=5
            #alm_relev='0101'
            #alm_base='0101'
            #head='Finishing:0300'
        #elif opcion==7:
            #print_buffer=' -P lx300wong'
            #modo_almacen=1
            #oper_log_pref='4'
            #doc_modo=4
            #doc_tipo_int=6
            #doc_tipo_ext=5
            #alm_relev='0100'
            #alm_base='0040'
            #head='Wong:0040'
        elif opcion==8:
            while 1:
                opcion2=menu('1. Operaciones|9. Regresar',head)
                if opcion2==1:
                    opcion3=menu('1. Ingreso de Ventas|2. Anulacion de Ventas|9. Regresar',head)
                    if opcion3==1:
                        ventas_proc(8)
                    elif opcion3==2:
                        anulacion_ventas()
                    elif opcion3==9:#Ingreso de Producto
                        pass
                else:
                    break
        #OPCION 9
        elif opcion==9:
            opcion2=menu('1.Cambiar Usuario|8.Cerrar Aplicacion|9.Regresar',head)
            if opcion2==1:
                codven=0
                nomven='I'
                nivel=0
                break
            elif opcion2==8 and nivel<5:
                curses.echo()
                curses.endwin()
                sys.exit()
            else:
                pass
        if modo_almacen==1:
            while 1:
                opcion2=menu('1. Operaciones|2. Reportes|9. Regresar',head)
                if opcion2==1:#Operaciones
                    opcion3=menu('i. Ingreso de Guias|1. Ingreso de Producto|2. Anulacion de Producto|3. Operaciones Internas|4. Anulacion Guias Internas|5. Operaciones Externas|6. Anulacion Guias Externas|m. Mermas de Tienda|c. Consumo Interno|r. Reimpresiones|9. Regresar',head)
                    ## data_proc(tipo_mov=1,doc_modo=1,doc_tipo=6,txt_fld=3,fech_cnt=1,fech_hea='t',turno_ing=1,masa_ing=1,impresion=1,oper_log='IPT',alm_rel='0101',alm_base='0100',oper_log_pref='1',add_data='',prod_filt='genero="0002"'):
                    if opcion3==1:#Ingreso de Producto
                        data_proc(1,doc_modo,doc_tipo_int,3,1,'t',1,1,1,'',alm_relev,alm_base,oper_log_pref,'')
                    elif opcion3==2:
                        data_proc(1,doc_modo,doc_tipo_int,3,1,'',1,0,1,'SAP',alm_base,alm_base,oper_log_pref,'')
                    elif opcion3==3:
                        data_proc(1,doc_modo,doc_tipo_int,3,1,'',0,0,1,'','',alm_base,oper_log_pref,'')
                    elif opcion3==4:
                        estado=anulacion_guia(doc_modo,doc_tipo_int,oper_log_pref)
                    elif opcion3==5:
                        data_proc(2,doc_modo,doc_tipo_ext,3,1,'',1,0,1,'','',alm_base,oper_log_pref,'')
                    elif opcion3==6:
                        estado=anulacion_guia(doc_modo,doc_tipo_ext,oper_log_pref)
                    elif opcion3=='m':
                        data_proc(1,doc_modo,doc_tipo_int,3,1,'',1,0,0,'IXM','',alm_base,oper_log_pref,'')
                    elif opcion3=='c':
                        data_proc(1,doc_modo,doc_tipo_int,3,1,'',1,0,0,'IKI','',alm_base,oper_log_pref,'')
                    elif opcion3=='r':
                        opcion4=menu('1. Internas|2. Externas|9. Regresar',head)
                        if opcion4==1:
                            estado=reimpresion_guia(doc_modo,doc_tipo_int,oper_log_pref)
                        elif opcion4==2:
                            estado=reimpresion_guia(doc_modo,doc_tipo_ext,oper_log_pref)
                        else:
                            pass
                    elif opcion3=='i':
                        data_proc(1,doc_modo,doc_tipo_int,3,1,'',0,0,1,'46','',alm_base,oper_log_pref,'2|Conv')
                    else:
                        break
                elif opcion2==2:#Reportes
                    opcion3=menu('1. Stocks|2. Kardex|9. Regresar',head)
                    modo_alm_ing=oper_log_pref+'1'
                    modo_alm_sal=oper_log_pref+'2'
                    if opcion3==1:
                        ver_imprimir(doc_modo,1,'',head)
                    elif opcion3==2:
                        ver_imprimir(doc_modo,0)
                else:
                    break
