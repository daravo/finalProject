from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Project(models.Model): #parecido a Genre
    """
    Modelo que representa el proyecto (obra),
    por ejemplo 'Bodegas de la nave industrial 14'
    Contiene rangos mínimos y máximos de latitud y longitud
    """
    name = models.CharField(max_length=200, help_text='Set here the name of the project')
    address = models.CharField(max_length=200,help_text='Set here the address of the project', blank=True, null=True)
    city = models.CharField(max_length=200, help_text='Set here the name of the project', blank=True, null=True)
    lat_long = models.CharField(max_length=200,help_text='Set here latitude and longitude of the project', blank=True, null=True)
    factured = models.BooleanField(default=False)
    
    
    class Meta:
        #los permisos están en la variable "{{perms.timingcontrol.nombrePermiso}} para usar en templates"
        permissions = (('can_mark_factured', 'can_mark_factured'),('can_edit', 'can_edit'),)
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])
class Worker(models.Model):
    """
    Modelo que representa un trabajador, cada uno será un usuario
    """    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='unique ID by user/worker')
    name = models.CharField(max_length=200, help_text='worker name')
    surname = models.CharField(max_length=200, help_text='worker surname')
    dni = models.CharField(max_length=10)
    email = models.EmailField()
    username = models.CharField(max_length=10)
    JOBS = (
        ('Tapper', 'Tapper'),
        ('Painter', 'Painter'),
        ('Steel-framer', 'Steel-framer'),
        ('Administrator', 'Administrator'),
    )
    job = models.CharField(max_length=20, choices=JOBS, blank=True, default='bui', help_text='Job of worker')
    usernameid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        ordering = ["surname"]
        
    def __str__(self):
        return '%s %s' % (self.name, self.surname)
        
    def get_absolute_url(self):
        return reverse('worker-detail', args=[str(self.id)])

    @property #Propiedad para poder usarla en plantillas
    def is_overdue(self):
        if (self.usernameid!=' '):
            return True
        return False
    
#Modificando la clase User:
class Useres(User):
    worker_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='unique ID by user/worker')
    JOBS = (
        ('Tapper', 'Tapper'),
        ('Painter', 'Painter'),
        ('Steel-framer', 'Steel-framer'),
        ('Administrator', 'Administrator'),
    )
    job = models.CharField(max_length=20, choices=JOBS, blank=True, default='bui', help_text='Job of worker')
    dni = models.CharField(max_length=10)
    
    #Mostrar ordenación por apellido
    class Meta:
        ordering = ["last_name"]
        
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
        
    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.worker_id)])
    
#tabla usuario-checkins
class Times(models.Model):
    """
    Modelo que guarda las entradas del usuario
    """
    user_id = models.ForeignKey(Useres, on_delete=models.SET_NULL, null=True, blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    timeEntry = models.TimeField(null=True, blank=True)
    timeExit = models.TimeField(null=True, blank=True)
    worked_hours = models.FloatField(null=True, blank=True, default=0)
    
    class Meta:
        ordering = ['date']
        
    def __str__(self):
        return '%s %s %s' % (self.user_id, self.project_id, self.date)
    
    def get_absolute_url(self):
        return reverse("times_detail", args=[str(self.id)])
    
        
    
    
    #-----------    
""" 
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Book(models.Model):
"""
    #Modelo que representa un libro (pero no un Ejemplar específico).
"""

title = models.CharField(max_length=200)
author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
# ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
# 'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.
summary = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")
isbn = models.CharField('ISBN',max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
genre = models.ManyToManyField(Genre, help_text="Seleccione un genero para este libro")
# ManyToManyField, porque un género puede contener muchos libros y un libro puede cubrir varios géneros.
# La clase Genre ya ha sido definida, entonces podemos especificar el objeto arriba.
def __str__(self):
"""
#        String que representa al objeto Book
"""
    return self.title
    def get_absolute_url(self):
"""
    #    Devuelve el URL a una instancia particular de Book
"""
    return reverse('book-detail', args=[str(self.id)])

"""
    