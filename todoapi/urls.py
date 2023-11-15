from django.urls import path
from todoapi import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('todos',views.TodosView,basename='todos')
urlpatterns=[
]+router.urls