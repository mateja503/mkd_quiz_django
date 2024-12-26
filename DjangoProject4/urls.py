from django.contrib import admin
from django.urls import path
from quiz import views
from django.urls import path, include

from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from DjangoProject4.views import signup  # Replace 'DjangoProject4' with your project name
from DjangoProject4.views import home  # Replace 'DjangoProject4' with your project name
from DjangoProject4.views import about  # Replace 'DjangoProject4' with your project name


urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include('quiz.urls', namespace='quiz')),  # Add namespace here

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),  # Handles login, logout, etc.
    path('posts/', include('posts.urls')),
    path('signup/', signup, name='signup'),  # Add signup route
    path('', home, name='home'),  # Add home page route
    path('about/', about, name='about'),  # About page

              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




