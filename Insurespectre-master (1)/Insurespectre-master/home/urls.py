from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('about/who/', views.who, name='who'),
    path('about/what/', views.what, name='what'),
    path('about/goal/', views.goal, name='goal'),
    path('about', views.about, name='about'),
    path('solution', views.solution, name='solution'),
]

