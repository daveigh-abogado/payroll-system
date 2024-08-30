'''
We have not discussed the Python language code in our program with anyone other than our instructor
or the teaching assistants assigned to this course.
We have not used Python language code obtained from another student, or any other unauthorized
source, either modified or unmodified.
If any Python language code or documentation used in our program was obtained from another source,
such as a textbook or course notes, that has been clearly noted with a proper citation in the
comments of our program.
'''
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.view_employees, name= 'view_employees'),    
    path('create_employee/',views.add_employee, name= 'add_employee'), 
    path('delete_employee/<str:pk>/',views.delete_employee, name= 'delete_employee'),    
    path('update_employee/<str:pk>/',views.update_employee, name= 'update_employee'), 
    path('add_overtime/<str:pk>/',views.add_overtime, name= 'add_overtime'), 
    path('view_payslips/<str:pk>/', views.view_payslips, name='view_payslips'),
    path('create_payslip', views.create_payslip,name="create_payslip"),
    path('delete_payslip/<str:pk>/',views.delete_payslip, name="delete_payslip"),
    path('deleteall',views.deleteall,name="deleteall"),
]
