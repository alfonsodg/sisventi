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
import crypt
import re
import types
import signal
import fpformat
import locale
import calendar
import zipfile
import glob
import md5
import logging
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
    in_file=open("data.cfg","r") # Opens the file
    params=in_file.read().splitlines()
    pos_num=params[0] # When a value is assigned, too is added the '\n' (non-visible character), then we omit it
    caja_num=params[1]
    print_port=params[2]
    host=params[3]
    database=params[4]
    user=params[5]
    pswd=params[6]
    n_serie=params[7]
    debug_mode=params[8]
    in_file.close() # close the file
except IOError:
    print 'Error al abrir el archivo de configuracion!!!!'
    sys.exit()
#####
try:
    in_file=open("export.cfg","r")
    lineas=in_file.read().splitlines()
    tablas={}
    for linea in lineas:
        partes=string.split(linea,'|')
        nombre_tabla=partes[0]
        tablas[nombre_tabla[1:]]=partes[1]
    in_file.close()
except:
    pass


#####
#Initialize Variables and Functions
#####
try:
    conn=MySQLdb.connect(db=database,host=host,user=user,passwd=pswd) # Starts the MySQL DB connection
except:
    print 'Error al conectarse con la base de datos!!!!'
    sys.exit()
conn.autocommit(True)
curs=conn.cursor()
stdscr=curses.initscr() # Initialize the call to the curses function
curses.start_color() # Initialize the color access
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # Assigns the color to the screen
curses.mousemask(curses.ALL_MOUSE_EVENTS) # Calls to the detection of mouse events (moves and clicks)
curses.noecho() # No returns a  character after a keypress
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
    win=curses.newwin(rows, cols, tly, tlx)
    pan=panel.new_panel(win)
    if curses.has_colors():
        if color==curses.COLOR_BLUE:
            fg=curses.COLOR_WHITE
        else:
            fg=curses.COLOR_BLACK
        bg=color
        curses.init_pair(color, color, curses.COLOR_BLACK)
        win.bkgdset(ord(' '), curses.color_pair(color))
    else:
        win.bkgdset(ord(' '), curses.A_BOLD)
    return pan


##Reads the Configuration of POS
def configurat():
    fecha_act=time.strftime("%Y-%m-%d")
    impuestos={}
    sql="""select doc_cabecera,doc_pie,modo_impuesto,impuestos,
    modo_moneda,moneda,money_drawer,productos_resumen,productos_clave,
    empresa,tipo_servicio,wincha,servidor_smtp,from_smtp,to_smtp,
    fondo_caja from pos_configuracion where id='%s'""" % (pos_num)
    cnt,rso=query(sql,0)
    if cnt==0:
        curses.echo()
        curses.endwin()
        print "Error en la Configuracion!....."
        sys.exit()
    doc_cabecera=string.split(rso[0],'-/n/-')
    doc_pie=string.split(rso[1],'-/n/-')
    modo_imp=rso[2]
    imp_partes=string.split(rso[3],',')
    for parte in imp_partes:
        temp=string.split(parte,':')
        impuestos[temp[1]]=temp[0]
    modmon=rso[4]
    moneda=rso[5]
    gaveta=rso[6]
    prod_resumen=string.split(rso[7],',')
    prod_clave=string.split(rso[8],',')
    empresa=rso[9]
    tipo_servicio=str(rso[10])
    wincha=str(rso[11])
    servidor_smtp=str(rso[12])
    from_smtp=str(rso[13])
    to_smtp=str(rso[14])
    fondo_caja=rso[15]
    try:
        fondo_caja=float(fondo_caja)
    except:
        fondo_caj=0.00
    sql="select valor from tipos_cambio where fecha='"+str(fecha_act)+"' or fecha='0000-00-00' order by fecha desc limit 1"
    cnt_1,rso_1=query(sql,0)
    if cnt_1==0:
        segur("Advertencia: No existe Tipo de Cambio Definido")
        tipo_cambio=1
    else:
        tipo_cambio=rso_1[0]
    return doc_cabecera,doc_pie,modo_imp,impuestos,modmon,moneda,tipo_cambio,gaveta,prod_resumen,prod_clave,empresa,tipo_servicio,wincha,servidor_smtp,from_smtp,to_smtp,fondo_caja


##User Authorization Routine
def aut():
    """
    Authorization scheme
    """
    curses.curs_set(1)
    updat()
    pan = mkpanel(curses.COLOR_WHITE, maxy, maxx, 0, 0)
    win = definewin(pan,0,1)
    msg = "Modulo: Administracion"
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
def derecha(x,cadena):
    posx=x-len(cadena)
    return posx


##Aligns to center any phrase
def centrar(x,cadena):
    posx=(x/2)-(len(cadena)/2)
    return posx


##Do the Query, sending 1 or Multiple results
def query(sql,ndat=1):
    if ndat==3:
        try:
            curs.execute("START TRANSACTION")
            curs.execute(sql)
            curs.execute("COMMIT")
            return 1
        except MySQLdb.Error, error:
            curs.execute("ROLLBACK")
            resp=segur("ERROR. INFORMACION NO REGISTRADA.")
            logging.debug("Query: %s" % error)
            logging.debug("Query-Detail: %s" % sql)
            return -1
    elif ndat==5:
        try:
            curs.execute("START TRANSACTION")
            for query in sql:
                curs.execute(query)
            curs.execute("COMMIT")
            return 1
        except MySQLdb.Error, error:
            curs.execute("ROLLBACK")
            resp=segur("ERROR. INFORMACION NO REGISTRADA.")
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
def menu(menudata):
    pan=mkpanel(curses.COLOR_WHITE,maxy,maxx,0,0)
    datatemp=string.split(menudata,'|')
    opciones={}
    win=definir(pan)
    texto='MENU'
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
        if c==curses.KEY_LEFT and tipo==0:return 'izquierda'
        if c==curses.KEY_RIGHT and tipo==0:return 'derecha'
        if c==curses.KEY_BACKSPACE or c==127:return 'backspace'
        if c==10:return 'enter'
        if c==curses.KEY_IC and tipo==0:return 'insert'
        if c==curses.KEY_DC and tipo==0:return 'borrar'
        if c==curses.KEY_NPAGE and tipo==0:return 'spag'
        if c==curses.KEY_PPAGE and tipo==0:return 'ppag'
        if c==curses.KEY_F12 and tipo==0: return 'f12'
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
def set_tipo_cambio(fecha):
    sql="select valor from tipos_cambio where fecha='"+fecha+"'"
    cuenta,resultado=query(sql,0)
    if cuenta==0:
        sql="select valor from tipos_cambio where fecha='0000-00-00'"
        cuenta_1,resultado_1=query(sql,0)
        data=resultado_1[0]
    else:
        data=resultado[0]
    return round(float(data),2)


def tiempocaja(tiempo='d'):
    if tiempo=='d':
        sql="select apertura,cierre from pos_administracion where pv="+str(pos_num)+" and caja="+str(caja_num)+" order by id desc"
    else:
        sql="select apertura,cierre from pos_administracion where pv="+str(pos_num)+" and caja="+str(caja_num)+" and apertura like '"+str(tiempo)+"%' order by id desc"
    cuenta,resultado=query(sql,0)
    if cuenta==0:
        apertura='0000-00-00 00:00:00'
        cierre='2999-12-30 23:59:59'
    else:
        apertura=resultado[0]
        cierre=resultado[1]
        if cierre=='0000-00-00 00:00:00' or cierre is None:
            cierre='2999-12-30 23:59:59'
    apertura=str(apertura)
    apertura=apertura[:19]
    cierre=str(cierre)
    cierre=cierre[:19]
    return str(apertura),str(cierre)


##Tax Calculation // monto=dinero,impto=impuesto a determinar
def valorimpuesto(monto,impto=''):
    tot_impto=0
    val_impto=0
    for llave in impuestos:
        tot_impto+=float(impuestos[llave])
    if impto!='':
        val_impto=float(impuestos[impto])
    if modo_imp==1 or modo_imp=='1':
        tot_impto+=100
        if impto=='':
            val_impto=100
    else:
        val_impto=tot_impto
        tot_impto=100
    mnt_impto=round((val_impto*monto)/tot_impto,2)
    return mnt_impto


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
        opcn=obch(pan)
        if opcn=='arriba':
            if posicion==0:
                posicion=0
            else:
                posicion=posicion-1
        elif opcn=='abajo':
            if posicion==(cuenta-1):
                posicion=(cuenta-1)
            else:
                posicion=posicion+1
        elif opcn=='enter':
            return posdata[posicion][rotulo],posdata[posicion][identif]
        elif opcn=='escape':
            return 'Anular','Anular'


def poscr(siz_win,siz_scr):
    dato=(siz_scr-siz_win)/2
    return dato


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
    panel=mkpanel(curses.COLOR_WHITE,sizey,sizex,posy,posx)
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
def strimpr(texto,py,tx,win='',ubicacion='c'):
    texto=str(texto)
    if ubicacion=='c' or ubicacion=='centrar' or ubicacion=='centro':
        px=centrar(tx,texto)
    else:
        px=derecha(tx,texto)
    win.addstr(py,px,texto)
    return


##Simple true/false question
def segur(msg='',posy=-1,posx=-1):
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


def menopc(relaciones,opciones,data):
    orden=opciones.keys()
    orden.sort()
    posy=(maxy-(len(orden)+2))/2
    posx=(maxx-22)/2
    pan=mkpanel(curses.COLOR_WHITE,len(orden)+2,22,posy,posx)
    win=definir(pan)
    pcy=1
    while 1:
        cy=0
        slx=''
        for x in orden:
            cy+=1
            if cy==pcy:
                slx=str(x)
                win.addstr(cy,1,str(x)+'. '+str(opciones[x]),curses.A_REVERSE)
                updat()
            else:
                win.addstr(cy,1,str(x)+'. '+str(opciones[x]))
                updat()
        opcion=obch(pan)
        if opcion=='arriba':
            if pcy <= 1:
                pcy= 1
            else:
                pcy-=1
        elif opcion=='abajo':
            if pcy >= len(orden):
                pcy=len(orden)
            else:
                pcy=pcy+1
        elif opcion=='escape':
            return 0,0
        elif opcion=='enter':
            pcy2=1 #Seleccion en Y
            cont=len(relaciones[slx]) #cuenta elementos
            relaciones[slx].sort()
            posy=(maxy-(cont+2))/2
            posx=(maxx-50)/2
            tamy=cont #Tamano de Y
            inic=0#Inicio de Array
            term=cont#Termino de Array
            if cont >= maxy:
                tamy=maxy-2
                posy=0
                inic=0
                term=maxy-2
            pan2=mkpanel(curses.COLOR_WHITE,tamy+2,50,posy,posx)
            win2=definir(pan2)
            while 1:
                cy2=0 # Contador
                slp=''
                for z in range(inic,term):
                    cy2+=1
                    opk=relaciones[slx][z]
                    if cy2 == pcy2:
                        slp=opk
                        win2.addstr(cy2,1,' '*48)
                        win2.addstr(cy2,1,opk+'. '+data[opk],curses.A_REVERSE)
                    elif cy2 < maxy-1:
                        win2.addstr(cy2,1,' '*48)
                        win2.addstr(cy2,1,opk+'. '+data[opk])
                    updat()
                opcion2=obch(pan2)
                if opcion2=='arriba':
                    if pcy2<= 1:
                        if cont>=maxy and inic>0:
                            inic-=1
                            term-=1
                        else:
                            pcy2=1
                    else:
                        pcy2-=1
                elif opcion2=='abajo':
                    if pcy2>=tamy:
                        if cont>=maxy and term<cont:
                            inic+=1
                            term+=1
                        else:
                            pcy2=tamy
                    else:
                        pcy2+=1
                elif opcion2=='enter':
                    return slx,slp
                elif opcion2=='escape':
                    borscr(pan2)
                    break


##Report Header, Writes an ASCII file
def cabecera(archivo,tipo):
    tiempo=time.strftime("%Y-%m-%d %H:%M:%S")
    texto=string.center(empresa,40)
    archivo.write(texto+'\n')
    if tipo==1:
        cab='X CORTA'
    elif tipo==2:
        cab='X LARGA'
    elif tipo==3:
        cab='Z'
    texto=string.center('REPORTE '+cab,40)
    archivo.write(texto+'\n')
    texto=string.center('TIENDA: '+str(pos_num),40)
    archivo.write(texto+'\n')
    texto=string.center('CAJA: '+str(caja_num),40)
    archivo.write(texto+'\n')
    archivo.write('\n')
    texto=string.center(str(tiempo),40)
    archivo.write(texto+'\n')
    for cnt in range(0,4):
        archivo.write('\n')
    return


##Footer or Back Resume of Operations
def pie(archivo):
    diferencia=abs(total_real-sumtot)
    texto=string.ljust('Diferencia FP:',15)+string.center(' ',10)+string.rjust(cardec(diferencia),15)
    archivo.write(texto+'\n')
    texto=string.ljust('Monto '+moneda+':',15)+string.center(' ',10)+string.rjust(cardec(mntsol),15)
    archivo.write(texto+'\n')
    texto=string.ljust('Monto $:',15)+string.center(' ',10)+string.rjust(cardec(mntdol),15)
    archivo.write(texto+'\n')
    texto=string.ljust('Anulaciones:',15)+string.center(cardec(nuls),10)+string.rjust(cardec(anulaciones),15)
    archivo.write(texto+'\n')
    texto=string.ljust('Total Neto:',15)+string.center(' ',10)+string.rjust(cardec(valorimpuesto(sumtot,'')),15)
    archivo.write(texto+'\n')
    for impuesto in impuestos:
        imp_dscp=str(impuesto)+' '+str(impuestos[impuesto])+'%:'
        texto=string.ljust(imp_dscp,15)+string.center(' ',10)+string.rjust(cardec(valorimpuesto(sumtot,impuesto)),15)
        archivo.write(texto+'\n')
    texto=string.ljust('Total Bruto:',15)+string.center(' ',10)+string.rjust(cardec(sumtot),15)
    archivo.write(texto+'\n')
    archivo.write('\n')
    archivo.write('\n')
    return


