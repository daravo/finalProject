from requests import request
# Creación de un nuevo registro usando el constructor del modelo.
a_record = MyModelName(my_field_name="Instancia #1")

# Guardar el objeto en la base de datos.
a_record.save()

#-------------------
# Accesso a los valores de los campos del modelo usando atributos Python.
print(a_record.id) # Debería devolver 1 para el primer registro.
print(a_record.my_field_name) # Debería imprimir 'Instancia #1'

# Cambio de un registro modificando los campos llamando a save() a continuación.
a_record.my_field_name="Nuevo Nombre de Instancia"
a_record.save()


#------SESIONES-----
# Obtener un dato de la sesión por su clave (ej. 'my_car'), generando un KeyError si la clave no existe
my_car = request.session['my_car']

# Obtener un dato de la sesión, estableciendo un valor por defecto ('mini') si el dato requerido no existe
my_car = request.session.get('my_car', 'mini')

# Asignar un dato a la sesión
request.session['my_car'] = 'mini'

# Eliminar un dato de la sesión
del request.session['my_car']
#--------------------------
# Objeto de sesión no directamente modificada, solo información dentro de la sesión.
# ¡Cambios no guardados!
request.session['my_car']['wheels'] = 'alloy'

# Establecer la sesión como modificada para forzar a que se guarden los cambios.
request.session.modified = True
