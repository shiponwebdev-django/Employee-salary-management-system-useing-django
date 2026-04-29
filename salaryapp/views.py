from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Employee, Attendance, Salary
from .utils import calculate_salary

User = get_user_model()



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import (
    Employee,
    SalaryStructure,
    Attendance,
    Leave,
    Salary,
    Payslip
)

from .utils import calculate_salary

User = get_user_model()






def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {
        'employees': employees
    })


def add_employee(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
            user_type='HR'
        )

        Employee.objects.create(
            user=user,
            employee_id=request.POST['employee_id'],
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            department=request.POST['department'],
            designation=request.POST['designation'],
            joining_date=request.POST['joining_date']
        )
        return redirect('employee_list')

    return render(request, 'employee_form.html')


def add_salary_structure(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        SalaryStructure.objects.update_or_create(
            employee=employee,
            defaults={
                'basic_salary': request.POST['basic_salary'],
                'hra': request.POST['hra'],
                'allowance': request.POST['allowance'],
                'tax': request.POST['tax'],
                'pf': request.POST['pf'],
            }
        )
        return redirect('employee_list')

    return render(request, 'salary_structure_form.html', {
        'employee': employee
    })





def mark_attendance(request):
    employees = Employee.objects.all()

    if request.method == 'POST':
        employee = Employee.objects.get(id=request.POST['employee'])

        Attendance.objects.create(
            employee=employee,
            date=request.POST['date'],
            status=request.POST['status']
        )
        return redirect('mark_attendance')

    return render(request, 'attendance_mark.html', {
        'employees': employees
    })


def attendance_list(request):
    attendance = Attendance.objects.select_related('employee')
    return render(request, 'attendance_list.html', {
        'attendance': attendance
    })



def apply_leave(request):
    if request.method == 'POST':
        Leave.objects.create(
            employee=request.user.employee,
            from_date=request.POST['from_date'],
            to_date=request.POST['to_date'],
            reason=request.POST['reason']
        )
        return redirect('leave_list')

    return render(request, 'leave_form.html')



def leave_list(request):
    leaves = Leave.objects.select_related('employee')
    return render(request, 'leave_list.html', {
        'leaves': leaves
    })



def approve_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    leave.is_approved = True
    leave.save()
    return redirect('leave_list')




def generate_salary(request):
    employees = Employee.objects.all()

    if request.method == 'POST':
        employee = Employee.objects.get(id=request.POST['employee'])
        month = request.POST['month']
        year = int(request.POST['year'])

        result = calculate_salary(employee, month, year)

        salary = Salary.objects.create(
            employee=employee,
            month=month,
            year=year,
            total_working_days=result['total_working_days'],
            present_days=result['present_days'],
            gross_salary=result['gross_salary'],
            total_deduction=result['total_deduction'],
            net_salary=result['net_salary']
        )

        return redirect('salary_detail', salary.id)

    return render(request, 'salary_generate.html', {
        'employees': employees
    })



def salary_detail(request, salary_id):
    salary = get_object_or_404(Salary, id=salary_id)
    return render(request, 'salary_detail.html', {
        'salary': salary
    })



def salary_list(request):
    salaries = Salary.objects.select_related('employee')
    return render(request, 'salary_list.html', {
        'salaries': salaries
    })



def upload_payslip(request, salary_id):
    salary = get_object_or_404(Salary, id=salary_id)

    if request.method == 'POST':
        Payslip.objects.create(
            salary=salary,
            pdf=request.FILES['pdf']
        )
        return redirect('salary_detail', salary.id)

    return render(request, 'payslip_upload.html', {
        'salary': salary
    })




def view_payslip(request, salary_id):
    payslip = get_object_or_404(Payslip, salary_id=salary_id)
    return render(request, 'payslip_view.html', {
        'payslip': payslip
    })