##Method of Payment, Report Calculation
def payment_options(apertura,cierre,archivo=''):
    sumtot=0.00
    anulaciones=0
    mntdol=0.00
    mntsol=0.00
    nuls=0 #Anulaciones
    transacciones=0
    total_real=0
    lineas=[]
    condicion_doc = " and doc.ext_doc=0"
    if cierre == '0000-00-00 00:00:00':
        cierre=apertura
    condicion = """doc.fecha_vta between date('%s') and
        date('%s')""" % (apertura, cierre)
    sql = """select cast(id as CHAR),nombre,modo from formas_pago"""
    cuenta,resultado=query(sql)
    metodo_pago={}
    for linea in resultado:
        fp=str(linea[0])
        modo_fp=str(linea[2])
        metodo_pago[fp]={}
        metodo_pago[fp]['nam']=linea[1]
        metodo_pago[fp]['mod']=modo_fp
        metodo_pago[fp]['mnt']=0.0
        metodo_pago[fp]['tra']=0
    sql = """select doc.estado,doc.medios_pago,doc.total,doc.n_doc_base
        from docventa doc where %s and doc.caja='%s' and doc.pv='%s' %s
        group by doc.estado,doc.n_doc_base order by doc.estado,
        doc.n_doc_base""" % (condicion, caja_num, pos_num,
        condicion_doc)
    cuenta,resultado=query(sql)
    for linea in resultado:
        estado=str(linea[0])
        medios_pago=linea[1]
        monto=float(linea[2])
        mp_tmp=string.split(medios_pago,'|')
        mp_det=[]
        mp_def={}
        for parte in mp_tmp:
            mp_det=string.split(parte,':')
            mp_def[mp_det[0]]=round(float(mp_det[1]),2)
        if estado=='0':
            nuls+=1
            for mp in mp_def:
                mp_temp=str(mp)
                if metodo_pago.has_key(mp):
                    pass
                else:
                    metodo_pago[mp_temp]={}
                    metodo_pago[mp_temp]['nam']='ND'
                    metodo_pago[mp_temp]['mod']='0'
                    metodo_pago[mp_temp]['mnt']=mp_def[mp]
                    metodo_pago[mp_temp]['tra']=0
            anulaciones+=float(monto)
        else:
            transacciones+=1
            for mp in mp_def:
                mp_temp=str(mp)
                if metodo_pago.has_key(mp):
                    metodo_pago[mp_temp]['mnt']+=mp_def[mp]
                    metodo_pago[mp_temp]['tra']+=1
                else:
                    metodo_pago[mp_temp]={}
                    metodo_pago[mp_temp]['nam']='ND'
                    metodo_pago[mp_temp]['mod']='0'
                    metodo_pago[mp_temp]['mnt']=mp_def[mp]
                    metodo_pago[mp_temp]['tra']=0
                if metodo_pago[mp_temp]['mod']=='1':
                    mntsol+=mp_def[mp]
                total_real+=mp_def[mp]
            sumtot+=float(monto)
    for mp in metodo_pago:
        mp_nam=metodo_pago[mp]['nam']
        mp_tra=metodo_pago[mp]['tra']
        mp_mnt=metodo_pago[mp]['mnt']
        if archivo!='':
            texto=string.ljust(str(mp_nam),15)+string.rjust(str(mp_tra),10)+string.rjust(cardec(mp_mnt),15)
            archivo.write(texto+'\n')
        else:
            prov=[]
            prov.append(str(mp_nam))
            prov.append(str(mp_tra))
            prov.append(cardec(mp_mnt))
            lineas.append(prov)
    if archivo!='':
        texto=string.ljust(' ',15)+string.center('----------',10)+string.rjust(' ',15)
        archivo.write(texto+'\n')
        texto=string.ljust('Total FP:',15)+string.rjust(' ',10)+string.rjust(cardec(total_real),15)
        archivo.write(texto+'\n')
        texto=string.ljust('Trans. Total:',15)+string.rjust(str(transacciones),10)+string.rjust(' ',15)
        archivo.write(texto+'\n')
    sql = """select distinct(doc.n_doc_base),doc.mntdol from
        docventa doc where %s and doc.caja='%s' and doc.pv='%s' and
        doc.estado='1' and doc.mntdol>0 %s""" % (condicion, caja_num,
        pos_num, condicion_doc)
    cuenta,resultado=query(sql)
    for linea in resultado:
        mntdol += float(linea[1])
    mntsol = round(mntsol-(mntdol*tipo_cambio),2)
    total_real = round(total_real,2)
    if archivo=='':
        prov=agregar_valores([],0,'-------','-------','-------')
        lineas.append(prov)
        prov=agregar_valores([],0,moneda,'$','TOTAL')
        lineas.append(prov)
        prov=agregar_valores([],0,'-------','-------','-------')
        lineas.append(prov)
        prov=agregar_valores([],0,round(mntsol,2),round(mntdol,2),round(sumtot,2))
        lineas.append(prov)
        prov=agregar_valores([],0,'FONDO CAJA','',round(fondo_caja,2))
        lineas.append(prov)
        for impuesto in impuestos:
            prov=agregar_valores([],0,impuesto,'',valorimpuesto(sumtot,impuesto))
            lineas.append(prov)
        prov=agregar_valores([],0,'NETO','',valorimpuesto(sumtot,''))
        lineas.append(prov)
        prov=agregar_valores([],0,'TOTAL CON FONDO CAJA','',round(fondo_caja+sumtot,2))
        lineas.append(prov)
        prov=agregar_valores([],0,'-------','-------','-------')
        lineas.append(prov)
        doc_m = doc_man(apertura)
        docm_tot = 0
        for linea in doc_m:
            temporal=[]
            parte=string.split(linea,':')
            temporal.append(string.strip(str(parte[0])))
            temporal.append('')
            mnt_man=string.strip(str(parte[1]))
            docm_tot+=float(mnt_man)
            temporal.append(mnt_man)
            lineas.append(temporal)
        prov=agregar_valores([],0,'-------','-------','-------')
        lineas.append(prov)
        prov=agregar_valores([],0,'TOTAL VENTAS A/M','',round(sumtot+docm_tot,2))
        lineas.append(prov)
        return lineas
    else:
        return round(mntsol,2),round(mntdol,2),str(nuls),round(anulaciones,2),round(sumtot,2),round(total_real,2)


def vales(apertura,cierre,modo='0',archivo=''):
    sql="select distinct codigo,nombre,porcentaje,valor from promociones order by codigo asc"
    cuenta,resultado=query(sql,1)
    vales={}
    condicion_doc=''
    if archivo!='':
        condicion_doc=" and ext_doc=0"
    for x in resultado:
        vales[x[0]]=[]
        vales[x[0]].append(x[1])
        vales[x[0]].append(x[2])
        vales[x[0]].append(x[3])
        vales[x[0]].append([])
    for x in range(0,cuenta):
        if cierre=='0000-00-00 00:00:00':
            cierre=apertura
#           condicion="tiempo between '"+apertura+"' and '"+cierre+"'"
#       else:
#           condicion="tiempo>='"+apertura+"'"
        condicion="fecha_vta between date('"+apertura+"') and date('"+cierre+"')"
        sql = """select n_doc_base,sello,total from docventa where
            vales like '%%%s%%'  and caja='%s' and pv='%s' and %s %s
            and estado='1' group by n_doc_base order by
            n_doc_base""" % (resultado[x][0], caja_num, pos_num,
            condicion, condicion_doc)
        cuenta2,resultado2=query(sql,1)
        if len([resultado[x][0]])>0:
            for y in resultado2:
                vales[resultado[x][0]][3].append(y)
        if cuenta2>0:
            for vale in vales.keys():
                valora=0
                if vales[vale][2]!=0:
                    valora=len(vales[vale][3])*vales[vale][2]
                cadena=string.ljust(str(vale),15)+string.center(str(len(vales[vale][3])),10)+string.rjust(cardec(valora),15)
                if archivo!='':
                    archivo.write('VALES:\n')
                    archivo.write(cadena+'\n')
                if modo=='1':
                    for dato in vales[vale][3]:
                        cadena=string.ljust(str(vales[vale][1]),15)+string.center(str(dato[1]),10)+string.rjust(str(dato[2]),15)
                        archivo.write(cadena+'\n')
                    archivo.write('\n')
                    archivo.write('\n')
                if archivo!='':
                    archivo.write('<----->\n')
        else:
            vales={}
    return vales


##Documents Report
def comprobantes(apertura,cierre,archivo):
    txt_estado=''
    if cierre=='0000-00-00 00:00:00':
        cierre=apertura
    condicion = """doc.fecha_vta between date('%s') and
        date('%s')""" % (apertura, cierre)
    sql = """select doc.estado,doc.comprobante,fpa.nombre,
        count(distinct(doc.n_doc_base)) as cnt,sum(sub_total_bruto)
        as mnt from docventa doc left join documentos_comerciales
        fpa on fpa.id=doc.comprobante where %s and doc.caja='%s'
        and doc.pv='%s' and doc.ext_doc=0 group by doc.estado,
        doc.comprobante order by doc.estado,
        doc.comprobante""" % (condicion, caja_num, pos_num)
    cuenta,resultado=query(sql,1)
    for linea in resultado:
        estado=linea[0]
        if estado=='1':
            txt_estado=str(linea[2])+' OK:'
        elif estado=='0':
            txt_estado=str(linea[2])+' Nul:'
        texto=string.ljust(txt_estado,15)+string.center(str(linea[3]),10)+string.rjust(cardec(linea[4]),15)
        archivo.write(texto+'\n')
    return


##Product (By Codes) Report
def codigo(apertura,cierre,archivo):
    if cierre=='0000-00-00 00:00:00':
        cierre=apertura
    condicion="doc.fecha_vta between date('"+apertura+"') and date('"+cierre+"')"
    sql = """select doc.codigo,if(length(mae.alias)>0,
        left(mae.alias,29),left(concat(mae.nombre,' ',
        mae.descripcion),29)) as producto,doc.cantidad as cnt,
        doc.precio as precio,sub_codbarras from docventa doc
        left join maestro mae on mae.id=doc.codigo
        where %s and doc.estado='1' and doc.pv='%s' and
        doc.caja='%s' and doc.ext_doc=0""" % (condicion, pos_num,
        caja_num)
    cuenta,resultado=query(sql,1)
    sub_prod={}
    prod={}
    for linea in resultado:
        producto=linea[0]
        dsc_producto=linea[1]
        cnt_producto=linea[2]
        prc_producto=linea[3]
        sub_productos=linea[4]
        if len(sub_productos)>0:
            sub_productos=string.split(sub_productos,'>')
            for sub in sub_productos:
                tmp=string.split(sub,'|')
                for elem in tmp:
                    try:
                        tmp2=string.split(elem,':')
                        if sub_prod.has_key(tmp2[0]):
                            sub_prod[tmp2[0]]['cnt']+=float(tmp2[1])
                        else:
                            sub_prod[tmp2[0]]={}
                            sub_prod[tmp2[0]]['cnt']=float(tmp2[1])
                    except:
                        pass
        if prod.has_key(producto):
            prod[producto]['cnt']+=cnt_producto
        else:
            prod[producto]={}
            prod[producto]['nam']=str(dsc_producto)
            prod[producto]['prc']=float(prc_producto)
            prod[producto]['cnt']=float(cnt_producto)
    for codigo in prod:
        texto=string.ljust(str(codigo),10)+string.ljust(prod[codigo]['nam'],30)
        archivo.write(texto+'\n')
        texto=string.ljust('Cantidad',10)+string.center(' ',15)+string.rjust(str(prod[codigo]['cnt']),15)
        archivo.write(texto+'\n')
        mnt_bruto=round(prod[codigo]['cnt']*prod[codigo]['prc'],2)
        texto=string.ljust('Bruto',10)+string.center(' ',15)+string.rjust(cardec(mnt_bruto),15)
        archivo.write(texto+'\n')
        texto=string.ljust('Neto',10)+string.center(' ',15)+string.rjust(cardec(valorimpuesto(mnt_bruto,'')),15)
        archivo.write(texto+'\n')
#   texto=string.ljust(' ',10)+string.center('----------',15)+string.rjust(' ',15)
    texto=string.ljust('----------',40)
    archivo.write(texto+'\n')
    for codigo in sub_prod:
        try:
            dsc,prc=producto_data(codigo)
            texto=string.ljust(str(codigo),10)+string.ljust(dsc[:29],30)
            archivo.write(texto+'\n')
            texto=string.ljust('Cnt:',10)+string.center(' ',15)+string.rjust(str(sub_prod[codigo]['cnt']),15)
            archivo.write(texto+'\n')
        except:
            pass
    texto=string.ljust('----------',40)
    archivo.write(texto+'\n')
    return


##Salesmen Report
def usuarios(apertura,cierre,archivo):
    if cierre=='0000-00-00 00:00:00':
        cierre=apertura
    condicion = """doc.fecha_vta between date('%s') and date('%s')
        """ % (apertura, cierre)
    sql = """select count(distinct(doc.n_doc_base)) as cnt,doc.cv_ing,
    concat(usu.first_name,' ',usu.last_name) as usr,
    substring_index(doc.medios_pago,':',1) as f_pag,fpa.nombre,
    sum(sub_total_bruto) as mnt from docventa doc left join auth_user
    usu on usu.id=doc.cv_ing left join formas_pago fpa on
    fpa.id=substring_index(doc.medios_pago,':',1) where
    doc.estado='1' and doc.pv='%s' and doc.caja='%s' and doc.ext_doc=0
    and %s group by doc.cv_ing,f_pag""" % (pos_num, caja_num, condicion)
    cuenta,resultado=query(sql)
    cod_usr=''
    total_op=0
    total_mnt=0
    cnt=0
    for linea in resultado:
        foot=0
        if cod_usr!=str(linea[1]):
            if cnt>0:
                texto=string.ljust('----- Sub Total:',25)+string.rjust(str(total_op),5)+string.rjust(str(total_mnt),10)
                archivo.write(texto+'\n')
            texto=string.ljust(str(linea[1])+'-'+str(linea[2]),40)
            archivo.write(texto+'\n')
            total_op=0
            total_mnt=0
        total_op+=int(linea[0])
        total_mnt+=float(linea[5])
        texto=string.ljust('->'+str(linea[3])+'-'+str(linea[4]),25)+string.rjust(str(linea[0]),5)+string.rjust(cardec(linea[5]),10)
        archivo.write(texto+'\n')
        cod_usr=str(linea[1])
        cnt+=1
        if cnt==cuenta or foot==1:
            texto=string.ljust('----- Sub Total:',25)+string.rjust(str(total_op),5)+string.rjust(cardec(total_mnt),10)
            archivo.write(texto+'\n')
    return


##Transaction by Hour Report
def horas(apertura,cierre,archivo):
    if cierre=='0000-00-00 00:00:00':
        cierre=apertura
    condicion = """doc.fecha_vta between date('%s') and
        date('%s')""" % (apertura,cierre)
    sql = """select count(distinct(doc.n_doc_base)) as cnt,
        date(doc.tiempo),concat(lpad(hour(doc.tiempo),2,'0'),':00')
        as hora,sum(sub_total_bruto) as mnt from docventa doc
        where %s and doc.estado='1' and doc.pv='%s' and doc.caja='%s'
        and doc.ext_doc=0 group by date(doc.tiempo),
        hour(doc.tiempo)""" % (condicion, pos_num, caja_num)
    cuenta,resultado=query(sql)
    for linea in resultado:
        fecha=str(linea[1])
        texto=string.ljust(str(fecha[:10]),10)+string.rjust(str(linea[2]),10)+string.rjust(cardec(linea[0]),10)+string.rjust(cardec(linea[3]),10)
        archivo.write(texto+'\n')
    return


##Ticket Header (Void Operations)
def ticket(archivo,compr_detalle,cadena,hora=''):
    if hora=='':
        hora=time.strftime("%Y-%m-%d %H:%M:%S")
    for cabecera in doc_cabecera:
        linea=string.center(cabecera[:38],38)
        archivo.write(linea+'\n')
    archivo.write('\n')
    nodoc=cadena[0][12]
    cdv=cadena[0][2]
    vend_temp=string.split(cadena[0][3],' ')
    nombre_vendedor=vend_temp[0][:10]
    forpa=cadena[0][1]
    formapago=forpa[:6]
    tiempo=str(cadena[0][9])
    docnum=cadena[0][10]
    nombr=cadena[0][11]
    total=float(cadena[0][8])
    ##Caracteristicas del Documento
    linea=string.ljust('Tda:'+str(pos_num),10)+string.ljust('Caja:'+str(caja_num),8)+string.rjust(tiempo[:19],20)
    archivo.write(linea+'\n')
    linea=string.ljust('No:'+str(nodoc),10)+string.center('Usr:'+str(cdv)+'-'+str(nombre_vendedor),18)+string.rjust('Fpg:'+str(formapago),10)
    archivo.write(linea+'\n')
    ##Documento con Detalles
    if compr_detalle==1:
        linea=string.ljust('Cliente: '+nombr,38)
        archivo.write(linea+'\n')
        linea=string.ljust('RUC: '+str(docnum),38)
        archivo.write(linea+'\n')
    linea='-'*38
    archivo.write(linea+'\n')
    archivo.write('\n')
    for linea in cadena:
        valor=fpformat.fix(linea[7],2)
        nomb_desc=str(linea[6])
        linea=string.ljust(str(linea[4]),4)+string.ljust(nomb_desc[:27],27)+string.rjust('-'+str(valor),7)
        archivo.write(linea+'\n')
    archivo.write('\n')
    ##Sub Total
    stot=fpformat.fix(str(valorimpuesto(total,'')),2)
    linea=string.ljust('Sub Total: ',20)+string.rjust('-'+stot,18)
    archivo.write(linea+'\n')
    ##Impuestos
    for impuesto in impuestos:
        valor=fpformat.fix(valorimpuesto(total,impuesto),2)
        etiqueta=str(impuesto)+' '+str(impuestos[impuesto])+'% '
        linea=string.ljust(etiqueta,20)+string.rjust('-'+valor,18)
        archivo.write(linea+'\n')
    ##Total
    total=fpformat.fix(str(total),2)
    linea=string.ljust('Total '+moneda,20)+string.rjust('-'+total,18)
    archivo.write(linea+'\n')
    archivo.write('\n')
    linea='-'*38
    archivo.write(linea+'\n')
    texto='Serie de Equipo: '+ident
    linea=string.center(texto,38)
    archivo.write(linea+'\n')
    archivo.write('\n')
    texto=string.center(str(hora),38)
    archivo.write(texto+'\n')
    texto=string.center('ANULACION DE DOCUMENTO',38)
    archivo.write(texto+'\n')
    for linea in range(0,9):
        archivo.write('\n')
    return


