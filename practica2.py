'''
Created on 15 dic. 2020

@author: matgu
'''
# Diferentes librerías importadas para su uso dentro de las funciones
import regex as re
import cv2
import sys
from datetime import time
import datetime

# Función encargada del menú donde elegir que función realizar
def menú():
    # Sucesión de prints que crear la "interfaz" del menú. A continuación, se pide el carácter que indicará que función se llamará
    print("A: Añadir registro de presencia")
    print("G: Generar salida")
    print("C: Control de presencia")
    print("S: Salir del programa")
    caracter = input(">> ")
    print()
    
    # Análisis de casos entre las diferentes funciones posibles del menú
    if caracter=="S" or caracter=="s":
        SystemExit()
    elif caracter=="A" or caracter=="a":
        añadirregistro()
    elif caracter=="G" or caracter=="g":
        generarsalida()
    elif caracter=="C" or caracter=="c":
        controlpresencia()
        
# Función encargada de añadir un registro al fichero de log.txt
def añadirregistro():
    
    # Patrones usados para las expresiones regulares
    patrón_fecha = r'([012]\d|3[01])(/|-)(0\d|1[012])\2(\d{4})'
    patrón_hora = r'([01]\d|2[0-3]):([0-5]\d):([0-5]\d)'
    patrón_ruta = r'\./recintos/.+\.png'
    patrón_móvil = r'(6\d{2})( ?)(\d{3})( ?)(\d{3})'
    patrón_acción = r'[Ii][Nn]|[Oo][Uu][Tt]'
    patrón_fechafichero = r'\[ Day (\d{4}) - (0\d|1[012]) - ([012]\d|3[01]) , ([01]\d|2[0-3]) : ([0-5]\d) : ([0-5]\d) ]'
    patrón_qr=r'0(\d)\.ED0(\d{2})\...\.\d\.\d{3}'
    patrón_edificio = r'^(\d);(\d{1,3})'
    patrón_qr_incompleto = r'ED0(\d{2})\...\.\d\.\d{3}'
    
    # Expresiones reguladas ya compiladas
    er_fecha = re.compile(patrón_fecha)
    er_hora = re.compile(patrón_hora)
    er_ruta = re.compile(patrón_ruta)
    er_móvil = re.compile(patrón_móvil)
    er_acción = re.compile(patrón_acción)
    er_fechafichero = re.compile(patrón_fechafichero)
    er_qr = re.compile(patrón_qr)
    er_edificio = re.compile(patrón_edificio)
    er_qr_incompleto = re.compile(patrón_qr_incompleto)
    
    # Método try-except para comprobar si el fichero existe o no. Si no existe, lo crea
    try:
        archivo = open('log.txt', 'r')
    except FileNotFoundError:
        print("El fichero no existe", file=sys.stderr)
        archivo = open('log.txt', 'w')
    archivo.close()
    
    # Recorremos el archivo para coger la última línea 
    archivo = open('log.txt', 'r')
    aux=""
    for linea in archivo:
        aux=linea
        
    archivo.close()
    
    
    fechaanterior = datetime.datetime(2020, 12, 31, 0, 0, 0)
    
    # Variable auxiliar donde inicializamos la fecha anterior
    fechaaux = er_fechafichero.match(aux)
    if fechaaux:
            añofechaaux = fechaaux.group(1)
            mesfechaaux = fechaaux.group(2)
            díafechaaux = fechaaux.group(3)
            horasfechaaux = fechaaux.group(4)
            minutosfechaaux = fechaaux.group(5)
            segundosfechaaux = fechaaux.group(6)
            fechaanterior = datetime.datetime(int(añofechaaux), int(mesfechaaux), int(díafechaaux), int(horasfechaaux), int(minutosfechaaux), int(segundosfechaaux))
            horaanterior = time(fechaanterior.hour, fechaanterior.minute, fechaanterior.second)
            
    díasiguales=False
    
    # Declaración de las horas mínimas y máximas
    horamínima = time(8,30,0)
    horamáxima = time(21,0,0)
    
    # Comprobamos primeramente si la fecha es cadena vacía o no
    vacío=False
    fecha = input("Fecha: ")
    if fecha=="":
        vacío=True
    iterador=True
    
    # Primer if que calcula el dato de fecha, teniendo en cuenta todas las condiciones propuestas
    if not vacío:
        while iterador and not vacío:
            if er_fecha.match(fecha)==None:
                print("Formato incorrecto, vuelve a introducir el dato")
                
            resul = er_fecha.match(fecha)
            if resul and not vacío:
                año = resul.group(1)
                mes = resul.group(3)
                día = resul.group(4)
                
                d = datetime.datetime(int(día), int(mes), int(año), 23, 59, 59)
                tt = d.timetuple()
                día_semana = tt[6]
                iterador=False
                if día_semana>4:
                    iterador=True
                    print("Fecha fuera de rango, vuelve a introducir el dato")
                if d<fechaanterior:
                    iterador=True
                    print("Fecha anterior a última entrada, vuelve a introducir el dato")
                if d==fechaanterior:
                    díasiguales=True
            if iterador==True:
                fecha = input("Fecha: ")
    # Segundo if que calcula el dato de hora, teniendo en cuenta todas las condiciones propuestas
    if not vacío:
        hora = input("Hora: ")
        if hora=="":
            vacío=True
        iterador=True
        while iterador and not vacío:
            if er_hora.match(hora)==None:
                print("Formato incorrecto, vuelve a introducir el dato")        
            
            resul2 = er_hora.match(hora)
            if resul2:
                horas = resul2.group(1)
                minutos = resul2.group(2)
                segundos = resul2.group(3)
                
                d2 = time(int(horas), int(minutos), int(segundos))
                iterador=False
                
                if (d2<horamínima) or (d2>horamáxima):
                    iterador=True
                    print("Hora fuera de rango, vuelve a introducir el dato")
                    
                if díasiguales==True:
                    if d2<horaanterior:
                        iterador=True
                        print("Hora anterior a última entrada, vuelve a introducir el dato")
            if iterador==True:
                hora = input("Hora: ")
    # Tercer if que calcula el dato de la ruta QR, teniendo en cuenta todas las condiciones propuestas       
    if not vacío:
        ruta = input("Ruta QR: ")
        if ruta=="":
            vacío=True
        iterador=True
        while iterador and not vacío:
            iterador=False
            if er_ruta.match(ruta)==None:
                iterador=True
                print("Formato incorrecto, vuelve a introducir el dato")
            
            imagen = cv2.imread(ruta)
            try:
                if imagen is None :
                    print("Error leyendo fichero")
                else:
                    detectorQR = cv2.QRCodeDetector()
                    texto, puntos, _ = detectorQR . detectAndDecode(imagen)
                    texto = texto.replace('_','.')
                    if puntos is not None:
                        archivo2 = open('edificios.csv', 'r+', encoding="utf8")
                        cv2.imshow("Codigo QR", imagen)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        archivo2lineas = archivo2.readlines()
                        if not er_qr.match(texto):
                            for línea in archivo2lineas:
                                qrresul = er_edificio.match(línea)
                                textoresul = er_qr_incompleto.match(texto)
                                if qrresul and textoresul:
                                    if int(textoresul.group(1))==int(qrresul.group(2)):
                                        texto="0"+qrresul.group(1)+"."+texto
                                        print(texto)
                                        print("Código patrimonial válido")
                        else:
                            patrimonioválido=False
                            for línea in archivo2lineas:
                                qrresul = er_edificio.match(línea)
                                textoresul = er_qr.match(texto)
                                if qrresul and textoresul:
                                    if textoresul.group(1)==qrresul.group(1) and textoresul.group(2)==qrresul.group(2):
                                        print("Código patrimonial válido")
                                        patrimonioválido=True
                            if not patrimonioválido:
                                print("Código patrimonial inválido")
                        archivo2.close()
                    else:
                        print ("Código QR no detectado")
            except FileNotFoundError:
                iterador=True
                print("Archivo no encontrado, vuelve a introducir el dato")
    
            if iterador==True:
                ruta = input("Ruta QR: ")
    # Cuarto if que calcula el dato de móvil, teniendo en cuenta todas las condiciones propuestas
    if not vacío:
        móvil = input("Móvil: ")
        if móvil=="":
            vacío=True
        iterador=True
        while er_móvil.match(móvil)==None and not vacío:
            print("Formato incorrecto, vuelve a introducir el dato")
            móvil = input("Móvil: ")
        resulmovil = er_móvil.match(móvil)
        if resulmovil:
            dígitos1=resulmovil.group(1)
            dígitos2=resulmovil.group(3)
            dígitos3=resulmovil.group(5)
    
    # Quinto if que calcula el dato de 
    if not vacío:
        acción = input("Acción: ")
        if acción=="":
            vacío=True
        while er_acción.match(acción)==None and not vacío:
            print("Formato incorrecto, vuelve a introducir el dato")
            acción = input("Acción: ")
    # Abrimos el fichero en modo escritura sin vaciar y escribimos el registro a añadir. Por último se cierra el fichero.
    if not vacío:
        print("--")
        archivo = open('log.txt', 'a')
        
        archivo.write("[ Day "+str(día)+" - "+str(mes)+" - "+str(año)+" , "+str(horas)+" : "+str(minutos)+" : "+str(segundos)+" ] Location : "+str(texto)+" , User : "+str(dígitos1)+" "+str(dígitos2)+" "+str(dígitos3)+" "+str(acción)+"\n")
        
        archivo.close()
        archivo2.close()
        
        # Se muestra por pantalla el registro que se acaba de añadir
        print("Registro añadido correctamente: ")
        print("[ Day ", día," - ", mes," - ", año," , ", horas," : ", minutos," : ", segundos," ] Location : ", texto," , User : ", dígitos1," ", dígitos2," ", dígitos3," ", acción)
    
    # Si alguno de los datos es una línea vacía, se vuelve al menú
    if vacío:
        print()
        menú()
    
    
