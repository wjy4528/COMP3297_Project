"""imageXback URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/view/<int:memberID>', views.profile_view, name='profile_view'),
    path('image/member/<int:memberID>', views.member_image, name='member_image'),
    path('image/self', views.my_image, name='my_image'),
    path('image/all/', views.all_image, name='all_image'),
    path('image/search', views.search_image, name='search_image'),
    path('image/upload/page/', views.upload_image_page, name='upload_image_page'),
    path('image/upload/new/', views.upload_image_data, name='upload_image_data'),
    path('image/delete/page/', views.delete_image_page, name='delete_image_page'),
    path('image/delete/data/<int:imgID>', views.delete_image_data, name='delete_image_data'),
    path('image/download/data/<int:imgID>', views.download_image_data, name='download_image_data'),
    path('password/forget/email', views.password_forget_email, name='password_forget_email'),
    path('password/forget/req', views.password_forget_req, name='password_forget_req'),
    path('password/forget/page/<str:token>', views.password_forget_page, name='password_forget'),
    path('password/forget/reset/', views.password_forget_reset, name='password_forget'),
    path('password/change/page/', views.password_change_page, name='password_change'),
    path('password/change/set/', views.password_change_set, name='password_change'),
    path('signindata', views.signindata, name='signindata'),
    path('signupdata', views.signupdata, name='signupdata'),
    path('token/generate/new', views.token_generate_new, name='token_generate_new'),
    path('token/generate/page', views.token_generate_page, name='token_generate_page'),
    path('api/updatelike/<int:imgID>', views.update_likes, name='update_likes'),
    path('api/update_download/<int:imgID>', views.update_download, name='update_download'),
    # path('api/delete/<int:imgID>', views.delete_image, name='delete_image'),
    path('edit_profile/update/',views.update_profile, name='update_profile'),
]