##WareHouse Report
def almacen(apertura,cierre='4',modo=0):
    lineas=[]
    relalm={}
    if modo==5:
        condtiempo=apertura
        parte=float(cierre)
    else:
        condtiempo=" between date('"+apertura+"') and date('"+cierre+"')"
    sql="(select doc.codigo,doc.precio,sum(doc.cantidad),if(length(mae.alias)>0,mae.alias,concat(mae.nombre,' ',mae.descripcion)) as padre,if(rec.codbarras_hijo!='NULL',rec.codbarras_hijo,'ERROR') as codigo_hijo,if(rec.codbarras_hijo!='NULL',if(length(ma2.alias)>0,ma2.alias,concat(ma2.nombre,' ',ma2.descripcion)),'DSCP ERROR') as dscp_hijo,if(rec.codbarras_hijo!='NULL',rec.cantidad,0) as cnt,if(rec.codbarras_hijo!='NULL',sum(doc.cantidad)*rec.cantidad,0) as cons from docventa doc left join maestro mae on mae.codbarras=doc.codigo left join recetas rec on rec.codbarras_padre=doc.codigo and rec.modo=0 and (rec.tipo=doc.dist_type or rec.tipo=2) left join maestro ma2 on ma2.codbarras=rec.codbarras_hijo where doc.estado='B' and doc.fecha_vta "+condtiempo+" and doc.pv="+str(pos_num)+" group by doc.codigo,rec.codbarras_hijo order by doc.codigo,rec.codbarras_hijo)"
    sql+=" union "
    sql+="(select aux.codbarras_auxiliar,mae.precio,sum(aux.cantidad_auxiliar),if(length(mae.alias)>0,mae.alias,concat(mae.nombre,' ',mae.descripcion)) as padre,ifnull(if(aux.codbarras_auxiliar!='NULL',rec.codbarras_hijo,'ERROR'),'') as codigo_hijo,ifnull(if(aux.codbarras_auxiliar!='NULL',if(length(ma2.alias)>0,ma2.alias,concat(ma2.nombre,' ',ma2.descripcion)),'DSCP ERROR'),'') as dscp_hijo,ifnull(if(aux.codbarras_auxiliar!='NULL',rec.cantidad,0),'') as cnt,ifnull(if(aux.codbarras_auxiliar!='NULL',sum(aux.cantidad_auxiliar)*rec.cantidad,0),0) as cons from operaciones_vta_aux aux left join maestro mae on mae.codbarras=aux.codbarras_auxiliar left join recetas rec on rec.codbarras_padre=aux.codbarras_auxiliar and rec.modo=0 and rec.tipo=2 left join maestro ma2 on ma2.codbarras=rec.codbarras_hijo where aux.n_doc_base in (select n_doc_base from docventa where estado='B' and fecha_vta "+str(condtiempo)+" and pv="+str(pos_num)+" group by n_doc_base) group by aux.codbarras_auxiliar,rec.codbarras_hijo order by aux.codbarras_auxiliar,rec.codbarras_hijo)"
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
            if resultado[x][5] is None:
                nombrebase=''
            else:
                nombrebase=resultado[x][5][:30]
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
                        if prod_clave.count(codigob)>0:
                            prov=agregar_valores([],0,codigob,relalm[codigob],nombrebase)
                            lineas.append(prov)
                            n=1
                    elif modo==3:
                        if prod_clave.count(codigob)>0:
                            prov=agregar_valores([],0,codigob,nombrebase,relalm[codigob])
                            lineas.append(prov)
                            prov=[]
                            prov.append('================================================================')
                            lineas.append(prov)
                            n=1
                    elif modo==5:
                        if prod_clave.count(codigob)>0:
                            cantid=float(relalm[codigob])
                            prov=agregar_valores([],0,codigob,cantid,round(cantid/parte),nombrebase)
                            lineas.append(prov)
                            n=1
                if modo==1:
                    prov=agregar_valores([],0,codigoventas,nombreprven,'',cantidadven)
                    lineas.append(prov)
                elif modo==3:
                    if prod_clave.count(codigob)>0:
                        prov=agregar_valores([],0,codigoventas,nombreprven,'',cantidadven)
                        lineas.append(prov)
            if x==(cuenta-1):
                if modo==1:
                    for paso in range(0,3):
                        prov=[]
                        prov.append('>---<')
                        lineas.append(prov)
                elif modo==3:
                    if prod_clave.count(codigob)>0:
                        for paso in range(0,3):
                            prov=[]
                            prov.append('>---<')
                            lineas.append(prov)
    return lineas


def permisos_acceso(modo,usuario,opcion):
    sql="select estado from accesos_permisos where opcion='"+str(opcion)+"' and usuario='"+str(usuario)+"'"
    cuenta,resultado=query(sql,0)
    if cuenta>0:
        acceso=int(resultado[0])
        if acceso==0:
            permiso=0
            segur("No tiene Permisos para Acceder a este Modulo")
        else:
            permiso=1
    else:
        permiso=1
    return permiso


##POS ID
def idd(modo=0):
    if modo==0:
        a=os.popen('cat /proc/pci')
        ident=a.read()
        a.close()
        ident=str(pos_num)+str(caja_num)+ident
        ident=crypt.crypt(ident,'0-9')
    else:
        ident=str(n_serie)
    return ident


##Prints line into file (text)
def linea_imp(archivo,lineas=1):
    for cnt in range(0,lineas):
        archivo.write('\n')
    return


##Send to Printer
def impresion(nomarch,gaveta):
    if debug_mode=='0' or debug_mode=='':
        if gaveta=='':
            os.system('/bin/cat apertura | escpos > '+print_port)
        else:
            os.system('ls > /dev/'+gaveta)
        if print_port[5:9]!='ttyS':
            os.system('/bin/cat '+nomarch+' > '+print_port)
            os.system('/bin/cat corte | escpos > '+print_port)
        else:
            impresion_serial(nomarch)
    return


def impresion_serial(nomarch):
    fichero = open(nomarch,"r")
    tlineas=0
    for linea in fichero:
        tlineas+=1
    fichero.close()
    partes=tlineas/20
    for a in range(0,partes+1):
        inicio=1+(a*20)
        termino=(a+1)*20
        if a == partes:
            termino=tlineas
        contador=0
        fichero=open(nomarch,"r")
        fichero2=open("temporal","w")
        for linea in fichero:
            contador+=1
            if contador>=inicio and contador<=termino:
                linea = linea[:-1]
                fichero2.write(linea+'\n')
        fichero2.close()
        fichero.close()
        os.system('/bin/cat temporal > '+print_port)
        time.sleep(5)
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


def backup():
    try:
        res=os.popen("/usr/local/bin/ventas_auto.sh &","w")
    except:
        pass
    try:
        tiempo=time.strftime("%Y%m%d%H%M%S")
        nombre_archivo='BD_'+str(pos_num)+'_'+str(caja_num)+'_'+str(tiempo)+'.sql'
        res=os.popen("mysqldump "+str(database)+" > /backup/"+str(nombre_archivo)+" &")
    except:
        pass
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
    ubicx=len(msg)+2
    tmax=tamx+ubicx
    txtp=0
    if len(texto)>0:
        codobt=texto
        txtp=1
    else:
        codobt=''
    win=definir(pan)
    tmy,tmx=win.getmaxyx()
    tamaxx=len(msg)+2+len(codobt)
    if tamaxx>tmx:
        tmp_x=tmx-tamaxx
        codobt=codobt[tmp_x]
    win.addstr(1,1,msg+': ',curses.A_UNDERLINE)
    while 1:
        if ubicx>=tmx:
            ubicx=len(msg)+2
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
        elif caracter=='arriba':
            return 'arriba'
        elif caracter=='abajo':
            return 'abajo'
        elif caracter=='insert':
            return 'insert'
        elif caracter=='spag':
            return 'spag'
        elif caracter=='ppag':
            return 'ppag'
        elif caracter=='f12':
            return 'f12'
        elif caracter=='backspace':
            ubicx-=1
            if ubicx<=len(msg)+2:
                ubicx=len(msg)+2
            codobt=codobt[:-1]
            win.addstr(1,ubicx,'   ')
            caracter=''
        elif (caracter>='0' and caracter<='9') or (caracter>='a' and caracter<='z') or (caracter>='A' and caracter<='Z') or (caracter=='-') or (caracter=='.'):
            ubicx+=1
            codobt+=str(caracter)
            if ubicx >=(tmax):
                ubicx=tmax
                codobt=codobt[:tamx]


def viewtext(texto,pan,psey=0,codigo=''):
    cnt=0
    py=0
    win=definir(pan)
    maxy,maxx = win.getmaxyx()
    lineas=len(texto)
    cou=0
    if lineas>(maxy-2):
        cnt=lineas-(maxy-2)
    if psey>0:
        cnt+=psey
    elif psey<0:
        cnt+=psey
        lineas+=psey
    elif psey==0:
        if codigo!='':
            for a in texto:
                cou+=1
                if a[0]==codigo:
                    cnt=cou-1
                    lineas=cnt+(maxy-2)
                    break
    for a in range(cnt,lineas):
        temporal=texto[a]
        py+=1
        ubx=1
        if len(temporal)>0:
            for b in range(0,len(temporal)):
                tpx=maxx/len(temporal)
                win.addstr(py,ubx+(b*tpx),str(temporal[b]))
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


def crtsrc(maxy,maxx):
    panelt=mkpanel(curses.COLOR_WHITE,3,maxx,0,0)
    panelh=mkpanel(curses.COLOR_WHITE,3,20,3,0)
    panelh2=mkpanel(curses.COLOR_WHITE,3,20,3,21)
    panelf=mkpanel(curses.COLOR_WHITE,maxy-6,maxx,6,0)
    return panelt,panelh,panelh2,panelf


def borscr(*paneles):
    for panel in paneles:
        win=definir(panel)
        win.erase()
        updat()
    return


def expresion(dato):
    dato=str(dato)
    decimal=re.search('^\d+\.\d+$',dato)
    entero=re.search('^\d+$',dato)
    caracter=re.search('^\D+$',dato)
    alfanumerico=re.search('^[a-zA-Z0-9]+$',dato)
    if decimal:
        dato=float(decimal.group(0))
        dato=round(dato,2)
        return float(dato),'decimal'
    if entero:
        dato=entero.group(0)
        return int(dato),'entero'
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
            fech_ing=ingresodato(mensaje,ventana,15,'',1,0)
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
                if dia<=int(dia_cmp[1]):
                    date_stat=1
            if date_stat==1 and fecha_base.count(fech_ing)==0:
                fecha_base.append(fech_ing)
                break
    if modo==1:
        return fecha_base[0]
    else:
        return fecha_base


def fechai(modo=1,tipom='n'):
    panel=mkpanel(curses.COLOR_WHITE,3,26,0,0)
    if modo==2:
        panel2=mkpanel(curses.COLOR_WHITE,3,26,0,27)
    feching2=''
    continuar='n'
    mensaje1='Fecha I (AAMMDD)'
    mensaje2='Fecha V (AAMMDD)'
    if tipom=='b':
        mensaje1='Fecha V (AAMMDD)'
        mensaje2='Fecha D (AAMMDD)'
    elif tipom=='s':
        mensaje1='Fecha (AAMMDD)'
        mensaje2=''
    elif tipom=='d':
        mensaje1='Fecha 1(AAMMDD)'
        mensaje2='Fecha 2(AAMMDD)'
    if len(tipom)>2:
        mensaje1=tipom
        mensaje2=''
    while 1:
        feching=ingresodato(mensaje1,panel,15,'',1,0)
        if feching=='Anular':
            return 'Anular','Anular'
        if feching=='':
            feching,feching2=tiempocaja('d')
            return str(feching[:10]),''
        valor,tipod=expresion(feching)
        if len(feching)==6 and tipod=='entero':
            feching='20'+feching[0:2]+'-'+feching[2:4]+'-'+feching[4:6]
            continuar='s'
        if continuar=='s':
            if modo==2:
                feching2=ingresodato(mensaje2,panel2,15,'',1,0)
            if feching2=='':
                return feching,''
            valor,tipod2=expresion(feching2)
            if len(feching2)==6 and tipod=='entero':
                feching2='20'+feching2[0:2]+'-'+feching2[2:4]+'-'+feching2[4:6]
                return feching,feching2


def datesp(titulo,panel,carac,condicion,dato='',tipo=0,clr=0):
    cond=string.split(condicion,',')
    while 1:
        provis=ingresodato(titulo,panel,carac,dato,tipo,clr)
        if provis=='':
            if cond.count('vacio'):
                cantidad=0
                return cantidad
        valor=expresion(provis)
        if cond.count(valor[1]):
            return valor[0]


def cons_almacen(modo_ingreso,modo_salida,fecha='',producto='',modo_fecha=0,ciclo_fecha=0,modo_operacion=0):
    if fecha!='':
        mes=fecha[5:7]
    if ciclo_fecha==0:
        cond_ciclo=" and month(fecha_doc)='"+str(mes)+"'"
    elif ciclo_fecha==1:
        cond_ciclo=""
    if modo_fecha==0:
        cond_fecha=""+cond_ciclo
    elif modo_fecha==1:
        cond_fecha=" and fecha_doc='"+str(fecha)+"'"+cond_ciclo
    elif modo_fecha==2:
        cond_fecha=" and fecha_doc<'"+str(fecha)+"'"+cond_ciclo
    elif modo_fecha==3:
        cond_fecha=" and fecha_doc<='"+str(fecha)+"'"+cond_ciclo
    elif modo_fecha==4:
        cond_fecha=" and fecha_doc>'"+str(fecha)+"'"+cond_ciclo
    elif modo_fecha==5:
        cond_fecha=" and fecha_doc>='"+str(fecha)+"'"+cond_ciclo
    ##INGRESOS
    sql="select codbarras,sum(cantidad_ing) from almacenes where modo='"+str(modo_ingreso)+"' and estado='1' "+str(cond_fecha)+" group by codbarras order by codbarras"
    c_ing,ingresos=query(sql,1)
    ##SALIDAS
    sql="select codbarras,sum(cantidad_ing) from almacenes where modo='"+str(modo_salida)+"' and estado='1' "+str(cond_fecha)+" group by codbarras order by codbarras"
    c_sal,salidas=query(sql,1)
    data={}
    if modo_operacion==0:
        ing=conv_dict(ingresos)
        sal=conv_dict(salidas)
        for codigo in ing:
            if sal.has_key(codigo):
                data[codigo]=ing[codigo]-sal[codigo]
            else:
                data[codigo]=ing[codigo]
        if producto=='':
            return data
        else:
            if data.has_key(producto):
                return data[producto]
            else:
                return 0


def get_correlativo(modo,documento,edit=0,panel=''):
    sql = """select prefijo,correlativo+1,sufijo from
        documentos_comerciales where id='%s'""" % (documento)
    cuenta,resultado=query(sql,0)
    if cuenta>0:
        prefijo=resultado[0]
        correlativo=resultado[1]
        sufijo=resultado[2]
    else:
        prefijo=''
        correlativo=0
        sufijo=''
    if edit==0:
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
    return str(prefijo),str(correlativo),str(sufijo)


def set_correlativo(modo_doc,tipo_doc,dato,modo=1):
    sql = """update documentos_comerciales set correlativo='%s' where
        id='%s"'""" % (dato, tipo_doc)
    if modo==1:
        exe = query(sql, 3)
    else:
        return sql
    return


def producto_data(codbarras):
    sql = """select if(length(mae.alias)>0,mae.alias,
        concat(mae.nombre,' ',mae.descripcion)),round(mae.precio,2)
        from maestro mae where mae.codbarras='%s'""" % (codbarras)
    cnt,rso=query(sql,0)
    nombre=rso[0]
    precio=round(rso[1],2)
    return nombre,precio


def datopc(titulo,panel,caracter,cond_control,sql_condicion=''):
    cond_tecla=string.split(cond_control,',')
    while 1:
        ingdat=ingresodato(titulo,panel,caracter,'',0,0)
        tipo_dato=expresion(ingdat)
        for condicion in cond_tecla:
            if ingdat==condicion:
                return ingdat,0
        sql = """select mae.codbarras,if(length(mae.alias)>0,mae.alias,
            concat(mae.nombre,' ',mae.descripcion)) from maestro mae
            where %s""" % (sql_condicion)
        if tipo_dato[1]=='caracter' or tipo_dato[1]=='alfanumerico':
            sql=sql+" and (mae.nombre like '%"+ingdat+"%' or mae.descripcion like '%"+ingdat+"%' or mae.nombre like '%"+string.upper(ingdat)+"%' or mae.descripcion like '%"+string.upper(ingdat)+"%')"
        else:
            sql=sql+" and mae.codbarras='"+str(ingdat)+"'"
        cuenta,resultado=query(sql)
        retorno=0
        if cuenta==1:
            codigo=resultado[0][0]
            retorno=1
        elif cuenta>1:
            codigo,nombre=ladocl(resultado,'Producto')
            if codigo!='Anular':
                retorno=1
        if retorno==1:
            win=definewin(panel,0,0)
            win.addstr(1,len(titulo)+2,str(codigo))
            return codigo,1


