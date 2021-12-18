from bitarray import bitarray
from numpy.random import MT19937,Generator

#Codigo validor: tecnica FEC funciono o no
#los codigos crc no corrigen errores, solo los detectan
#r(bits de redundancia):  vale 4,que es el numero de bits redundantes que le estamos agregando al mansaje
#n : es el tamaño de la rafaga

#lo que haremos primero es convertir una cadena de texto a binario
def cyclic_redundancy_check(filename: str, divisor: str, len_crc: int) -> int:
    """
    This function computes the CRC of a plain-text file 
    arguments:
    filename: the file containing the plain-text
    divisor: the generator polynomium
    len_crc: The number of redundant bits (r)
    """
    redundancy = len_crc * bitarray('0')
    bin_file = bitarray()
    p = bitarray(divisor)
    #len_p : longitud del divisor
    len_p = len(p)
    with open(filename, 'rb') as file:
        bin_file.fromfile(file) #ARREGLO DE BITS
    #cw(ARREGLO DE BITS): code work,mensaje que vamos a codificar
    cw = bin_file + redundancy
    #rem: residuo de la division binaria, tiene que aplicar tantos bits como el del divisor
    #porque se aplica el XOR,por ejemplo si tenemos un divisor de 5 bits el residuo tomara tantos bits  
    rem = cw[0 : len_p]
    #el residuo se inicializa
    end = len(cw)
    #calculo de cuantas veces se itera sobre el mensaje
    #esto de tal manera que obtengamos el residuo y despues obtener codigo de redundancia ciclica 
    for i in range(len_p, end + 1):
        if rem[0]:
            rem ^= p   #p: contenido binario del divisor 
        #funcionamiento del desplazamiento
        if i < end:
            #Error
            rem = rem << 1  #el contenido del residuo se desplaza hacia la izquieda, para hacer bien la division de XOR
            rem[-1] = cw[i] #ayuda al afecto del desplazamiento
        #termina funcionamiento del desplazamiento    
    crc = rem[len_p-len_crc : len_p]
    
    #el codificador debe de enviar el mensaje  + CRC  
    return (bin_file,crc)


#los errores pueden pasar inclusive en CRC
def generador(cadena:str,tam:int,semilla:int) -> str :
    pos_invertir = []
    # #b = Generator(MT19937(semilla))
    # #posiciones del 1 al penusltimo se van a modificar
    # #contiene la semilla generada
    a = Generator(MT19937(semilla + 3000))
    # #seleccionar bits que se van a invertir 
    
    # #voltear los bits
    # #hacer que e bits se inviertan aleatoriamente
    # if(e<=tam):
    #     for i in range(0,e):
    #         posicion = int(a.integers(1,tam-1))
    #         if posicion is not pos_invertir:
    #     
    #        posicion = pos_invertir.append(posicion)
    
    e = int(a.integers(3,tam-1))
    for i in range(0,e):
            posicion = int(a.integers(1,tam-1))
            cadena[posicion] = not cadena[posicion]
    
    print("despues",cadena)   
    
    return cadena


#entra el mensaje completo aunque la redundancia se haya corrompido
#el decodificador recibe datos de redundancia, es decir el cw

def Decodificador(archivoBin : str,len_crc:int,divisor:str ):
    p = bitarray(divisor)
    len_p = len(p)
    cw = archivoBin
    rem = cw[0:len_p]
    end = len(cw)
    for i in range(len_p,end + 1):
        if rem[0]:
            rem ^= p   #p: contenido binario del divisor 
        #funcionamiento del desplazamiento
        if i < end:
            #Error
            rem = rem << 1  #el contenido del residuo se desplaza hacia la izquieda, para hacer bien la division de XOR
            rem[-1] = cw[i] #ayuda al afecto del desplazamiento
        #termina funcionamiento del desplazamiento    
    return rem[len_p-len_crc : len_p]
#divisor mas uno.


def validador(residuo : str):
#si el mensaje que me regresa puros ceros o puros unos entonces el mensaje es correcto
#se incrementaria exitos

#en base al numero de errores detectados sacamos la probabilidad entre mil
    if(residuo == '0000'):
        return True
    else:
        return False
  


def main():
   errores = 0
   exitos = 0 
   divisor = '10111'
   for i in range(0,99):
        arch, c = cyclic_redundancy_check('test.txt', divisor, 4)
        #concatenamos el archivo binario con el CRC
        binario = arch + c
        print(c)
        print(arch)
        tam = len(binario)
        result = generador(binario,tam,10)
        print(result)
        residuo = Decodificador(result,4,divisor)

        if(validador(residuo)):
            exitos +=1
        else:
            errores +=1
   
   print(f"probabilidad de exito : {exitos/100} \nProbabilidad de error: {errores/100}")
   print("Errores: ",errores
   print("Exitos: ",exitos)
    #sacar la probabilidad



if __name__ == '__main__':
    main()
   

    
