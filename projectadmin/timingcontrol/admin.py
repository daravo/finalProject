from django.contrib import admin
from .models import Worker, Project, Useres


# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address', 'lat_long', 'factured')
    list_filter = ('factured', 'city')
    fieldsets = (
    (None, {
        'fields': ('name', ('address', 'city'), 'lat_long')
    }),
    ('Coordinate range', {
        'fields': (('latitude_min', 'longitude_min'),('latitude_max','longitude_max'))
    }),
    )
    
@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'job','username','email','usernameid')
    list_filter = ('job',)

@admin.register(Useres)
class UserAdmin(admin.ModelAdmin):
    pass
