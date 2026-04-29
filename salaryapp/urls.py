from django.urls import path
from . import views

urlpatterns = [

    # ================= EMPLOYEE =================
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_employee, name='add_employee'),

    # Salary structure for a specific employee
    path(
        'employees/<int:employee_id>/salary-structure/',
        views.add_salary_structure,
        name='add_salary_structure'
    ),

    # ================= ATTENDANCE =================
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/list/', views.attendance_list, name='attendance_list'),

    # ================= LEAVE =================
    path('leave/apply/', views.apply_leave, name='apply_leave'),
    path('leave/list/', views.leave_list, name='leave_list'),

    path(
        'leave/approve/<int:leave_id>/',
        views.approve_leave,
        name='approve_leave'
    ),

    # ================= SALARY =================
    path('salary/generate/', views.generate_salary, name='generate_salary'),
    path('salary/list/', views.salary_list, name='salary_list'),

    path(
        'salary/detail/<int:salary_id>/',
        views.salary_detail,
        name='salary_detail'
    ),

    # ================= PAYSLIP =================
    path(
        'salary/<int:salary_id>/payslip/upload/',
        views.upload_payslip,
        name='upload_payslip'
    ),

    path(
        'salary/<int:salary_id>/payslip/view/',
        views.view_payslip,
        name='view_payslip'
    ),
]