def replicacion(fech,destino='/replicacion/',origen='/datos/'):
    cma=os.popen("rm -R -f "+origen+"*")
    time.sleep(5)
    aper,cier=tiempocaja(fech)
#   repbancos(aper,cier)
    fecha=str(aper)
    fecha=fecha[:10]
    try:
        for parte in tablas:
            tabla=str(parte)
            arch_almac=origen+tabla+"-"+pos_num+"-"+caja_num+"-"+fecha+'.csv'
            sql="select "+str(tablas[tabla])+ " into outfile \""+str(arch_almac)+"\" fields terminated by ',' enclosed by '\"' from "+tabla+" where registro>=\""+aper+"\" and registro<=\""+cier+"\""
            exe = query(sql)
    except Exception,msg:
        pass
    comprim=aper[0:4]+aper[5:7]+aper[8:10]+str(pos_num[2:4])+str(caja_num)+'.zip'
    archivo=zipfile.ZipFile(destino+comprim,'w')
    for fila in glob.glob(origen+"*"):
        archivo.write(fila)
    archivo.close
    return


def cierre_caja():
    tiempo = time.strftime("%Y-%m-%d %H:%M:%S")
    sql = """select id from pos_administracion 
        where pv='%s' and caja=%s and
        estado=1""" % (pos_num, caja_num)
    cuenta, resultado = query(sql, 0)
    if cuenta > 0:
        id_admin = resultado[0]
        sql = """update pos_administracion set cierre='%s',
            user_out='%s', estado=0 where
            id='%s'""" % (tiempo, idven, id_admin)
        exe = query(sql, 3)
        return 1
    else:
        return 0


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
    sql="select distinct(doc.codigo),if(length(mae.alias)>0,mae.alias,concat(mae.nombre,' ',mae.descripcion)),sum(doc.cantidad),sum(doc.cantidad/"+partes+") from docventa as doc,maestro as mae where doc.codigo=mae.codbarras and doc.pv="+str(pos_num)+" and doc.caja="+str(caja_num)+" "+condicion
    sql+=" group by codigo"
    cuenta,resultado=query(sql)
    return resultado


def delivery(apertura,cierre,modo=0):
    bkg=''
    datemp=[]
    sql = """select a.tiempo,c.n_doc_base,c.total,b.cliente,
        if(length(d.alias)>0,d.alias,
        concat(d.nombre,' ',d.descripcion)),
        c.cantidad from delivery as a,clientes as b,docventa as c,
        maestro as d where a.cliente=b.id and c.n_doc_base=a.docnum
        and c.codigo=d.id and c.estado='1' and
        (a.tiempo>='%s' and a.tiempo<='%s')
        order by a.tiempo""" % (apertura, cierre)
    cuenta,resultado=query(sql)
    if cuenta>0:
        lineas=[]
        for x in range(0,cuenta):
            temp=resultado[x]
            if bkg!=temp[1]:
                for z in range(0,2):
                    garbage=agregar_valores([],0,'>>>>','>>>>','---','>>>>','---','>>>>','---')
                    lineas.append(garbage)
                datemp=[]
                for y in range(0,3):
                    datemp.append(temp[y])
                    bkg=temp[1]
                datemp.append(0)
                lineas.append(datemp)
                garbage=agregar_valores([],0,'****','****','---','****','---','****','---')
                lineas.append(garbage)
            datemp=[]
            for y in range(3,len(temp)):
                datemp.append(temp[y])
            datemp.append(0)
            lineas.append(datemp)
        return lineas
    return ''


def ingr_alm(panel,mensaje='Destino',pre_dato=''):
    while 1:
        dato=ingresodato(mensaje,panel,12,pre_dato,1,0)
        if dato=='Anular':
            return 'Anular'
        tam_dato=len(dato)
        if tam_dato>0:
            condicion_dato=" and almacen='"+str(dato)+"'"
        else:
            condicion_dato=''
        sql = """select almacen,descripcion from almacenes_lista where modo=1 and descripcion!='' %s order by almacen asc""" % (condicion_dato)
        cuenta,resultado=query(sql,1)
        if cuenta>0:
            dato,nomb=ladocl(resultado,'Almacenes')
            if dato!='Anular':
                win=definir(panel)
                win.addstr(1,1,mensaje+': '+str(dato))
                return dato


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


def turnos(opcion1='',opcion2=''):
    if opcion1=='':
        sql="select turno,descripcion from turnos where turno!=''"
        cuenta,resultado=query(sql,1)
        ingdat,nombre=ladocl(resultado,'Turnos')
        return ingdat
    else:
        while 1:
            resp=segur('Turno: ')
            if resp=='manana':
                return opcion1
            elif resp=='tarde':
                return opcion2


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
    if eliminar==0:
        tamano_elim=0
    else:
        tamano_elim=len(eliminar)
    if tamano_elim>0:
        for posicion in eliminar:
            cadena.append(str(array[posicion]))
    for campo in campos:
        cadena.append(str(campo))
    return cadena


def conv_dict(data):
    datx={}
    for linea in data:
        if len(linea)==3:
            datx[linea[0]]=[linea[2],linea[1]]
        elif len(linea)==2:
            datx[linea[0]]=linea[1]
    return datx


def alerta_derivados(sql_prd,sql_alm):
    almacen,tipo_alm=datos_cons(sql_alm)
    variedad,tipo_var=datos_cons(sql_prd)
    panel_top=mkpanel(curses.COLOR_WHITE,3,20,3,0)
    panel_bot=mkpanel(curses.COLOR_WHITE,maxy-6,maxx,6,0)
    psey=0
    temc=0
    alm_data=conv_dict(almacen)
    var_data=conv_dict(variedad)
    cnt_alm=len(alm_data)
    cnt_var=len(var_data)
    if cnt_alm<cnt_var:
        alerta=segur("Error: Las Variedades ingresadas son mayores que en el Almacen")
    elif cnt_alm>cnt_var:
        alerta=segur("Advertencia:Existen mas productos en el Almacen que en Variedades")
    datax=[]
    orden=alm_data.keys()
    orden.sort()
    for clave in orden:
        temp=[]
        temp.append(clave)
        temp.append(alm_data[clave][0])
        cant_alm=float(alm_data[clave][1])
        temp.append(alm_data[clave][1])
        if var_data.has_key(clave):
            cant_var=float(var_data[clave][1])
            temp.append(var_data[clave][1])
        else:
            cant_var=0.0
            temp.append('0.0')
        temp.append(cant_alm-cant_var)
        datax.append(temp)
    while 1:
        viewtext(datax,panel_bot,psey)
        ingdat=ingresodato('Resumen',panel_top,10,'',0,0)
        if ingdat=='Anular':
            borscr(panelh,panelf)
            break
        elif ingdat=='arriba':
            psey-=1
        elif ingdat=='abajo':
            psey+=1
        else:
            psey=0
        temc=abs(psey)
        if temc>len(lineas):
            psey=0
    return


def selec_doc(modo):
    sql = """select id,nombre from documentos_comerciales where
        modo='%s' and pv='%s' and caja=%s order by
        id""" % (modo, pos_num, caja_num)
    cuenta,resultado=query(sql)
    if cuenta>0:
        doc_tipo,doc_tipo_dscp=ladocl(resultado,'Documento')
        if doc_tipo=='Anular':
            return 'Anular','Anular'
        else:
            return doc_tipo,doc_tipo_dscp


def sql_seleccion(sql,texto=''):
    cuenta,resultado=query(sql,1)
    if cuenta>0:
        dato,dscp=ladocl(resultado,texto)
        if dato=='Anular':
            return 'Anular','Anular'
        else:
            return dato,dscp


def alerta(mensaje,subject='ALERTA'):
    msg=("From: %s\r\nTo:%s\r\nSubject:%s\r\n%s"%(from_smtp,to_smtp,subject,mensaje))
    try:
        import smtplib
        server=smtplib.SMTP(servidor_smtp)
        server.sendmail(from_smtp,to_smtp,msg)
        server.quit()
    except Exception,excp:
        pass


def doc_man(fecha):
    docum=[]
    sql = """select doc.nombre,sum(vta.sub_total_bruto) from docventa
        vta left join documentos_comerciales doc on
        doc.id=vta.comprobante where vta.fecha_vta='%s'
        and doc.modo=5 and vta.estado=1
        group by doc.modo,doc.documento""" % (fecha)
    cuenta,resultado=query(sql)
    if cuenta>0:
        for linea in resultado:
            docum.append(str(linea[0])+': '+str(round(float(linea[1]),2)))
    return docum


def proc_anulacion():
    apertura,cierre=tiempocaja()
    panel_full=mkpanel(curses.COLOR_WHITE,maxy,maxx,0,0)
    panel_cons=mkpanel(curses.COLOR_WHITE,3,40,5,(maxx/2)-20)
    win=definir(panel_full)
    linea='3. Anulacion de Documentos'
    px=centrar(maxx,linea)
    win.addstr(2,px,linea)
    updat()
    while 1:
        sql = """select distinct(modo),case modo when 0 then 'Interno'
            when 5 then 'Manual' end dscp from documentos_comerciales
            where (modo=0 or modo=5) order by modo"""
        modo, modo_dscp = sql_seleccion(sql, 'Modo')
        if modo=='Anular':
            return 0
        sql = """select id,nombre from documentos_comerciales where
            modo='%s' order by documento""" % (modo)
        documento,documento_dscp=sql_seleccion(sql,'Documento')
        if documento=='Anular':
            return 0
        sql = """select copia,detalle from documentos_comerciales where
            id='%s'""" % (documento)
        cuenta,resultado=query(sql,0)
        if cuenta>0:
            compr_id=documento
            compr_copia=resultado[0]
            compr_detalle=resultado[0]
        else:
            return 0
        linea='Numero de Documento'
        no_doc=ingresodato(linea,panel_cons,15,'',1,0)
        if no_doc=='Anular':
            break
        #sql="""select doc.fp,fpa.nombre,doc.cv_ing,
            #concat(usr.nombres,' ',usr.apellidos),doc.cantidad,
            #doc.codigo,if(length(mae.alias)>0,mae.alias,
            #concat(mae.nombre,' ',mae.descripcion)),doc.precio,
            #doc.total,doc.tiempo,doc.cliente,dir.nombre_corto,
            #doc.n_doc_base from docventa doc left join maestro
            #mae on mae.codbarras=doc.codigo left join formas_pago
            #fpa on fpa.forma_pago=doc.fp left join usuarios_pos usr on
            #usr.codigo=doc.cv_ing left join directorio dir on
            #dir.doc_id=doc.cliente where doc.n_doc_base='%s'
            #and doc.comprobante='%s' and doc.caja=%s
            #and doc.pv='%s' and doc.vta>='%s'""" % (no_doc,
            #compr_id, caja_num, pos_num, apertura)
        sql = """select substring_index(doc.medios_pago,':',1) fp_ad,fpa.nombre,doc.cv_ing,
            concat(usr.first_name,' ',usr.last_name) usr_name,doc.cantidad,
            doc.codigo,if(length(mae.alias)>0,mae.alias,
            concat(mae.nombre,' ',mae.descripcion)) alias,doc.precio,
            doc.total,doc.tiempo,doc.cliente,dir.nombre_corto,
            doc.n_doc_base from docventa doc left join maestro
            mae on mae.id=doc.codigo left join formas_pago
            fpa on fpa.id=substring_index(doc.medios_pago,':',1) left join auth_user usr on
            usr.id=doc.cv_ing left join directorio dir on
            dir.doc_id=doc.cliente where doc.n_doc_base='%s'
            and doc.comprobante='%s' and doc.caja=%s
            and doc.pv='%s' and doc.fecha_vta='%s'""" % (no_doc,
            compr_id, caja_num, pos_num, apertura[:10])
        cuenta,resultado=query(sql)
        if cuenta>0:
            linea='El total de dicho documento es: '+str(resultado[0][8])
            px=centrar(maxx,linea)
            win.addstr(9,px,linea)
            resp=segur('Procedo a su Anulacion? ')
            if resp=='si':
                tiempo_null=time.strftime("%Y-%m-%d %H:%M:%S")
                nomarch='anulacion'+str(time.time())
                archivo=open(nomarch,'w')
                ticket(archivo,compr_detalle,resultado,tiempo_null)
                archivo.close()
                impresion(nomarch,gaveta)
                if compr_copia=='1':
                    impresion(nomarch,gaveta)
                if debug_mode=='0' or debug_mode=='':
                    os.remove(nomarch)
                sql="update docventa set estado='0',cv_anul='"+str(idven)+"',tiempo_null='"+str(tiempo_null)+"' where n_doc_base='"+str(no_doc)+"' and comprobante='"+str(compr_id)+"' and caja="+str(caja_num)+" and pv="+str(pos_num)+""
                exe = query(sql, 3)
                resp=segur('Anulacion Exitosa!!!')
                break
            elif resp=='exit':
                break
        else:
            linea='Documento NO existe o NO puede ser Anulado'
            resp=segur(linea)
    return


def gestion_caja():
    #apertura,cierre=tiempocaja()
    panel=mkpanel(curses.COLOR_WHITE,maxy,maxx,0,0)
    win=definir(panel)
    tiempo=time.strftime("%Y-%m-%d %H:%M:%S")
    sql_i = """insert into pos_administracion (pv,caja,user_ing,
        apertura,registro,estado) values ('%s',%s,'%s','%s','%s',1)
        """ % (pos_num, caja_num, idven, tiempo, tiempo)
    resp=''
    strimpr('6. Gestion de Caja',2,maxx,win)
    strimpr('Fecha Actual: '+str(tiempo[:10]),9,maxx,win)
    strimpr('Hora Actual: '+str(tiempo[11:]),10,maxx,win)
    strimpr('Estado de Caja: ',12,maxx,win)
    updat()
    sql = """select apertura, cierre from pos_administracion 
        where pv='%s' and caja=%s and
        estado=1""" % (pos_num, caja_num)
    cuenta, resultado = query(sql,0)
    if cuenta == 0:
        strimpr('CERRADA',13,maxx,win)
        strimpr('---------------------',14,maxx,win)
        #win.getch()
        resp=segur("Procedo a la Apertura? ")
        if resp == 'si':
            sql = """select apertura from pos_administracion order by id
                desc limit 1"""
            cuenta, resultado = query(sql,0)
            if cuenta == 0:
                estado = query(sql_i, 3)
            else:
                ultimo_tiempo = str(resultado[0])
                if tiempo <= ultimo_tiempo:
                    strimpr('Error en la Fecha de la Computadora!!!',13,maxx,win)
                    strimpr('No es posible Aperturar la Caja',14,maxx,win)
                    updat()
                    win.getch()
                    return
            #estado = query(sql_i, 3)
            strimpr('--* Caja Aperturada *--',13,maxx,win)
            strimpr('Fecha: '+str(tiempo[:10]),15,maxx,win)
            strimpr('Hora: '+str(tiempo[11:]),16,maxx,win)
            win.getch()
    else:
        strimpr('APERTURADA',13,maxx,win)
        strimpr('---------------------',14,maxx,win)
        updat()
        win.getch()
    return


