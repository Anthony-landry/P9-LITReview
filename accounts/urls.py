"""
URL configuration for Litreview_V2_21092023 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from accounts.views import SignUp, Login, Logout, follow_view, unfollow_view, ReviewList, delete_post, update_post, \
    TicketUpdate, delete_ticket

app_name = "accounts"

urlpatterns = [

    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('follow/', follow_view, name='follow'),
    path('unfollow/<int:id>', unfollow_view, name='unfollow'),

    path('posts/', ReviewList.as_view(), name='posts'),
    path('delete-post/<int:id>', delete_post, name='delete-post'),
    path('delete-ticket/<int:pk>', delete_ticket, name='delete-ticket'),
    path('modify-post/<int:pk>', update_post, name='modify-post'),
    path('modify-ticket/<int:pk>', TicketUpdate.as_view(), name='modify-ticket'),

]
