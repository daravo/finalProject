from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    
    url(r'^...$', views.index, name='index'),
    path('workers/', views.WorkerListView.as_view(), name='workers'),
    path('worker-detail/<uuid:pk>', views.WorkerDetailView.as_view(), name='worker-detail'),
    url(r'^myprofile/$', views.WorkerByUserListView.as_view(), name='my-profile'),
    #path('createUser/<rol>', views.createUser, name='createUser')
]
urlpatterns += [
    url(r'^worker/create/$', views.WorkerCreate.as_view(), name='worker_create'),
    path('worker/<uuid:pk>/update/', views.WorkerUpdate.as_view(), name='worker_update'),
    path('worker/<uuid:pk>/delete/', views.WorkerDelete.as_view(), name='worker_delete'),
]
#Projects:
urlpatterns += [
    url(r'^project/create/$', views.ProjectCreate.as_view(), name='project_create'),
    url(r'^project/(?P<pk>\d+)/update/$', views.ProjectUpdate.as_view(), name='project_update'),
    url(r'^project/(?P<pk>\d+)/delete/$', views.ProjectDelete.as_view(), name='project_delete'),
    url(r'^projects/$', views.ProjectListView.as_view(), name='projects'),
    path('project-detail/<int:pk>', views.ProjectDetailView.as_view(), name='project-detail'),
]
#Users:
urlpatterns += [    
    path('users/', views.UseresListView.as_view(), name='users'),
    path('user/create/', views.UseresCreate.as_view(), name='create_user'),
    path('user/<uuid:pk>/update/', views.UseresUpdate.as_view(), name='user_update'),
    path('user_detail/<uuid:pk>', views.UseresDetailView.as_view(), name='user_detail'),
    path('user/<uuid:pk>/delete/', views.UseresDelete.as_view(), name='user_delete'),
    
]

#urls de los servicios:
urlpatterns += [
    path('workers/api/', views.WorkerListApiView.as_view(), name= 'api-workers'),
    path('api/projects/', views.ProjectListApiView.as_view(), name= 'api-projects'),
]