def gestion_asistencia():
    apertura,cierre=tiempocaja()
    panel_full=mkpanel(curses.COLOR_WHITE,maxy,maxx,0,0)
    win=definir(panel_full)
    tiempo=time.strftime("%Y-%m-%d %H:%M:%S")
    strimpr('7. Control de Asistencia',2,maxx,win)
    strimpr('Fecha Actual: '+str(tiempo[:10]),5,maxx,win)
    strimpr('Hora Actual: '+str(tiempo[11:]),6,maxx,win)
    strimpr('*************************',7,maxx,win)
    strimpr('Usuario: '+str(nomven),8,maxx,win)
    strimpr('Codigo: '+str(codven),9,maxx,win)
    strimpr('Nivel: '+str(nivel),10,maxx,win)
    updat()
    while 1:
        sql="select ingreso,salida from personal where usuario='"+str(idven)+"' and pv="+str(pos_num)+" and salida='0' order by id desc"
        cuenta,resultado=query(sql,0)
        if cuenta==0:
            strimpr('Ingreso No Registrado',13,maxx,win)
            strimpr('---------------------',14,maxx,win)
            updat()
            win.getch()
            resp=segur("Procedo a Registrar su Ingreso? ")
            if resp=='si':
                qsql="insert into personal (ingreso,pv,usuario) values ('"+str(tiempo)+"','"+str(pos_num)+"','"+str(idven)+"')"
                qsex = query(qsql, 3)
                strimpr('--* Ingreso Registrado *--',13,maxx,win)
                strimpr('Fecha: '+str(tiempo[:10]),15,maxx,win)
                strimpr('Hora: '+str(tiempo[11:]),16,maxx,win)
                updat()
                win.getch()
            break
        else:
            strimpr('Ingreso Previamente Registrado',13,maxx,win)
            strimpr('---------------------',14,maxx,win)
            updat()
            win.getch()
            resp=segur("Procedo a Registrar su Salida? ")
            if resp=='si':
                qsql="update personal set salida='"+str(tiempo)+"' where ingreso='"+str(resultado[0])+"' and usuario='"+str(idven)+"' and pv="+str(pos_num)+""
                qsex = query(qsql, 3)
                strimpr('--* Salida Registrada *--',13,maxx,win)
                strimpr('Fecha: '+str(tiempo[:10]),15,maxx,win)
                strimpr('Hora: '+str(tiempo[11:]),16,maxx,win)
                updat()
                win.getch()
            break
    return


def vta_total(fecha):
    sql = """select sum(vta.sub_total_bruto) from docventa vta where
        vta.fecha_vta=date(%s) and vta.estado='1' and
        vta.pv='%s'""" % (fecha, pos_num)
    cuenta,resultado=query(sql,0)
    if cuenta>0:
        total_vta=float(resultado[0])
    else:
        total_vta=0
    return total_vta


def data_proc(tipo_mov=1,doc_modo=1,doc_tipo=6,txt_fld=3,fech_cnt=1,fech_hea='t',turno_ing=1,masa_ing=1,impresion=1,oper_log='IPT',alm_rel='0101',alm_base='0100',oper_log_pref='1',add_data='',prod_filt='mae.genero="0002"'):
    panel_top,panel_text_1,panel_text_2,panel_text_3,panel_mid=win_def(txt_fld)#maxy,maxx
    campos_bd='alm.codbarras,alm.cantidad_ing,alm.turno,alm.fecha_doc,alm.modo,alm.almacen_origen,alm.almacen_destino,alm.operacion_logistica,alm.modo_doc,alm.tipo_doc'
    seleccion_prod={}
    validacion_prod={}
    lineas=[]
    fecha=fecha_ing(fech_cnt,fech_hea)
    if fecha=='Anular':
        return 0
    else:
        prefijo,correlativo,sufijo=get_correlativo(doc_modo,doc_tipo,0,panel_text_3)
        sql="select if(length(mae.alias)>0,mae.alias,concat(mae.nombre,' ',mae.descripcion)),"+campos_bd+" from almacenes alm left join maestro mae on mae.codbarras=alm.codbarras where alm.n_doc_base="+correlativo+" and alm.n_doc_prefijo='"+prefijo+"' and alm.n_doc_sufijo='"+sufijo+"' and alm.fecha_doc='"+str(fecha)+"' and alm.estado='1' and alm.modo_doc='"+str(doc_modo)+"' and alm.tipo_doc='"+str(doc_tipo)+"'"
        cuenta,resultado=query(sql)
        if cuenta>0:
            turno=resultado[0][3]
            fecha=str(resultado[0][4])
            fecha=fecha[:10]
            modo_oper_log=str(resultado[0][5])
            alm_ori=resultado[0][6]
            alm_des=resultado[0][7]
            oper_log=resultado[0][8]
            doc_modo=resultado[0][9]
            doc_tipo=resultado[0][10]
            extra_oper_log=''
            alm_ori2=''
            alm_des2=''
            masa=''
            extra_data=''
            correlativo2=0
            transp_codigo=''
            vehiculo_codigo=''
#           cabecera='Fecha: '+str(fecha)+' - Turno: '+str(turno)+ ' - Masa: '+str(masa)+' - Operacion: '+str(oper_log)
            for linea in resultado:
                seleccion_prod[linea[1]]=[linea[2],linea[0],0]
            lineas=[]
            validacion_prod=seleccion_prod
            for valor in validacion_prod:
                cod_tmp=valor
                cnt_tmp=validacion_prod[valor][0]
                nom_tmp=validacion_prod[valor][1]
                mod_tmp=validacion_prod[valor][2]
                prov=agregar_valores([],[],cod_tmp,cnt_tmp,nom_tmp,mod_tmp)
                lineas.append(prov)
            titulo_almacenes=str(alm_ori)+'/'+str(alm_des)
            cabecera='Fecha: '+str(fecha)+' - Turno: '+str(turno)+' - Operacion: '+str(oper_log)+' - Almacenes: '+str(titulo_almacenes)
        else:
            if turno_ing==1:
                sql="select turno,descripcion from turnos where turno!='' order by turno asc"
                turno,turno_dscp=sql_seleccion(sql,'Turno')
                if turno=='Anular':
                    return 0
            modo_oper_log=''
            oper_log2=''
            modo_oper_log2=''
            masa=''
            extra_data=''
            extra_oper_log=0
            alm_ori2=''
            alm_des2=''
            correlativo2=''
            transp_codigo=''
            vehiculo_codigo=''
            titulo_almacenes=''
            while 1:
                if oper_log=='':
                    oper_log=ingresodato('Operacion',panel_text_1,10,oper_log,1,0)
                    if oper_log=='Anular':
                        return 0
                    tam_oper_log=len(oper_log)
                    if tam_oper_log>=3 and tam_oper_log<=4:
                        condicion_oper_log="operacion='"+str(oper_log)+"' or operacion='"+string.upper(str(oper_log))+"'"
                    elif tam_oper_log>4:
                        condicion_oper_log="(descripcion like '"+str(oper_log)+"%' or descripcion like ucase('"+str(oper_log)+"%')) and operacion!=''"
                    else:
                        condicion_oper_log="operacion!=''"
                    sql="select operacion,descripcion from operaciones_logisticas where "+condicion_oper_log
                    oper_log,oper_log_dscp=sql_seleccion(sql,'Operaciones Logisticas')
                    if oper_log=='Anular':
                        return 0
                sql="select modo,operacion_relac,almacen_relac from operaciones_logisticas where operacion='"+str(oper_log)+"'"
                cta,rso=query(sql,0)
                if cta>0:
                    modo_oper_log=oper_log_pref+str(rso[0])
                else:
                    return 0
                if alm_rel=='':
                    if rso[0]==1:
                        alm_ori=ingr_alm(panel_text_1,'Origen')
                        alm_des=alm_base
                    elif rso[0]==2:
                        alm_ori=alm_base
                        alm_des=ingr_alm(panel_text_1,'Destino')
                    titulo_almacenes=str(alm_ori)+'/'+str(alm_des)
                    if alm_ori=='Anular' or alm_des=='Anular':
                        return 0
                    if rso[1]!='':
                        almacen_relac=rso[2]
                        sql="select modo from operaciones_logisticas where operacion='"+str(rso[1])+"'"
                        cta2,rso2=query(sql,0)
                        if cta2==0:
                            return 0
                        else:
                            ##Data
                            if rso2[0]==1:
                                if almacen_relac!='':
                                    alm_ori2=almacen_relac
                                else:
                                    alm_ori2=ingr_alm(panel_text_2,'Origen',almacen_relac)
                                alm_des2=alm_base
                                titulo_almacenes=str(alm_des)+'/'+str(alm_ori2)
                            elif rso2[0]==2:
                                alm_ori2=alm_base
                                if almacen_relac!='':
                                    alm_des2=almacen_relac
                                else:
                                    alm_des2=ingr_alm(panel_text_2,'Destino',almacen_relac)
                                titulo_almacenes=str(alm_ori)+'/'+str(alm_des2)
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
                sql="select codigo,concat(nombres,' ',apellidos) from transportistas where (nombres like '%"+str(transp_data)+"%' or apellidos like '%"+str(transp_data)+"%') and (nombres!='' or apellidos!='')"
                transp_codigo,transp_descripcion=sql_seleccion(sql,'Transportista')
                if transp_codigo=='Anular':
                    return 0
                sql="select codigo,concat('->',registro,'-',marca,' / ',modelo) from vehiculos"
                vehiculo_codigo,vehiculo_descripcion=sql_seleccion(sql,'Vehiculos')
                if vehiculo_codigo=='Anular':
                    return 0
            if masa_ing==1:
                masa=ingresodato('Masa',panel_text_1,10,'',1,1)
                if masa=='Anular' or masa=='':
                    return 0
                cabecera='Fecha: '+str(fecha)+' - Turno: '+str(turno)+ ' - Masa: '+str(masa)+' - Operacion: '+str(oper_log)
#       lineas=[]
        psey=0
        temc=0
        winhead(cabecera,panel_top)
        while 1:
            procesar=1
            viewtext(lineas,panel_mid,psey)
            ingdat,cuenta=datopc('Codigo',panel_text_1,10,'insert,arriba,abajo,Anular',prod_filt)
            cuenta,resultado=query("select if(length(mae.alias)>0,concat(mae.alias,'(',mae.unidad_medida,')'),concat(mae.nombre,' ',mae.descripcion,'(',mae.unidad_medida,')')) from maestro mae where mae.codbarras!='' and mae.codbarras='"+str(ingdat)+"'",0)
            if cuenta>0:
                nombre_prod=resultado[0]
                if add_data!='':
                    while 1:
                        extra_data=ingresodato(add_data,panel_text_2,30,'',1,10)
                        if extra_data=='Anular':
                            return 0
                        cantidad=1
                        break
                else:
                    cantidad=datesp('Cantidad',panel_text_2,8,'decimal,entero','',1,1)
                    if cantidad>500:
                        resp=segur("Esta seguro(a)? ")
                        if resp=='si':
                            procesar=1
                        else:
                            procesar=0
                stock_individual=cons_almacen('91','92',fecha,str(ingdat)) #modo_ingreso,modo_salida,producto='',fecha='',modo_fecha=0,ciclo_fecha=0,modo_operacion=0
                stock_individual=10000
                if modo_oper_log[-1]=='2':
                    stock_individual=float(stock_individual)
                else:
                    stock_individual=cantidad
                if cantidad==0 or stock_individual==0 or cantidad>stock_individual:
                    segur('El Stock de este producto es:'+str(stock_individual))
                    procesar=0
                if procesar==1:
                    if seleccion_prod.has_key(ingdat):
                        modo_int=0
                    else:
                        modo_int=1
                    validacion_prod[ingdat]=[cantidad,nombre_prod,modo_int]
                    lineas=[]
                    for valor in validacion_prod:
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
                query_trans=[]
                tiempo_reg=time.strftime("%Y-%m-%d %H:%M:%S")
                if correlativo=='Anular':
                    return
                if extra_oper_log==1:
                    prefijo2=prefijo
                    correlativo2=int(correlativo)+1
                    sufijo2=sufijo
                for z in range(0,len(lineas)):
                    if lineas[z][3]=='0':
                        base=sqlsend(lineas[z],'codbarras,cantidad_ing',0)
                        sql="update almacenes set "+base+",user_ing='"+str(idven)+"',tiempo='"+str(tiempo_reg)+"' where n_doc_base='"+str(correlativo)+"' and codbarras='"+str(lineas[z][0])+"' and turno='"+str(turno)+"' and fecha_doc='"+str(fecha)+"' and estado='1' and operacion_logistica='"+str(oper_log)+"' and modo='"+str(modo_oper_log)+"' and modo_doc='"+str(doc_modo)+"' and tipo_doc='"+str(doc_tipo)+"'"
                        query_trans.append(sql)
                    else:
                        campos_bd='codbarras,cantidad_ing,turno,n_doc_base,user_ing,tiempo,fecha_doc,modo,almacen_origen,almacen_destino,fecha_prod,estado,masa,operacion_logistica,extra_data,modo_doc,tipo_doc,n_doc_relacion,transportista,vehiculo'
                        temporal=lineas[z]
                        temporal_x=agregar_valores(temporal,[0,1],turno,correlativo,codven,tiempo_reg,fecha,modo_oper_log,alm_ori,alm_des,fecha,'1',masa,oper_log,extra_data,doc_modo,doc_tipo,correlativo2,transp_codigo,vehiculo_codigo)
                        base=sqlsend(temporal_x,campos_bd,1)
                        sql="insert into almacenes "+base
                        query_trans.append(sql)
                        if extra_oper_log==1:
                            temporal_y=agregar_valores(temporal,[0,1],turno,correlativo2,codven,tiempo_reg,fecha,modo_oper_log2,alm_ori2,alm_des2,fecha,'1',masa,oper_log2,extra_data,doc_modo,doc_tipo,correlativo,transp_codigo,vehiculo_codigo)
                            base2=sqlsend(temporal_y,campos_bd,1)
                            sql2="insert into almacenes "+base2
                            query_trans.append(sql2)
                if len(query_trans)>0:
                    sql=set_correlativo(doc_modo,doc_tipo,correlativo,0)
                    query_trans.append(sql)
                    if extra_oper_log==1:
                        sql=set_correlativo(doc_modo,doc_tipo,correlativo2,0)
                        query_trans.append(sql)
                estado=query(query_trans,5)
                if estado==1:
                    if modo_oper_log[-1]=='1':
                        msg1='Nota de Ingreso'
                        msg2='Nota de Salida'
                        alm1=alm_ori
                        alm2=alm_des2
                    elif modo_oper_log[-1]=='2':
                        msg1='Nota de Salida'
                        msg2='Nota de Ingreso'
                        alm1=alm_des
                        alm2=alm_ori2
                    if tipo_mov==2:
                        if impresion==1:
                            impresion_guia_externa(prefijo,correlativo)
                    else:
                        if impresion==1:
                            impresion_guia_interna(prefijo,correlativo)
                    if extra_oper_log==1:
                        if impresion==1:
                            impresion_guia_interna(prefijo2,correlativo2)
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


