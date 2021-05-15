#Ejercicio 4
saldo=2000
print("1. Ingreso de dinero")
print("2. Retiro de dinero")
print("3. Mostrar dinero")
print("4. Salir")

seleccion =int(input("Elija una opcion: "))

if seleccion==1:
    ingreso = float(input("Dinero a ingresar: "))
    saldo+=ingreso
    print(f"Nuevo saldo en la cuenta: {saldo}")
elif seleccion==2:
    salida=float(input("Dinero de salida: "))
    if salida>saldo:
        print("Saldo insuficiente")
    else:
        saldo-=salida
        print(f"Nuevo saldo disponible {saldo}")
elif seleccion==3:
    print(f"Saldo disponible {saldo}")
elif seleccion==4:
    print("Salida")
else:
    print("Seleccione una opcion correcta")