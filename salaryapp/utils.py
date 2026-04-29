from .models import Attendance

def calculate_salary(employee, month, year):
    salary_structure = employee.salarystructure

    gross_salary = (
        salary_structure.basic_salary +
        salary_structure.hra +
        salary_structure.allowance
    )

    total_working_days = 26

    present_days = Attendance.objects.filter(
        employee=employee,
        date__month=month,
        date__year=year,
        status='Present'
    ).count()

    absent_days = total_working_days - present_days

    per_day_salary = gross_salary / total_working_days

    attendance_deduction = absent_days * per_day_salary

    total_deduction = (
        attendance_deduction +
        salary_structure.tax +
        salary_structure.pf
    )

    net_salary = gross_salary - total_deduction

    return {
        'gross_salary': gross_salary,
        'total_deduction': total_deduction,
        'net_salary': net_salary,
        'present_days': present_days,
        'total_working_days': total_working_days
    }