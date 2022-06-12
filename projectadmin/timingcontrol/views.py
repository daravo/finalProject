from time import strftime
from xmlrpc.client import DateTime
from rest_framework.generics import ListAPIView
from .serializers import WorkerSerializer, ProjectSerializer
from sqlite3 import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required #decorador para funciones
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin #mixin que restringe en clases (vistas basadas en clases)
from .models import Project, Worker, Useres, Times
import datetime
from .forms import RenewBookForm, CreateWorkerModelForm #Importando formularios
import sqlite3

con = sqlite3.connect('project_db.sqlite3', check_same_thread=False)

def sentencias (con, sentencia, listaDatos):#Recibe una sentencia SQL y una lista con los datos

    cursorObj = con.cursor()
    cursorObj.execute(sentencia,listaDatos)
    con.commit()

@login_required
def index(request):
    num_projects = Project.objects.all().count()
    projects = Project.objects.all()
    workers = Worker.objects.all()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    return render(
        request,
        'index.html',
        context={'num_projects': num_projects, 'projects':projects, 'workers':workers, 'num_visits':num_visits}
        
    )
    
class WorkerListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = ('timingcontrol.can_edit', 'timingcontrol.can_mark_factured')
    #permission_required = 'timingcontrol.can_edit' #se le puede pasar un valor, si quieres más, se pone en tuplas
    model = Worker
    paginate_by = 10
    
class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker

    """
    Vista que me muestra el enlace al perfil exacto del trabajador logueado

    """
class WorkerByUserListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = 'timingcontrol/worker_private_user.html'
    
    def get_queryset(self):
        return Worker.objects.filter(usernameid = self.request.user)
    
class UseresListView(LoginRequiredMixin, generic.ListView):
    model = Useres
    template_name = 'timingcontrol/user_list.html'

class UseresDetailView(LoginRequiredMixin, generic.DetailView):
    model = Useres

    """
    Función que crea un usuario si le pasamos un objeto con los datos necesarios
    dataList = {'username':'username', 'mail':'mail@mail.com', 'password':'password','name':'name','surname':'surname'}
    devuelve el username
    """
@permission_required('timingcontrol.can_mark_factured')
@permission_required('timingcontrol.can_edit')
def createUser(request, rol): #El grupo se lo paso en la url
    username='paca'
    mail='mailpepito@mail.com'
    password='contraseña1'
    name = 'pedro'
    surname = 'pedrito'
    
    try:
        user = User.objects.create_user(username, mail, password)
        user.first_name = name
        user.last_name = surname
        #añadir usuario al grupo:
        group = Group.objects.get(name=rol)
        user.groups.add(group)
        user.save()
        respuesta = 'dado de alta con éxito: '
    except:
        
        #if ('UNIQUE constraint' in e):
        respuesta = 'El username '+username+' ya está en uso'
    
    #Hasta aquí estaría creado el usuario, ahora hay que crear un worker o admin usando la información del usuario nuevo creado:
    
    
    return render(
        request,
        'timingcontrol/new_user.html',
        context={'respuesta':respuesta}
    )

class WorkerCreate(CreateView):
    model = Worker
    fields = '__all__'
    
class WorkerUpdate(UpdateView):
    model = Worker
    fields = '__all__'
        
class WorkerDelete(DeleteView):
    model = Worker
    success_url = reverse_lazy('workers')#Cuando borra el usuario, vuelve a la lista de usuarios   

#------------USERS---------------------
class UseresCreate(CreateView):
    model = Useres
    #fields = '__all__'
    fields = ('id','username','dni','job', 'first_name','last_name','email','password','groups','is_active')
    template_name = 'timingcontrol/user_form.html'
    success_url = reverse_lazy('users')#Cuando borra el usuario, vuelve a la lista de usuarios   
   
class UseresUpdate(UpdateView):
    model = Useres
    fields = ('username', 'first_name','last_name','email','password','groups','is_active')
    template_name = 'timingcontrol/user_form.html'
class UseresDelete(DeleteView):
    model = Useres
    success_url = reverse_lazy('users')#Cuando borra el usuario, vuelve a la lista de usuarios   
   
#------------------PROJECTS-------------
class ProjectCreate(CreateView):
    model = Project
    fields = '__all__'
    
class ProjectUpdate(UpdateView):
    model = Project
    fields = '__all__'
    
class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('projects')
    
class ProjectListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = ('timingcontrol.can_edit', 'timingcontrol.can_mark_factured')
    #permission_required = 'timingcontrol.can_edit' #se le puede pasar un valor, si quieres más, se pone en tuplas
    model = Project
    paginate_by = 10
    
class ProjectDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    model = Project    
    permission_required = ('timingcontrol.can_edit', 'timingcontrol.can_mark_factured')
#-------------------------TIMES----------------
class TimestListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = ('timingcontrol.can_edit', )
    model = Times
    paginate_by = 10
    
class TimesUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('timingcontrol.can_edit', )
    model = Times
    fields = '__all__'
    
class TimesDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = ('timingcontrol.can_edit', )
    model = Times
  
class TimesCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required =  ('timingcontrol.can_edit', )
    model = Times
    fields = '__all__'

    
    """
    ejemplos
    """