def derivados_proc(txt_fld=3,alm_ori='',alm_des='',campos='ing_produccion',add_data='',prod_filt='mae.genero="0004"'):#tipo_mov=1,doc_modo=1,doc_tipo=6,txt_fld=3,fech_cnt=1,fech_hea='t',turno_ing=1,masa_ing=1,impresion=1,oper_log='IPT',alm_rel='0101',alm_base='0100',oper_log_pref='1',add_data='',prod_filt='genero="0002"'):
    panel_top,panel_text_1,panel_text_2,panel_text_3,panel_mid=win_def(txt_fld)#maxy,maxx
    fecha=fecha_ing(1,'t')
    if fecha=='Anular':
        return 0
    else:
        sql="select turno,descripcion from turnos where turno!='' order by turno asc"
        turno,turno_dscp=sql_seleccion(sql,'Turno')
        if turno=='Anular':
            return 0
        campos=string.split(campos,'|')
        if len(campos)==1:
            campo=campos[0]
        if alm_ori=='':
            alm_ori=ingr_alm(panel_text_1,'Origen',alm_des)
            if alm_ori!=alm_des:
                if len(campos)==2:
                    campo=campos[1]
                else:
                    campo=campos[0]
            else:
                campo=campos[0]
        if alm_ori=='Anular':
            return
        if alm_des=='':
            alm_des=ingr_alm(panel_text_1,'Destino',alm_ori)
        if alm_des=='Anular':
            return
        titulo_almacenes=str(alm_ori)+'/'+str(alm_des)
        cabecera='Fecha: '+str(fecha)+' - Turno: '+str(turno)+' - Almacenes: '+str(titulo_almacenes)
        lineas=[]
        psey=0
        temc=0
        winhead(cabecera,panel_top)
        validacion_prod={}
        seleccion_prod={}
        sql="select pro.codbarras,pro."+str(campo)+",if(length(mae.alias)>0,mae.alias,concat(mae.nombre,' ',mae.descripcion)) from produccion_derivados pro left join maestro mae on mae.codbarras=pro.codbarras where pro.fecha='"+str(fecha)+"' and pro.cp_base='"+str(alm_ori)+"' and pro.cp_aux='"+str(alm_des)+"' and pro.turno='"+str(turno)+"'"
        cuenta,resultado=query(sql)
        if cuenta>0:
            for linea in resultado:
                seleccion_prod[linea[0]]=[linea[1],linea[2],0]
            lineas=[]
            validacion_prod=seleccion_prod
            for valor in validacion_prod:
                cod_tmp=valor
                cnt_tmp=validacion_prod[valor][0]
                nom_tmp=validacion_prod[valor][1]
                mod_tmp=validacion_prod[valor][2]
                prov=agregar_valores([],[],cod_tmp,cnt_tmp,nom_tmp,mod_tmp)
                lineas.append(prov)
        while 1:
            procesar=1
            viewtext(lineas,panel_mid,psey)
            ingdat,cuenta=datopc('Codigo',panel_text_1,10,'insert,arriba,abajo,Anular',prod_filt)
            cuenta,resultado=query("select if(length(mae.alias)>0,mae.alias,concat(mae.nombre,' ',mae.descripcion)) from maestro mae where mae.codbarras='"+str(ingdat)+"'",0)
            if cuenta>0:
                nombre_prod=resultado[0]
                if add_data!='':
                    while 1:
                        extra_data=ingresodato(add_data,panel_text_2,30,'',1,10)
                        if extra_data=='Anular':
                            return 0
                        cantidad=1
                        break
                else:
                    cantidad=datesp('Cantidad',panel_text_2,8,'decimal,entero','',1,1)
                    if cantidad>500:
                        resp=segur("Esta seguro(a)? ")
                        if resp=='si':
                            procesar=1
                        else:
                            procesar=0
                if procesar==1:
                    if seleccion_prod.has_key(ingdat):
                        modo_int=0
                    else:
                        modo_int=1
                    validacion_prod[ingdat]=[cantidad,nombre_prod,modo_int]
                    lineas=[]
                    for valor in validacion_prod:
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
                query_trans=[]
                for z in range(0,len(lineas)):
                    if lineas[z][3]=='0':
                        base=sqlsend(lineas[z],'codbarras,'+str(campo),0)
                        sql="update produccion_derivados pro set "+base+",user_ing='"+str(idven)+"' where pro.codbarras='"+str(lineas[z][0])+"' and pro.fecha='"+str(fecha)+"' and pro.cp_base='"+str(alm_ori)+"' and pro.cp_aux='"+str(alm_des)+"' and pro.turno='"+str(turno)+"'"
                        query_trans.append(sql)
                    else:
                        campos_bd='codbarras,'+str(campo)+',turno,cp_base,cp_aux,fecha,user_ing'
                        temporal=lineas[z]
                        temporal_x=agregar_valores(temporal,[0,1],turno,alm_ori,alm_des,fecha,codven)
                        base=sqlsend(temporal_x,campos_bd,1)
                        sql="insert into produccion_derivados "+base
                    query_trans.append(sql)
                estado=query(query_trans,5)
                if estado==1:
                    return 1
                elif estado==-1:
                    return -1
                elif estado==0:
                    return 0
            elif ingdat=='arriba':
                psey-=1
            elif ingdat=='abajo':
                psey+=1
            temc=abs(psey)
            if temc>len(lineas):
                psey=0


def win_def(txt_fld=2,maxy=24,maxx=80):
    panel_top=mkpanel(curses.COLOR_WHITE,3,maxx,0,0)
    panel_text_1=mkpanel(curses.COLOR_WHITE,3,20,3,0)
    if txt_fld==2.5:
        panel_text_2=mkpanel(curses.COLOR_WHITE,3,40,3,20)
    else:
        panel_text_2=mkpanel(curses.COLOR_WHITE,3,20,3,20)
    if txt_fld>=3:
        panel_text_3=mkpanel(curses.COLOR_WHITE,3,20,3,40)
        panel_text_4=mkpanel(curses.COLOR_WHITE,3,20,3,60)
    panel_mid=mkpanel(curses.COLOR_WHITE,maxy-6,maxx,6,0)
    if txt_fld==1:
        return panel_top,panel_text_1,panel_mid
    elif txt_fld==2 or txt_fld==2.5:
        return panel_top,panel_text_1,panel_text_2,panel_mid
    elif txt_fld==3:
        return panel_top,panel_text_1,panel_text_2,panel_text_3,panel_mid
    elif txt_fld==4:
        return panel_top,panel_text_1,panel_text_2,panel_text_3,panel_text_4,panel_mid


def winhead(texto,pan):
    win=definir(pan)
    maxy,maxx = win.getmaxyx()
    px=centrar(maxx,texto)
    win.addstr(1,px,texto)
    updat()
    return


def inventarios(pos_num):
    prod_filt="genero='0001'"
    panel_top,panel_text_1,panel_text_2,panel_text_3,panel_text_4,panel_mid=win_def(4)#maxy,maxx
    fecha=fecha_ing(1,'t')
    if fecha=='Anular':
        return 0
    else:
        cabecera='Fecha: '+str(fecha)+' - Almacen: '+str(pos_num)
        lineas=[]
        psey=0
        temc=0
        winhead(cabecera,panel_top)
        validacion_prod={}
        seleccion_prod={}
        sql="select inv.codbarras,if(length(mae.alias)>0,concat(mae.alias,' (',mae.unidad_medida,')'),concat(mae.nombre,' ',mae.descripcion,' (',mae.unidad_medida,')')) ,inv.cantidad,inv.cantidad_1,inv.cantidad_2,inv.cantidad_conv,mae.unidad_medida_valor from inventarios inv left join maestro mae on mae.codbarras=inv.codbarras awhere fecha_doc='"+str(fecha)+"' and modo=0 and almacen='"+str(pos_num)+"'"
        cuenta,resultado=query(sql)
        if cuenta>0:
            for linea in resultado:
                seleccion_prod[linea[0]]=[linea[1],linea[2],linea[3],linea[4],linea[5],linea[6],0]
            lineas=[]
            validacion_prod=seleccion_prod
            for valor in validacion_prod:
                cod_tmp=valor
                cnt_tmp=validacion_prod[valor][0]
                nom_tmp=validacion_prod[valor][1]
                mod_tmp=validacion_prod[valor][2]
                prov=agregar_valores([],[],cod_tmp,cnt_tmp,nom_tmp,mod_tmp)
                lineas.append(prov)
        nomarch='inventario'+str(fecha)+'-'+pos_num+'.csv'
        while 1:
            procesar=1
            viewtext(lineas,panel_mid,psey)
            ingdat,cuenta=datopc('Codigo',panel_text_1,10,'insert,arriba,abajo,Anular',prod_filt)
            cuenta,resultado=query("select if(length(mae.alias)>0,mae.alias,concat(mae.nombre,' ',mae.descripcion)) from maestro mae where mae.codbarras='"+str(ingdat)+"'",0)
            if cuenta>0:
                nombre_prod=resultado[0]
                sql="select if(inv.peso_total_1 is null,0,inv.peso_total_1),if(inv.peso_total_2 is null,0,inv.peso_total_2),if(inv.peso_tara_1 is null,0,inv.peso_tara_1),if(inv.peso_tara_2 is null,0,inv.peso_tara_2),if(inv.factor is null,mae.unidad_medida_valor,inv.factor),if(inv.factor_peso is null,1,inv.factor_peso),mae.unidad_empaque,mae.unidad_medida,inv.peso_unitario,inv.formula  from maestro mae left join  inventarios_control inv on mae.codbarras=inv.codbarras where mae.codbarras='"+str(ingdat)+"'"
                cuenta,resultado=query(sql,0)
                if cuenta>0:
                    peso_total_1=resultado[0]
                    peso_total_2=resultado[1]
                    peso_tara_1=resultado[2]
                    peso_tara_2=resultado[3]
                    factor_conv=resultado[4]
                    factor_peso=resultado[5]
                    unidad_inv=resultado[6]
                    unidad_med=resultado[7]
                    peso_unitario=resultado[8]
                    formula=resultado[9]
                    if formula==1:
                        dato_tot=((peso_total_1*factor_peso)+peso_total_2)
                        dato_tar=((peso_tara_1*factor_peso)+peso_tara_2)
                    else:
                        dato_tot=(peso_total_1+(peso_total_2/factor_peso))
                        dato_tar=(peso_tara_1+(peso_tara_2/factor_peso))
                    if dato_tot==0:
                        dato_tot=1
                else:
                    factor_conv=1
                    factor_peso=1
                    dato_tot=1
                    dato_tar=0
                unidad_empaque=datesp('Und',panel_text_2,8,'vacio,decimal,entero','',1,1)
                if unidad_empaque>5000:
                    resp=segur("Esta seguro(a)?: "+str(unidad_empaque))
                    if resp=='si':
                        procesar=1
                    else:
                        procesar=0
                if unidad_empaque>0:
                    unid_med=unidad_empaque*factor_conv
                else:
                    unid_med=0
#               unidad_medida=datesp('Und',panel_text_2,8,'vacio,decimal,entero','',1,1)
                unidad_peso_1=datesp('Lbs',panel_text_3,8,'vacio,decimal,entero','',1,1)
                unidad_peso_2=datesp('Onz',panel_text_4,8,'vacio,decimal,entero','',1,1)
                if formula==1:
                    dato_act=((unidad_peso_1*factor_peso)+unidad_peso_2)
                else:
                    dato_act=(unidad_peso_1+(unidad_peso_2/factor_peso))
                if peso_unitario>0:
                    cantidad=unid_med+(dato_act/peso_unitario)
                else:
#                   cantidad=(unidad_medida+unid_med)+((dato_act*factor_conv)/(dato_tot-dato_tar))
                    if formula==1:
#                       valor_cnt=(dato_act/factor_peso)*factor_conv
                        valor_cnt=dato_act*factor_conv
                    else:
                        valor_cnt=dato_act*factor_conv
                    cantidad=unid_med+(valor_cnt/(dato_tot-dato_tar))
#               print cantidad
#               print dato_act
#               print peso_unitario
#               sys.exit()
                if unidad_med=='UND':
                    cantidad=round(cantidad,0)
                if procesar==1:
                    if seleccion_prod.has_key(ingdat):
                        modo_int=0
                    else:
                        modo_int=1
                    validacion_prod[ingdat]=[nombre_prod,unidad_empaque,unidad_peso_1,unidad_peso_2,cantidad,modo_int]
                    lix=str(ingdat)+','+nombre_prod+','+str(unidad_empaque)+','+str(unidad_peso_1)+','+str(unidad_peso_2)+','+str(cantidad)+'\n'
                    fila=open(nomarch,'a')
                    fila.write(lix)
                    fila.close()
                    os.system('tail -n 1 '+str(nomarch)+'>'+print_port)
                    lineas=[]
                    for valor in validacion_prod:
                        cod_tmp=valor
                        nom_tmp=validacion_prod[valor][0]
                        emp_tmp=validacion_prod[valor][1]
#                       med_tmp=validacion_prod[valor][2]
                        peso1_tmp=validacion_prod[valor][2]
                        peso2_tmp=validacion_prod[valor][3]
                        cnt_tmp=validacion_prod[valor][4]
                        mod_tmp=validacion_prod[valor][5]
                        prov=agregar_valores([],[],cod_tmp,emp_tmp,peso1_tmp,peso2_tmp,cnt_tmp,nom_tmp,mod_tmp)
                        lineas.append(prov)
            if ingdat=='Anular':
                resp=segur("Esta seguro(a)? ")
                if resp=='si':
                    return 0
            elif ingdat=='insert':
                query_trans=[]
                for z in range(0,len(lineas)):
                    if lineas[z][6]=='0':
                        base=sqlsend(lineas[z],'codbarras,'+str(campo),0)
                        sql="update produccion_derivados pro set "+base+",user_ing='"+str(idven)+"' where pro.codbarras='"+str(lineas[z][0])+"' and pro.fecha='"+str(fecha)+"' and pro.cp_base='"+str(alm_ori)+"' and pro.cp_aux='"+str(alm_des)+"' and pro.turno='"+str(turno)+"'"
                        query_trans.append(sql)
                    else:
                        campos_bd='codbarras,cantidad,cantidad_1,cantidad_2,cantidad_conv,fecha_doc,almacen'
                        temporal=lineas[z]
                        temporal_x=agregar_valores(temporal,[0,1,2,3,4],fecha,pos_num)
                        base=sqlsend(temporal_x,campos_bd,1)
                        sql="insert into inventarios "+base
                    query_trans.append(sql)
                estado=query(query_trans,5)
                if estado==1:
                    return 1
                elif estado==-1:
                    return -1
                elif estado==0:
                    return 0
            elif ingdat=='arriba':
                psey-=1
            elif ingdat=='abajo':
                psey+=1
            temc=abs(psey)
            if temc>len(lineas):
                psey=0
    sys.exit()


panelmenu=mkpanel(curses.COLOR_WHITE,maxy,maxx,0,0)
fecha=time.strftime("%Y-%m-%d")
sumtot=0.00
contad=0
apertura,cierre=tiempocaja()


