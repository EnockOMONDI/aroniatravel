
from django.contrib import admin
from django.urls import path,include
from . import views as tours_travels_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static







urlpatterns = [

    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path("ckeditor5/", include('django_ckeditor_5.urls')),  # CKEditor 5 URLs
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='/admin/'), name='admin_logout'),
    path('admin/', admin.site.urls),
    path('', include(('aronia.urls', 'aronia'), namespace='aronia')),
    path('events/', include(('events.urls', 'events'), namespace='events')),
    path('users/', include(('users.urls', 'users'), namespace='home')),
    path('tours/', include(('adminside.urls', 'adminside'), namespace='adminside')),
    path('login/',auth_views.LoginView.as_view(template_name='users/aronia/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/aronia/index.html'),name='logout'),
    path('mail/',tours_travels_views.mail,name='mail'),
  
    

]


if settings.DEBUG == True:
    # static function below returns a list of url patterns of static path
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)  




    
