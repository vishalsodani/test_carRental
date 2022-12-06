from django.urls import path, include
from . import views
urlpatterns = [
    path('list_users/', views.list_users, name='list_users'),
    path('blockuser/', views.blockUser, name='blockuser'),
    path('deleteemployee/', views.deleteEmployee, name='deleteemployee'),
    path('editemployee/', views.editEmployee, name='editemployee'),
    path('manager/', views.manager, name='manager'),
    path('employee/', views.employee, name='employee'),
    path('customer/', views.customer, name='customer'),
]