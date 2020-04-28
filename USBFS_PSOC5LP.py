# -*- coding: utf-8 -*-


#!/usr/bin/env python3

import time
import usb.core
import usb.util
import numpy as np
import sys
import matplotlib.pyplot as plt


def close_device(exitVal=0):
    print("Exiting...")
    usb.util.dispose_resources
    sys.exit(exitVal)

###########Configuración USBFS (lado de Python)###########
VID = 0x04B4
PID = 0xF232

dev = usb.core.find(idVendor = VID, idProduct = PID)

if not dev:
    print('PSoC no encontrada')
    close_device(1)

print('PSoC encontrada')
#establecer la configuración activa (básicamente, iniciar el dispositivo)
dev.set_configuration()

#Establece la interface 0, alternate setting 0
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]

#print(intf)

epOut = usb.util.find_descriptor(
    intf,
    # coincidir con el primer Endpoint OUT
    custom_match= \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

#Asegúrate de que nuestra EP se encuentre
if epOut is None:
    close_device(1)

# encuentre el primer (y solo en este caso) EP_IN en nuestra interfaz
epIn = usb.util.find_descriptor(
    intf,
    custom_match= \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_IN)

#Asegúrate de que nuestra EP se encuentre
if epIn is None:
   close_device(1)

###########Configuración USBFS (lado de Python)###########



# si usamos transferencias a BULK estamos atascados en 64 bytes
bytes_to_read = 64

#variables 
datos = []
datos_int = []
j = 0;
#while j <10:
for i in range(10):
    time.sleep(0.01)

    data = epIn.read(bytes_to_read)

    # imprimir datos en decimal
    # obtenemos los datos en formato u8 para transformarlos en u16
    # necesitamos mover las 8 posiciones de high_byte a la izquierda
    # and OR con el lower_byte
    # Repítalo dependiendo del número de bytes a leer
    for i in range(0, bytes_to_read, 2):
         #print(' {0:d}'.format(data[i+1] << 8 | data[i]))
        datos.append(' {0:d}'.format(data[i+1] << 8 | data[i]))
        

for i in range(len(datos)):
    datos_int.append(int(datos[i]))
plt.plot(datos_int, label='linear')        
plt.legend()
plt.show()
#j = j +1
close_device()