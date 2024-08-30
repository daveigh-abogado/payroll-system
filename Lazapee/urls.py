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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('payroll_app.urls'))
]