# Función encargada de generar la salida del fichero log.txt en otro llamado log.csv
def generarsalida():

    print("Generando fichero log.csv")    
    print("--")
    
    # Abrimos ambos archivos
    archivo = open('log.txt', 'r', encoding="utf8")
    archivo2 = open('log.csv', 'w', encoding="utf8")
    archivo2.close()

    # Patrones usados para las expresiones regulares
    patrón=r'\[ Day (\d{4}) - (0\d|1[012]) - ([012]\d|3[01]) , (([01]\d|2[0-3]) : [0-5]\d : [0-5]\d) ] Location : 02.(ED\d{3}\...\.\d\.\d{3}) , User : (6\d{2} \d{3} \d{3}) (in|out)'
    patrón2=r'(ED\d{3};..;\d;\d{3});(in|out);(6\d{2}\d{3}\d{3});(([01]\d|2[0-3]):[0-5]\d:[0-5]\d);([012]\d|3[01])/(0\d|1[012])/\d{4}'

    # Expresiones reguladas ya compiladas
    er_patrón=re.compile(patrón)
    er_patrón2=re.compile(patrón2)
    
    # Inicializamos las variables encargadas de los registros válidos, erróneos y redundantes
    válidos=0
    erróneos=0
    redundantes=0
    
    # Inicializamos el contador de las líneas del archivo
    contador=1
    # Primer bucle que recorre cada linea del archivo log.txt
    for linea in archivo:
        escribir=True
        resul_patrón = er_patrón.match(linea)
        if resul_patrón:
            # Asignamos los diferentes datos de hora, fecha, ruta, móvil y acción al formato adecuado
            hora=resul_patrón.group(4)
            hora=hora.replace(" ","")

            año=resul_patrón.group(1)
            mes=resul_patrón.group(2)
            día=resul_patrón.group(3)
            
            ruta=resul_patrón.group(6)
            ruta=ruta.replace(".",";")
            
            móvil=resul_patrón.group(7)
            móvil=móvil.replace(" ","")
            
            acción=resul_patrón.group(8)
            escribir=True
            archivo2 = open('log.csv', 'r', encoding="utf8")
            # No comprobamos si los patrimonios son válidos porque se supone que si se registran en el log.txt, es ppr
            # Segundo bucle que recorre cada linea ya registrada del archivo log.csv
            for línea in archivo2:
                redundancia=True
                if er_patrón2.match(línea):
                    resul2_patrón = er_patrón2.match(línea)
                    if resul2_patrón:
                        # Se obtienen los valores de ruta, móvil y acción de la linea del archivo log.csv       
                        ruta2=resul2_patrón.group(1)
                        móvil2=resul2_patrón.group(3)
                        acción2=resul2_patrón.group(2)
                        # Condición a la que se entra solo cuando las rutas, móviles y acciones de ambas lineas son iguales
                        if móvil==móvil2 and ruta==ruta2 and acción==acción2:
                            for auxiliar in archivo2:
                                resulaux=er_patrón2.match(auxiliar)
                                if resulaux:
                                    movilaux=resulaux.group(3)
                                    if movilaux==móvil2 and not auxiliar==línea:
                                        redundancia=False
                                        break     
                            # Condición a la que se entra cuando la acción en común de los registros sea "out" y haya redundancia                           
                            if acción=="out" and redundancia:
                                archivo2.close()
                                archivo2 = open('log.csv', 'r', encoding="utf8")
                                lineasarchivo = archivo2.readlines()
                                redundantes=redundantes+1
                                válidos=válidos-1
                                archivo2.close()
                                archivo2 = open('log.csv', 'w', encoding="utf8")
                                for line in lineasarchivo:
                                    if line != línea:
                                        archivo2.write(line)
                                archivo2.close()
                                archivo2 = open('log.csv', 'r', encoding="utf8")
                                break
                            # Condición a la que se entra cuando la acción en común de los registros sea "in" y haya redundancia
                            elif acción=="in" and redundancia:
                                redundantes=redundantes+1
                                válidos=válidos-1
                                escribir=False
                                break
            archivo2.close()
            archivo2 = open('log.csv', 'a+', encoding="utf8")
            # Escribimos el registro con el formato pedido en el archivo log.csv
            if escribir:
                archivo2.write(str(ruta)+";"+str(acción)+";"+str(móvil)+";"+str(hora)+";"+str(día)+"/"+str(mes)+"/"+str(año)+"\n")
                válidos=válidos+1
            archivo2.close()       
        # Se entrará en este else solo cuando nos encontremos con un registro erróneo (formato inválido)             
        else:
            archivo2 = open('log.csv', 'a+', encoding="utf8")
            # Escribimos un string que represente la línea con formato incorrecto
            archivo2.write("Línea numero "+str(contador)+", formato incorrecto\n")
            archivo2.close()
            erróneos=erróneos+1
        # Se cierra el archivo log.csv
        archivo2.close()
        archivo2 = open('log.csv', 'a+', encoding="utf8")
        archivo2.close()
        contador=contador+1
    # Se imprimen por pantalla el conteo de los registros válidos, erróneos y redundantes
    print("Registros válidos: ", válidos)
    print("Registros erróneos: ", erróneos)
    print("Registros redundantes: ", redundantes)
    # Cerramos el archivo log.txt
    archivo.close()
    
