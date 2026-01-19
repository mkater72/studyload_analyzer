from django.urls import path
from .views import (
    dashboard,
    subject_list,
    delete_subject,
    delete_grade
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('subjects/', subject_list, name='subject_list'),
    path('subjects/delete/<int:subject_id>/', delete_subject, name='delete_subject'),
    path('grades/delete/<int:grade_id>/', delete_grade, name='delete_grade'),
]