while 1:
    while nomven=='I':
        codven,nomven,nivel,idven=aut()
    doc_cabecera,doc_pie,modo_imp,impuestos,modmon,moneda,tipo_cambio,gaveta,prod_resumen,prod_clave,empresa,tipo_servicio,wincha,servidor_smtp,from_smtp,to_smtp,fondo_caja=configurat()
    ident=idd()
    while 1:
        sumtot=0.00
        opcion=menu('1. Reportes Ventas|2. Analisis/Reportes Integrados|3. Anulaciones|4. Miscelaneo|5. Ingresos|6. Caja|7. Personal|8. Datos|9. Salir')
        tipo_cambio=set_tipo_cambio(apertura)
        #OPCION 1
        if opcion==1:
            opcion2=menu('1. X Corto|2. X Largo|3. Z|4. Ventas Diarias|5. Delivery|9. Regresar')
            if opcion2==1:
                apertura,cierre=tiempocaja()
                panel_full=mkpanel(curses.COLOR_WHITE,maxy,maxx,0,0)
                win=definir(panel_full)
                impr='1.1. X Corta'
                px=centrar(maxx,impr)
                win.addstr(2,px,impr)
                updat()
                nomarch='Xcorta'+str(int(time.time()))
                archivo=open(nomarch,'w')
                cabecera(archivo,opcion2)
                mntsol,mntdol,nuls,anulaciones,sumtot,total_real=0.0,0.0,0.0,0.0,0.0,0.0
                mntsol,mntdol,nuls,anulaciones,sumtot,total_real=payment_options(apertura,cierre,archivo)
                vales(apertura,cierre,'0',archivo)
                pie(archivo)
                for linea in range(0,9):
                    archivo.write('\n')
                archivo.close()
                impresion(nomarch,gaveta)
                resp=segur('Presione una Tecla para Salir')
                if debug_mode=='0' or debug_mode=='':
                    os.remove(nomarch)
                borscr(panel_full)
            elif opcion2==2:
                apertura,cierre=tiempocaja()
                panel_full=mkpanel(curses.COLOR_WHITE,maxy,maxx,0,0)
                win=definir(panel_full)
                impr='1.2. X Larga'
                px=centrar(maxx,impr)
                win.addstr(2,px,impr)
                updat()
                nomarch='XLarga'+str(int(time.time()))
                resp=segur("Esta seguro(a)? ")
                if resp=='si':
                    archivo=open(nomarch,'w')
                    cabecera(archivo,opcion2)
                    mntsol,mntdol,nuls,anulaciones,sumtot,total_real=0.0,0.0,0.0,0.0,0.0,0.0
                    mntsol,mntdol,nuls,anulaciones,sumtot,total_real=payment_options(apertura,cierre,archivo)
                    vales(apertura,cierre,'0',archivo)
                    pie(archivo)
                    vales(apertura,cierre,'1',archivo)
                    comprobantes(apertura,cierre,archivo)
                    pie(archivo)
                    codigo(apertura,cierre,archivo)
                    pie(archivo)
                    usuarios(apertura,cierre,archivo)
                    pie(archivo)
                    horas(apertura,cierre,archivo)
                    pie(archivo)
                    for linea in range(0,9):
                        archivo.write('\n')
                    archivo.close()
                    impresion(nomarch,gaveta)
                    resp=segur('Presione una Tecla para Salir')
                    if debug_mode=='0' or debug_mode=='':
                        os.remove(nomarch)
                    segur("Al Cierre de Tienda NO SE OLVIDE SACAR LA Z")
                    borscr(panel_full)
            elif opcion2==3:
                apertura,cierre=tiempocaja()
                panel_full=mkpanel(curses.COLOR_WHITE,maxy,maxx,0,0)
                win=definir(panel_full)
                impr='1.3. Z'
                px=centrar(maxx,impr)
                win.addstr(2,px,impr)
                updat()
                nomarch='Z'+str(int(time.time()))
                resp=segur("Esta seguro(a)? ")
                if resp=='si':
                    archivo=open(nomarch,'w')
                    cabecera(archivo,opcion2)
                    mntsol,mntdol,nuls,anulaciones,sumtot,total_real=0.0,0.0,0.0,0.0,0.0,0.0
                    mntsol,mntdol,nuls,anulaciones,sumtot,total_real=payment_options(apertura,cierre,archivo)
                    vales(apertura,cierre,'0',archivo)
                    pie(archivo)
                    vales(apertura,cierre,'1',archivo)
                    comprobantes(apertura,cierre,archivo)
                    pie(archivo)
                    codigo(apertura,cierre,archivo)
                    pie(archivo)
                    usuarios(apertura,cierre,archivo)
                    pie(archivo)
                    horas(apertura,cierre,archivo)
                    pie(archivo)
                    archivo.write('\n')
                    archivo.write('Productos Clave\n')
                    archivo.write('---------------\n')
                    archivo.write('\n')
                    #lineas=almacen(apertura,cierre,0)
                    for data in lineas:
                        if prod_resumen.count(data[0])>0:
                            rprodi=str(data[0])+'---'+str(data[1])
                            archivo.write(rprodi+'\n')
                    ###Fin Productos
                    for linea in range(0,9):
                        archivo.write('\n')
                    archivo.close()
                    impresion(nomarch,gaveta)
                    replicacion('d')
                    ecierre=0
                    ##Cierre
                    conta=0
                    while ecierre==0:
                        ecierre=cierre_caja()
                        conta+=1
                        if conta>50:
                            resp=segur('Se ha encontrado un error en el cierre')
                            break
                    backup()
                    resp=segur('Presione una Tecla para Salir')
                    if debug_mode=='0' or debug_mode=='':
                        os.remove(nomarch)
                    borscr(panel_full)
            elif opcion2==4:#Ventas en Pantalla
                aper,cier=fechai(2,'d')
                if aper=='Anular':
                    pass
                else:
                    if cier=='':
                        cier=aper
                    lineas=payment_options(aper,cier)
                    panelh=mkpanel(curses.COLOR_WHITE,3,20,0,0)
                    panelf=mkpanel(curses.COLOR_WHITE,maxy-3,maxx,3,0)
                    psey=0
                    temc=0
                    while 1:
                        viewtext(lineas,panelf,psey)
                        winz=definewin(panelf,0,0)
                        winz.addstr(0,1,'FP  --       Cantidad       --    Monto')
                        updat()
                        ingdat=ingresodato('Ventas',panelh,10,'',0,0)
                        if ingdat=='Anular':
                            borscr(panelh,panelf)
                            break
                        elif ingdat=='arriba':
                            psey-=1
                        elif ingdat=='abajo':
                            psey+=1
                        else:
                            psey=0
                        temc=abs(psey)
                        if temc>len(lineas):
                            psey=0
            elif opcion2==5:#Delivery
                fech,fechp=fechai(2,'s')
                if fech=='Anular':
                    pass
                else:
                    if fech=='':
                        fech='d'
                    if fechp=='':
                        fechp='d'
                    aper,c1=tiempocaja(fech)
                    a1,cier=tiempocaja(fechp)
                    lineas=delivery(aper,cier)
                    if len(lineas)>0:
                        panelh=mkpanel(curses.COLOR_WHITE,3,20,0,0)
                        panelf=mkpanel(curses.COLOR_WHITE,maxy-3,maxx,3,0)
                        psey=0
                        temc=0
                        while 1:
                            viewtext(lineas,panelf,psey)
                            winz=definewin(panelf,0,0)
                            winz.addstr(0,1,'Tiempo        --       Documento       --     Total')
                            updat()
                            ingdat=ingresodato('Delivery',panelh,10,'',0,0)
                            if ingdat=='Anular':
                                borscr(panelh,panelf)
                                break
                            elif ingdat=='arriba':
                                psey-=1
                            elif ingdat=='abajo':
                                psey+=1
                            else:
                                psey=0
                            temc=abs(psey)
                            if temc>len(lineas):
                                psey=0
            elif opcion2==9:
                pass
        #OPCION 2
        if opcion==2:
            opcion2=menu('1. Salidas por Ventas y Consumos|2. Almacen/Produccion vs Ventas|5. Consumos de Almacen|8. Sugerencia de Venta|9. Regresar')
            if opcion2==1:#Salidas por Ventas
                fech,fechp=fechai(2)
                if fech=='Anular':
                    pass
                else:
                    resp=segur("Lista Larga? ")
                    if resp=='si':
                        modoal=1
                    else:
                        modoal=2
                    if fechp=='':
                        fechp=fech
                    lineas=almacen(fech,fechp,modoal)
                    panelh=mkpanel(curses.COLOR_WHITE,3,20,0,0)
                    panelh2=mkpanel(curses.COLOR_WHITE,3,55,0,21)
                    panelf=mkpanel(curses.COLOR_WHITE,maxy-3,maxx,3,0)
                    psey=0
                    temc=0
                    codex_sel=''
                    winhead('Fechas: '+str(fech)+' / '+str(fechp),panelh2)
                    while 1:
                        viewtext(lineas,panelf,psey,codex_sel)
                        winz=definewin(panelf,0,0)
                        winz.addstr(0,1,'Codigo  ----------       Descripcion      ----------      Cantidad')
                        updat()
                        ingdat=ingresodato('Ventas',panelh,10,'',0,0)
                        if ingdat=='Anular':
                            resp=segur("Esta seguro(a)? ")
                            if resp=='si':
                                borscr(panelh,panelh2,panelf)
                                break
                        elif ingdat=='arriba':
                            psey-=1
                        elif ingdat=='abajo':
                            psey+=1
                        elif ingdat=='ppag':
                            psey-=20
                        elif ingdat=='spag':
                            psey+=20
                        else:
                            codex_sel=ingdat
                            psey=0
                        temc=abs(psey)
                        if temc>len(lineas):
                            psey=0
            if opcion2==2:#Almacen/Produccion vs Ventas
                pass
            if opcion2==5:#Consumos de Almacen
                fech,fechp=fechai(2)
                if fech=='Anular' or fech=='':
                    pass
                else:
                    if fechp=='':
                        fechp=fech
                    lineas=almacen(fech,fechp)
                    panelh=mkpanel(curses.COLOR_WHITE,3,20,0,0)
                    panelf=mkpanel(curses.COLOR_WHITE,maxy-3,maxx,3,0)
                    psey=0
                    temc=0
                    while 1:
                        viewtext(lineas,panelf,psey)
                        winz=definewin(panelf,0,0)
                        winz.addstr(0,1,'Codigo  --       Cantidad       --    Descripcion')
                        updat()
                        ingdat=ingresodato('Ventas',panelh,10,'',0,0)
                        if ingdat=='Anular':
                            borscr(panelh,panelf)
                            break
                        elif ingdat=='arriba':
                            psey-=1
                        elif ingdat=='abajo':
                            psey+=1
                        elif ingdat=='ppag':
                            psey-=20
                        elif ingdat=='spag':
                            psey+=20
                        else:
                            psey=0
                        temc=abs(psey)
                        if temc>len(lineas):
                            psey=0
            if opcion2==8:#Sugerencia de Venta
                break
                fech,fechp=fechai(1,'Dia Sugerido')
                panelh=mkpanel(curses.COLOR_WHITE,3,20,0,0)
                sql="select date_add('"+str(fech)+"',INTERVAL -7 DAY),date_add('"+str(fech)+"',INTERVAL -14 DAY),date_add('"+str(fech)+"',INTERVAL -21 DAY),date_add('"+str(fech)+"',INTERVAL -28 DAY)"
                cuenta,resultado=query(sql,0)
                fech1=ingresodato('Dia 1',panelh,10,resultado[0],1,0)
                fech2=ingresodato('Dia 2',panelh,10,resultado[1],1,0)
                fech3=ingresodato('Dia 3',panelh,10,resultado[2],1,0)
                fech4=ingresodato('Dia 4',panelh,10,resultado[3],1,0)
                porc_cob=ingresodato('% Cob',panelh,10)
                if fech=='Anular' or fech1=='Anular' or fech2=='Anular' or fech3=='Anular' or fech4=='Anular':
                    pass
                else:
                    fech=fech[:10]
                    turno=turnos('1','2')
                    sql="(select pro.fecha,if(length(mae.alias)>0,mae.alias,concat(mae.nombre,' ',mae.descripcion)),round(((sum(pro.canti"+str(turno)+")+(sum(pro.ingtras"+str(turno)+")-sum(pro.saltras"+str(turno)+"))-sum(pro.merm"+str(turno)+"))),0) as pedido from produccion pro inner join relaciones rel on rel.codbarras_hijo=pro.codigo and rel.modo=0 inner join relaciones re2 on re2.codbarras_hijo=rel.codbarras_padre and re2.modo=9 inner join maestro mae on mae.codbarras=re2.codbarras_padre where (pro.fecha='"+str(fech1)+"' or pro.fecha='"+str(fech2)+"' or pro.fecha='"+str(fech3)+"' or pro.fecha='"+str(fech4)+"') and pro.pv="+str(pos_num)+" group by re2.codbarras_padre,pro.fecha"
                    sql+=") union (select '-----','-----','-----'"
                    sql+=") union (select 'Total',if(length(mae.alias)>0,mae.alias,concat(mae.nombre,' ',mae.descripcion)),round(((sum(pro.canti"+str(turno)+")+(sum(pro.ingtras"+str(turno)+")-sum(pro.saltras"+str(turno)+"))-sum(pro.merm"+str(turno)+"))),0) as pedido from produccion pro inner join relaciones rel on rel.codbarras_hijo=pro.codigo and rel.modo=0 inner join relaciones re2 on re2.codbarras_hijo=rel.codbarras_padre and re2.modo=9 inner join maestro mae on mae.codbarras=re2.codbarras_padre where (pro.fecha='"+str(fech1)+"' or pro.fecha='"+str(fech2)+"' or pro.fecha='"+str(fech3)+"' or pro.fecha='"+str(fech4)+"') and pro.pv="+str(pos_num)+" group by re2.codbarras_padre"
                    sql+=") union (select '-----','-----','-----'"
                    sql+=") union (select concat('Sugerencia',' ','"+str(fech)+"'),if(length(mae.alias)>0,mae.alias,concat(mae.nombre,' ',mae.descripcion)),round(round((((sum(pro.canti"+str(turno)+")+(sum(pro.ingtras"+str(turno)+")-sum(pro.saltras"+str(turno)+"))-sum(pro.merm"+str(turno)+"))/4)),0)*(1."+str(porc_cob)+"),0) as pedido from produccion pro inner join relaciones rel on rel.codbarras_hijo=pro.codigo and rel.modo=0 inner join relaciones re2 on re2.codbarras_hijo=rel.codbarras_padre and re2.modo=9 inner join maestro mae on mae.codbarras=re2.codbarras_padre where (pro.fecha='"+str(fech1)+"' or pro.fecha='"+str(fech2)+"' or pro.fecha='"+str(fech3)+"' or pro.fecha='"+str(fech4)+"') and pro.pv="+str(pos_num)+" group by re2.codbarras_padre"
                    sql+=")"
                    lineas,tipo=datos_cons(sql)
                    panelf=mkpanel(curses.COLOR_WHITE,maxy-3,maxx,3,0)
                    psey=0
                    temc=0
                    while 1:
                        viewtext(lineas,panelf,psey)
                        winz=definewin(panelf,0,0)
                        winz.addstr(0,1,'Codigo -- Cantidad')
                        updat()
                        ingdat=ingresodato('Dia '+str(fech),panelh,10,'',0,0)
                        if ingdat=='Anular':
                            break
                        elif ingdat=='arriba':
                            psey-=1
                        elif ingdat=='abajo':
                            psey+=1
                        else:
                            psey=0
                        temc=abs(psey)
                        if temc>len(lineas):
                            psey=0
                borscr(panelh,panelf)
            if opcion2==9:#Salir
                pass
        #OPCION 3
        if opcion==3 and nivel<=6:#Anulaciones
            proc_anulacion()
        #OPCION 4
        if opcion==4:#Miscelaneo
            opcion2=menu('1. Abrir Gaveta|4. Documentos Manuales|9. Regresar')
            if opcion2==1:
                if gaveta=='':
                    os.system('/bin/cat apertura | escpos > '+print_port)
                else:
                    os.system('ls > /dev/'+gaveta)
            elif opcion2==4:
                aper,cier=fechai(1,'s')
                if aper=='Anular':
                    pass
                else:
                    if cier=='':
                        cier=aper
#                   print aper
#                   print cier
#                   sys.exit()
#                   aper,cier=tiempocaja(aper)
                    sql="select comprobante,n_doc_base,codigo,cantidad,total from docventa where fecha_vta between date('"+str(aper)+"') and date('"+str(cier)+"') and comprobante>7"
                    lineas,tipo=datos_cons(sql)
                    doc_m=doc_man(aper)
                    cab2=string.join(doc_m)
                    panelh=mkpanel(curses.COLOR_WHITE,3,20,0,0)
                    panelh2=mkpanel(curses.COLOR_WHITE,3,50,0,25)
                    panelf=mkpanel(curses.COLOR_WHITE,maxy-3,maxx,3,0)
                    psey=0
                    temc=0
                    win2=definewin(panelh2,0,0)
                    win2.addstr(0,1,'Totales -- '+str(cab2))
                    while 1:
                        viewtext(lineas,panelf,psey)
                        winz=definewin(panelf,0,0)
                        winz.addstr(0,1,'Comprob -- Documento --  Codigo  --  Cant  --     Total')
                        updat()
                        ingdat=ingresodato('Comprobantes',panelh,10,'',0,0)
                        if ingdat=='Anular':
                            borscr(panelh,panelf,panelh2)
                            break
                        elif ingdat=='arriba':
                            psey-=1
                        elif ingdat=='abajo':
                            psey+=1
                        else:
                            psey=0
                        temc=abs(psey)
                        if temc>len(lineas):
                            psey=0
            elif opcion2==8:
                resp=segur('ADVERTENCIA: Esta seguro?')
                if resp=='si':
                    ecierre=0
                    conta=0
                    while ecierre==0:
                        ecierre=cierre_caja()
                        conta+=1
                        if conta>50:
                            resp=segur('Error en el Cierre. Duplicado? ')
                            break
            else:
                pass
        #OPCION 5
        if opcion==5:#Ingresos
            while 1:
                opcion2=menu('1. Mermas|2. Guias|3. Transferencias|4. Variedades|5. Inventarios|6. Bancos|7. Consumo Interno|8. Pedidos|9. Regresar')
                if opcion2==1:#Mermas
                    opcion3=menu('1. Productos|2. Variedad|9. Regresar')
                    if opcion3==1:#Mermas de Productos
                        #def data_proc(tipo_mov=1,doc_modo=1,doc_tipo=6,txt_fld=3,fech_cnt=1,fech_hea='t',turno_ing=1,masa_ing=1,impresion=1,oper_log='IPT',alm_rel='0101',alm_base='0100',oper_log_pref='1',add_data='',prod_filt='genero="0002"'):
                        data_proc(1,1,6,3,1,'',1,0,0,'SXM',pos_num,'0021','4','','(genero="0001" or genero="0002" or genero="0003")')
                    elif opcion3==2:#Mermas de Variedad
                        derivados_proc(3,'',pos_num,'sal_merma')
#                   elif opcion3==1:#Mermas de Productos
                        #def data_proc(tipo_mov=1,doc_modo=1,doc_tipo=6,txt_fld=3,fech_cnt=1,fech_hea='t',turno_ing=1,masa_ing=1,impresion=1,oper_log='IPT',alm_rel='0101',alm_base='0100',oper_log_pref='1',add_data='',prod_filt='genero="0002"'):
