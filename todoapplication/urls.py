from django.urls import path
from todoapplication import views
urlpatterns=[
    path('signup',views.SignupView.as_view(),name='register'),
    path('',views.LoginView.as_view(),name='login'),
    path('home',views.IndexView.as_view(),name='home'),
    path('signout',views.LogoutView.as_view(),name='signout'),
    path('todo/add',views.TodoAddView.as_view(),name='todoadd'),
    path('todo/list',views.TodoListView.as_view(),name='todolist'),
    path('todo/remove/<int:id>',views.DeleteTodo.as_view(),name='removetodo'),
    path('todo/details/<int:id>',views.TodoDetailView.as_view(),name='tododetails'),
    path('todo/edit/<int:id>',views.TodoEditView.as_view(),name='todoedit')
]