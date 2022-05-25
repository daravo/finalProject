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

#@login_required
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
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
    
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
    
    