#                       data_proc(1,1,6,3,1,'',1,0,0,'SXM',pos_num,'0021','4','','(genero="0001" or genero="0002")')
                    elif opcion3==9:
                        pass
                if opcion2==2:#Guias de Remision
                    #def data_proc(tipo_mov=1,doc_modo=1,doc_tipo=6,txt_fld=3,fech_cnt=1,fech_hea='t',turno_ing=1,masa_ing=1,impresion=1,oper_log='IPT',alm_rel='0101',alm_base='0100',oper_log_pref='1',add_data='',prod_filt='genero="0002"'):
                    data_proc(1,1,6,3,1,'',1,0,0,'IST','0099',pos_num,'4','','(genero="0001" or genero="0002")')
                if opcion2==3:#Transferencias
                    opcion3=menu('1. Productos|2. Variedad|9. Regresar')
                    if opcion3==1:#Transferencias de Productos
                        data_proc(1,1,6,3,1,'',1,0,0,'ITT',pos_num,'','4','','(genero="0001" or genero="0002")')
                    if opcion3==2:#Transferencias de Variedad
                        derivados_proc(3,pos_num,'','sal_traslado')
                    if opcion3==9:
                        break
                if opcion2==4:#Variedades
                    derivados_proc(3,'',pos_num,'ing_produccion|ing_traslado')
                if opcion2==5:#Inventarios
                    inventarios(pos_num)
                if opcion2==6:#Bancos
                    tipo=1
                    psey=0
                    temc=0
                    total=0
                    agencia=''
                    glosa1=''
                    glosa2=''
                    pm=0.0
                    panelt=mkpanel(curses.COLOR_WHITE,3,maxx,0,0)
                    panelh=mkpanel(curses.COLOR_WHITE,3,20,3,0)
                    panelh2=mkpanel(curses.COLOR_WHITE,3,20,3,20)
                    panelh21=mkpanel(curses.COLOR_WHITE,3,20,3,40)
                    panelh3=mkpanel(curses.COLOR_WHITE,3,40,6,0)
                    panelh5=mkpanel(curses.COLOR_WHITE,3,20,6,40)
                    panelf=mkpanel(curses.COLOR_WHITE,maxy-9,(maxx/2)+15,9,0)
                    panelf2=mkpanel(curses.COLOR_WHITE,maxy-9,(maxx/2)-15,9,(maxx/2)+15)
                    panelf3=mkpanel(curses.COLOR_WHITE,3,15,6,60)
                    fechav,fechad=fechai(2,'b')
                    if (fechav=='' or fechav=='Anular') or fechad=='Anular':
                        borscr(panelt,panelh,panelh2,panelh21,panelh3,panelh5,panelf,panelf2,panelf3)
                        break
                    tipo_cambio=set_tipo_cambio(fechav)
                    if fechad=='':
                        fechad=time.strftime("%Y-%m-%d")
                    sql="select abs(datediff('"+str(fechav)+"','"+str(fechad)+"'))"
                    cuenta,resultado=query(sql,0)
                    if cuenta>0:
                        dias_valid=int(resultado[0])
                        if dias_valid>3:
                            segur("Los depositos deben realizarse hasta 3 dias despues de la venta")
                            break
                    else:
                        break
                    sql="select banco,monto,cambio,glosa1,glosa2,agencia from bancos where fechav='"+str(fechav)+"'"
                    cuentaz,resultadoz=query(sql)
                    if cuentaz>0:
                        lineas=[]
                        for x in range(0,cuentaz):
                            temp=resultadoz[x]
                            datemp=[]
                            for y in range(0,2):
                                datemp.append(temp[y])
                            pm=float(temp[1])
                            if temp[0]=='002' or temp[0]=='005':
                                pm=pm*tipo_cambio
                            total+=pm
                            sql1="select entidad from cuentas where codigo='"+str(temp[0])+"'"
                            cuentaz1,resultadoz1=query(sql1,0)
                            datemp.append(resultadoz1[0])
                            lineas.append(datemp)
                        cambio=resultadoz[0][2]
                        glosa1=resultadoz[0][3]
                        glosa2=resultadoz[0][4]
                        agencia=resultadoz[0][5]
                    else:
                        lineas=[]
                    while 1:
                        if agencia=='':
                            agencia=ingresodato('Agencia',panelh,10,'',1,0)
                        else:
                            winz=definir(panelh)
                            winz.addstr(1,1,'Agencia: '+str(agencia))
                        if agencia!='':
                            break
                    while 1:
                        if glosa1=='':
                            glosa1=ingresodato('Glosa1',panelh2,10,'',1,0)
                            if glosa1=='Anular':
                                glosa1=' '
                        else:
                            winz=definir(panelh2)
                            winz.addstr(1,1,'Glosa1: '+str(glosa1))
                        if glosa1!='':
                            break
                    while 1:
                        if glosa2=='':
                            glosa2=ingresodato('Glosa2',panelh21,10,'',1,0)
                            if glosa2=='Anular':
                                glosa2=' '
                        else:
                            winz=definir(panelh21)
                            winz.addstr(1,1,'Glosa2: '+str(glosa2))
                        if glosa2!='':
                            break
                    winhead('Bancos --- Ventas: '+str(fechav)+' // Deposito: '+str(fechad),panelt)
                    datos=[]
#                   aper,cier=tiempocaja(fechav)
                    tempo=payment_options(fechav,fechav)
                    for linea in tempo[:9]:
                        datos.append(linea)
                    for linea in tempo[-4:]:
                        datos.append(linea)
                    total_vta=vta_total(fechav)
                    while 1:
                        if apertura=='0000-00-00 00:00:00':
                            break
                        viewtext(lineas,panelf,psey)
                        viewtext(datos,panelf2,psey)
                        winz=definir(panelf3)
                        winz.addstr(1,1,'T: '+str(total))
                        ingdat=segur('Comando:',3,60)
                        if ingdat=='Anular':
                            resp=segur("Esta seguro(a)? ")
                            if resp=='si':
                                borscr(panelt,panelh,panelh2,panelh21,panelh3,panelh5,panelf,panelf2,panelf3)
                                break
                        dif_comp=round(round(total,2)-round(total_vta,2),2)
                        save_allow=0
                        if dif_comp>=0:
                            save_allow=1
                        if ingdat=='grabar' and save_allow==1:#and round(total,2)>=round(total_vta,2):
                            save_cont=1
                            if dif_comp>0:
                                resp=segur("Existe un Excedente de "+str(dif_comp)+", esta seguro?")
                                if resp=='si':
                                    save_cont=1
                                    mensaje="Monto de la Venta:"+str(total_vta)+"- Monto del Deposito:"+str(total)
                                    alerta(mensaje,'ALERTA DE DEPOSITOS')
                                else:
                                    save_cont=0
                            if save_cont==1:
                                ingdat2=segur('Guardar?',3,61)
                                if ingdat2=='si':
                                    sql="delete from bancos where fechav='"+str(fechav)+"'"
                                    exe = query(qsql, 3)
                                    for z in range(0,len(lineas)):
                                        temporal=lineas[z]
                                        temporal=agregar_valores(temporal,[0,1],fechav,fechad,pos_num,tipo_cambio,glosa1,glosa2,agencia)
                                        base=sqlsend(temporal,'banco,monto,fechav,fechad,pv,cambio,glosa1,glosa2,agencia',1)
                                        sql_ing="insert into bancos "+base
                                        exe = query(sql_ing, 3)
                                    borscr(panelt,panelh,panelh2,panelh21,panelh3,panelh5,panelf,panelf2,panelf3)
                                    break
                        else:
                            segur("Existe una Diferencia de "+str(dif_comp))
                        sql9="select codigo,concat(entidad,'-',moneda) from cuentas where codigo!='000' order by codigo asc"
                        cuenta9,resultado9=query(sql9,1)
                        banco,nombre=ladocl(resultado9,'Cuentas')
                        if nombre!='Anular':
                            temporal=string.split(nombre,'-')
                            nombre=temporal[0]
                            moneda=temporal[1]
                            winh3=definir(panelh3)
                            winh3.addstr(1,1,'Banco: '+str(nombre)+' -> '+str(banco))
                            while 1:
                                monto=ingresodato('Monto',panelh5,12,'',1,0)
                                if monto=='Anular':
                                    break
                                else:
                                    try:
                                        monto=float(monto)
                                        break
                                    except:
                                        pass
                            if banco=='Anular' or monto=='Anular':
                                resp=segur("Esta seguro(a)? ")
                                if resp=='si':
                                    borscr(panelt,panelh,panelh2,panelh21,panelh3,panelh5,panelf,panelf2,panelf3)
                                    break
                                else:
                                    monto=0
                            elif monto=='arriba':
                                psey-=1
                            elif monto=='abajo':
                                psey+=1
                            else:
                                prov=agregar_valores([],0,banco,monto,nombre[:13])
                                lineas.append(prov)
                            temc=abs(psey)
                            if temc>len(lineas):
                                psey=0
                            if moneda=='2' or moneda==2:
                                monto=float(monto)*tipo_cambio
                            total+=float(monto)
                if opcion2==7:#Consumos Internos
#                   permiso=permisos_acceso(0,codven,str(opcion2)+'.0')
#                   if permiso==0:
#                       segur("No tiene permisos para Acceder a este Modulo")
#                       break
                    opcion3=menu('1. Productos-Checklist Tienda|2. Productos-Checklist General|3. Productos-Entrenamiento|4. Productos-Consumo Tienda|8. Variedad|9. Regresar')
                    if opcion3==1:#Consumo Interno de Productos Checklist Tienda
                        data_proc(1,1,6,3,1,'',1,0,0,'SKT',pos_num,'0021','4','','(genero="0001" or genero="0002" or genero="0003")')
                    elif opcion3==2:#Consumo Interno de Productos Checklist
                        data_proc(1,1,6,3,1,'',1,0,0,'SKG',pos_num,'0021','4','','(genero="0003")')
                    elif opcion3==3:#Consumo Interno de Productos Entrenamiento
#                       permiso=permisos_acceso(0,codven,str(opcion2)+'.'+str(opcion3))
#                       if permiso==0:
#                           break
                        data_proc(1,1,6,3,1,'',1,0,0,'SKE',pos_num,'0021','4','','(genero="0001" or genero="0002" or genero="0003")')
                    elif opcion3==4:#Consumo Tienda
                        data_proc(1,1,6,3,1,'',1,0,0,'SKI',pos_num,'0021','4','','(genero="0003")')
                    elif opcion3==8:#Consumo Interno de Variedad
                        derivados_proc(3,'',pos_num,'sal_consumo_int')
                if opcion2==8:#Pedidos
                    aper,cier=fechai(1,'Dia (AAMMDD)')
                    if aper=='Anular':
                        pass
                    else:
                        opcion4=menu('1. Donuts|2. Productos|3. Especiales Donuts|4. Especiales Variedad|5. Especiales Otros|6. Emergencia|9. Anular')
                        if opcion4==1:
                            guia='-'+aper[2:4]+aper[5:7]+aper[8:10]+str(pos_num[2:4])+'-PE'
                            tipo_ped='0'
                            condic_sql="genero='0002'"
                        elif opcion4==2:
                            guia='-'+aper[2:4]+aper[5:7]+aper[8:10]+str(pos_num[2:4])+'-PR'
                            tipo_ped='1'
                            condic_sql="genero='0001'"
                        elif opcion4==3:
                            guia='-'+aper[2:4]+aper[5:7]+aper[8:10]+str(pos_num[2:4])+'-ES'
                            tipo_ped='2'
                            condic_sql="genero='0002'"
                        elif opcion4==4:
                            guia='-'+aper[2:4]+aper[5:7]+aper[8:10]+str(pos_num[2:4])+'-FI'
                            tipo_ped='3'
                            condic_sql="genero='0004'"
                        elif opcion4==5:
                            guia='-'+aper[2:4]+aper[5:7]+aper[8:10]+str(pos_num[2:4])+'-OT'
                            tipo_ped='4'
                            condic_sql="genero='0001'"
                        elif opcion4==6:
                            guia='-'+aper[2:4]+aper[5:7]+aper[8:10]+str(pos_num[2:4])+'-EM'
                            tipo_ped='5'
                            condic_sql="(genero='0001' or genero='0002')"
                        elif opcion4==9:
                            break
                        guia_prefijo,guia,guia_sufijo=guias(guia)
                        guia_completa=str(guia_prefijo)+'-'+str(guia)+'-'+str(guia_sufijo)
                        if opcion4==1 or opcion4==3 or opcion4==4 or opcion4==6:
                            turno=turnos()
                        else:
                            turno='00001'
                        panelt=mkpanel(curses.COLOR_WHITE,3,maxx,0,0)
                        panelh=mkpanel(curses.COLOR_WHITE,3,20,3,0)
                        panelh2=mkpanel(curses.COLOR_WHITE,3,20,3,20)
                        panelh3=mkpanel(curses.COLOR_WHITE,3,20,3,40)
                        panelh4=mkpanel(curses.COLOR_WHITE,3,20,3,60)
                        panelf=mkpanel(curses.COLOR_WHITE,maxy-6,maxx,6,0)
                        sql="select a.codbarras,a.cantidad,if(length(b.alias)>0,b.alias,concat(b.nombre,' ',b.descripcion)) from pedidos as a,maestro as b where a.n_doc_prefijo='"+str(guia_prefijo)+"' and a.n_doc_base='"+str(guia)+"' and a.n_doc_sufijo='"+str(guia_sufijo)+"' and a.codbarras=b.codbarras and a.modo='"+str(tipo_ped)+"' and a.turno='"+str(turno)+"' and a.fecha='"+str(aper)+"'"
                        lineas,tipo=datos_cons(sql)
                        psey=0
                        temc=0
                        winhead('Pedido: '+str(guia_completa)+' / '+str(tipo_ped)+' / '+str(turno),panelt)
                        while 1:
                            viewtext(lineas,panelf,psey)
                            ingdat,cuenta=datopc("Codigo",panelh,10,"insert,arriba,abajo,Anular",condic_sql)
                            cuenta,resultado=query("select nombre,descripcion from maestro where codbarras='"+str(ingdat)+"'",0)
                            if cuenta>0:
                                cantidad=datesp('Cantidad',panelh2,8,'decimal,entero')
                                nombre=resultado[0]
                                descripcion=resultado[1]
                                motip=modo_ingr(lineas)
                                prov=agregar_valores([],0,ingdat,cantidad,nombre+'/'+descripcion,motip)
                                lineas.append(prov)
                            if ingdat=='Anular':
                                resp=segur("Esta seguro(a)? ")
                                if resp=='si':
                                    borscr(panelt,panelh,panelh2,panelh3,panelh4,panelf)
                                    break
                            if ingdat=='insert':
                                fecha=aper
                                for z in range(0,len(lineas)):
                                    if lineas[z][3]=='0':
                                        base=sqlsend(lineas[z],"codbarras,cantidad",0)
                                        sql="update pedidos set "+base+",user_ing='"+str(idven)+"' where fecha='"+str(fecha)+"' and n_doc_prefijo='"+str(guia_prefijo)+"' and  n_doc_base='"+str(guia)+"' and n_doc_sufijo='"+str(guia_sufijo)+"' and codbarras='"+str(lineas[z][0])+"' and modo='"+str(tipo_ped)+"' and turno='"+str(turno)+"'"
                                    else:
                                        temporal=lineas[z]
                                        temporal=agregar_valores(temporal,2,guia_prefijo,guia,guia_sufijo,pos_num,idven,codven,fecha,turno,tipo_ped)
                                        base=sqlsend(temporal,"codbarras,cantidad,n_doc_prefijo,n_doc_base,n_doc_sufijo,pv,user_req,user_ing,fecha,turno,modo",1)
                                        sql="insert into pedidos "+base
                                    exe = query(sql, 3)
                                borscr(panelt,panelh,panelh2,panelh3,panelh4,panelf)
                                break
                            if ingdat=='arriba':
                                psey-=1
                            if ingdat=='abajo':
                                psey+=1
                            temc=abs(psey)
                            if temc>len(lineas):
                                psey=0
                if opcion2==9:
                    break
        #OPCION 6
        if opcion==6 and nivel<=9:
            gestion_caja()
        #OPCION 7
        if opcion==7:
            gestion_asistencia()
            codven=0
            nomven='I'
            nivel=0
            break
        #OPCION 8
        if opcion==8 and nivel<=10:
            fech,fechp=fechai(1)
            if fech=='Anular':
                pass
            else:
                if fech[:10]==time.strftime("%Y-%m-%d"):
                    fech='d'
                replicacion(fech)
        #OPCION 9
        if opcion==9:
            opcion2=menu('1.Cambiar Usuario|2.Apagar|3.Reiniciar|8.Cerrar Aplicacion|9.Regresar')
            if opcion2==1:
                codven=0
                nomven='I'
                nivel=0
                break
            elif opcion2==2:
                a=os.popen('sudo /sbin/shutdown -h now')
            elif opcion2==3:
                a=os.popen('sudo /sbin/shutdown -r now')
            elif opcion2==8 and nivel<5:
                curses.echo()
                curses.endwin()
                sys.exit()
            else:
                pass
                
