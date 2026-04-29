from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USERS = [
        ('Admin', 'Admin'),
        ('HR', 'HR'),
    ]
    user_type = models.CharField(choices=USERS, max_length=100, null=True)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class SalaryStructure(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    allowance = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    pf = models.DecimalField(max_digits=10, decimal_places=2)


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[('Present', 'Present'), ('Absent', 'Absent')]
    )


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    is_approved = models.BooleanField(default=False)


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    total_working_days = models.IntegerField()
    present_days = models.IntegerField()
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    generated_on = models.DateTimeField(auto_now_add=True)


class Payslip(models.Model):
    salary = models.OneToOneField(Salary, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='payslips/')