def controlpresencia():
    
    # Comprobamos si el archivo log.csv existe o no. Si no existe, se pide crearlo a través de la función "generarsalida"
    try:
        archivo = open('log.csv', 'r', encoding="utf8")
    except FileNotFoundError:
        print("Primero tienes que generar la salida\n")
        menú()
    archivo.close()
    
    # Patrones usados para las expresiones regulares
    patrón_teléfono = r'.+((6\d{2})( ?)(\d{3})( ?)(\d{3}))'
    patrón_fecha = r'.+(([012]\d|3[01])([/-])(0\d|1[012])\3(\d{4}))'
    patrón_lugar = r'(ED0(\d{2});..;\d;\d{3})'
    patrón_edificio = r'^(\d);(\d{1,3});(.+)'
    patrón_lineacsv = r'ED\d{3};..;\d;\d{3};.+;(6\d{2}\d{3}\d{3});(([01]\d|2[0-3]):([0-5]\d):([0-5]\d));(([012]\d|3[01])/(0\d|1[012])/(\d{4}))'
    
    # Expresiones reguladas ya compiladas
    er_teléfono = re.compile(patrón_teléfono)
    er_fecha = re.compile(patrón_fecha)
    er_lugar = re.compile(patrón_lugar)
    er_edificio = re.compile(patrón_edificio)
    er_lineacsv = re.compile(patrón_lineacsv)
    
    vacío=False
    
    # Se pide al usuario que introduza un teléfono y una fecha, de manera similar a como se pide en la función "registrarentrada"
    teléfono = input("Teléfono: ")
    if teléfono=="":
        vacío=True
    iterador=True
    
    if not vacío:
        while iterador and not vacío:
            if er_teléfono==None:
                print("Formato incorrecto, vuelve a introducir el dato")
                teléfono = input("Teléfono: ")
            else:
                iterador=False

    if not vacío:
        fecha = input("Fecha: ")
        if fecha=="":
            vacío=True
        iterador=True
        while iterador and not vacío:
            if er_fecha==None:
                print("Formato incorrecto, vuelve a introducir el dato")
                fecha = input("Fecha: ")
            else:
                iterador=False
    
    if vacío:
        print()
        menú()
    print("--")
    
    # Abrimos el archivo log.csv en modo lectura
    archivo = open('log.csv', 'r', encoding="utf8")
    
    lineas=archivo.readlines()
    # Se inicializa una lista vacía donde se almacenarán los recintos donde ha estado el usuario
    
    encontrado=False
    # Primer bucle que recorre las lineas del archivo log.csv
    for linea in lineas:
        resullineacsv = er_lineacsv.match(linea)
        resullugar = er_lugar.match(linea)
        if resullineacsv and resullugar:
            resulfecha = resullineacsv.group(6)
            resulteléfono = resullineacsv.group(1)
            resulhora = resullineacsv.group(2)
            resulfacultad = resullugar.group(2)
            resuldirección = resullugar.group(1)
            if resulfecha and resulteléfono and resulhora:
                t1=time(int(resullineacsv.group(3)),int(resullineacsv.group(4)),int(resullineacsv.group(5)))
                # if para comprobar que las fechas y el teléfono del usuario introducido coinciden con el de log.csv
                if fecha==resulfecha and teléfono==resulteléfono:
                    archivo2 = open('edificios.csv', 'r', encoding="utf8")
                    nombrelugar=""
                    # bucle for para coger el nombre del edificio en el que coinciden ambas personas
                    for linea2 in archivo2:
                        resuledificio = er_edificio.match(linea2)
                        if resuledificio:
                            if resuledificio.group(2)==resulfacultad:
                                nombrelugar = resuledificio.group(3)
                    # print que indica el nombre del recinto y la direccón del mismo, con toda la información del edificio, bloque, planta y sala respectivamente
                    print(nombrelugar+" "+resuldirección.replace(";", "."))
                    archivo2.close()
                    # Se crea un array vacío "usuarios" donde se van a almacenar los móviles de los que han coincidido
                    usuarios = []
                    # Tercer bucle for para realizar la comprobación de los móviles que han coincidido con el que se introduce
                    for linea3 in lineas:
                        resullineacsv3 = er_lineacsv.match(linea3)
                        resullugar3 = er_lugar.match(linea3)
                        if resullineacsv3 and resullugar3:
                            resulfecha3 = resullineacsv3.group(6)
                            resulteléfono3 = resullineacsv3.group(1)
                            if resulfecha3 and resullugar3:
                                # if para comprobar si las fechas y lugares de ambas personas coinciden
                                if resulfecha==resulfecha3 and str(resullugar)==str(resullugar3):
                                    resulhora3 = resullineacsv3.group(2)
                                    if resulhora3:
                                        t2=datetime.datetime(100,1,1,int(resullineacsv3.group(3)),int(resullineacsv3.group(4)),int(resullineacsv3.group(5)))
                                        t3=t2+datetime.timedelta(minutes = 5)
                                        #if para comprobar que las personas han coincidido en un intervalo de 5 minutos superior
                                        if t2.time()>t1 and t2.time()<t3.time():
                                            norepetido=True
                                            for i in usuarios:
                                                if i == resulteléfono3:
                                                    norepetido=False
                                            # if para insertar aquellos usuarios no repetidos en los diferentes lugares donde coinciden
                                            if norepetido:
                                                usuarios.append(resulteléfono3)
                                                encontrado=True   
                    # bucle for para imprimir en pantalla el formato correcto de salida de los usuarios                   
                    for usuario in usuarios:
                        print("- ", usuario)
    
    # if para notificar que no se han encontrado registros de presencia
    if encontrado==False:
        print("No se han encontrado registros de presencia.")
if __name__ == '__main__':
    menú()
    
    
    
    