#El detailView con función y personalizando el error 404
def worker_detail_view(request, pk):
    try:
        worker_id = Worker.objects.get(pk=pk)
    except Worker.DoesNotExist:
        raise Http404('Worker does not exist')
    
    book_id=get_object_or_404(Worker, pk=pk)
    
    return render(
        request,
        'timingcontrol/worker_detail.html',
        context={'worker':worker_id,}
    )

    """
    
    """

"""aquí empiezan los servicios
"""
class WorkerListApiView(ListAPIView):
    serializer_class = WorkerSerializer
    
    def get_queryset(self):
        kword = self.request.query_params.get('kword', '')
        return Worker.objects.filter(name__icontains = kword)
        
class ProjectListApiView(ListAPIView):
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        kword = self.request.query_params.get('kword', '')
        return Project.objects.filter(name__icontains = kword)
    
def newDate(request, pk, hour):
    print(request.__dict__)
    fecha = pk
    hora = hour
    print('fecha recogida en el back ', fecha, '\nhora recogida en el back ',hora)
    return index(request)

def checkOutForm(request):
    datos = []
    datosConsulta = []
    registroFecha = request.POST.get('registroFecha')
    registroHora = request.POST.get('registroHora')
    projectId = request.POST.get('projectId')
    userId = request.POST.get('userId')
    
    datosConsulta.append(projectId)
    datosConsulta.append(registroFecha)
    datosConsulta.append(userId)
    #Asegurarse primero que el checkin se ha hecho, para poder hacer checkout:
    sentenciaConsulta = 'SELECT * from timingcontrol_times where project_id_id = ? and date = ? and user_id_id = ?;'
    cur = con.cursor()
    cur.execute(sentenciaConsulta,datosConsulta)
    resultado = cur.fetchone()
    print(resultado)
    if resultado == None: #Si no existe registro con la misma fecha, proyecto y usuario, lanzo mensaje de error porque no se ha hecho checking
        return render(request, 'timingcontrol/error_checkout.html')
    elif resultado[3] == None: 
        worked_hours = 0  
        #Calcular horas de fin  
        horaFin = registroHora.split(':')
        worked_hours += int(horaFin[0])
        if int(horaFin[1])>30:
            worked_hours += 0.5
        #Calcular horas de inicio:
        horaInicio = resultado[2].split(':') #Esta es la hora de inicio
        worked_hours -= int(horaInicio[0])
        if int(horaInicio[1])>30:
            worked_hours -= 0.5

        #Modificar en base de datos la hora de salida:
        datos.append(registroHora)
        datos.append(projectId)
        datos.append(registroFecha)
        datos.append(userId)
        
        sentenciaModificar = "UPDATE timingcontrol_times SET timeExit = ? WHERE project_id_id = ? and date = ? and user_id_id = ?;"
        sentencias(con,sentenciaModificar,datos)
        
        #Modificar las horas trabajadas:
        datos = []
        datos.append(worked_hours)
        datos.append(projectId)
        datos.append(registroFecha)
        datos.append(userId)
        
        sentenciaModificar = "UPDATE timingcontrol_times SET worked_hours = ? WHERE project_id_id = ? and date = ? and user_id_id = ?;"
        sentencias(con,sentenciaModificar,datos)
     
        #Redirigir a esta altura a una pantalla de éxito
        return render(request, 'timingcontrol/success_checkout.html')
    else: #Si llega a este else, es porque ya se había hecho antes un checkout para este mismo día y proyecto.
        return render(request, 'timingcontrol/error_checkout.html', context={'checkoutDone':'Check-out already done before'})
    
def newDateForm(request):
    datos = []
    datosConsulta = []
    registroFecha = request.POST.get('registroFecha')
    datos.append(registroFecha)
    registroHora = request.POST.get('registroHora')
    datos.append(registroHora)
    projectId = request.POST.get('projectId')
    datos.append(projectId)
    userId = request.POST.get('userId')

    datos.append(userId)
    
    datosConsulta.append(projectId)
    datosConsulta.append(registroFecha)
    datosConsulta.append(userId)
    
    #consultar si existe ya el checkin para evitar checkin duplicados en el mismo día:
    sentenciaConsulta = 'SELECT * from timingcontrol_times where project_id_id = ? and date = ? and user_id_id = ?;'
    cur = con.cursor()
    cur.execute(sentenciaConsulta,datosConsulta)
    resultado = cur.fetchone()
    print(resultado)
    if resultado == None: #Si no existe registro con la misma fecha, proyecto y usuario, le doy de alta
        sentenciaAlta = 'INSERT INTO timingcontrol_times(date, timeEntry, project_id_id, user_id_id) VALUES(?, ?, ?, ?);'
        sentencias(con,sentenciaAlta,datos)
        #Redirigir a esta altura a una pantalla de éxito
        return render(request, 'timingcontrol/success_checkin.html')
    else:
        #Redirigir a pantalla advirtiendo que ya se ha hecho el checkin para este día en este proyecto
        return render(request, 'timingcontrol/error_checkin.html')
    

# CONSULTAR HORAS HECHAS POR MES DE UN TRABAJADOR EN CONCRETO
# select sum(timeExit) from timingcontrol_times 
# where (date BETWEEN '2022-06-01' AND '2022-06-31') and user_id_id = 1
