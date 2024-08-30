'''
We have not discussed the Python language code in our program with anyone other than our instructor
or the teaching assistants assigned to this course.
We have not used Python language code obtained from another student, or any other unauthorized
source, either modified or unmodified.
If any Python language code or documentation used in our program was obtained from another source,
such as a textbook or course notes, that has been clearly noted with a proper citation in the
comments of our program.
'''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Employee, Payslip 


def view_employees(request):
    employee_objects = Employee.objects.all()
    return render(request, 'payroll_app/employees.html', {'employees':employee_objects})


def add_employee(request):
    if(request.method=="POST"):
        id_number = request.POST.get('id_number')
        if len(Employee.objects.filter(id_number=id_number)) > 0:
            messages.error(request, "That ID Number is already in use.")
            return redirect('add_employee')
        else:
            name = request.POST.get('name')
            rate = request.POST.get('rate')
            overtime_pay = 0
            if(request.POST.get('allowance')!=''):
                allowance = request.POST.get('allowance')
            else:
                allowance = 0
            Employee.objects.create(name=name,id_number=id_number,rate=rate,allowance=allowance,overtime_pay=overtime_pay)
            messages.success(request, "Employee has been added to the system.")
            return redirect ('view_employees')
    else:
        employee_objects = Employee.objects.all()
        return render(request, 'payroll_app/add_employee.html', {'employees':employee_objects})

def delete_employee(request, pk):
    employee_objects = Employee.objects.all()
    item = Employee.objects.get(pk=pk)

    if(request.method == 'POST'):
        item.delete()
        messages.info(request, "Employee has been deleted from the system.")
        return redirect('view_employees')
    
    else:
        return render(request, 'payroll_app/delete_employee.html', {'employees':employee_objects,'pk':pk})

def add_overtime(request, pk):
    employee_objects = Employee.objects.all()

    if(request.method == 'POST'):
        hours = request.POST.get('hours')
        rate = Employee.objects.get(pk=pk).rate
        xovertime = Employee.objects.get(pk=pk).overtime_pay


        xxovertime = float((rate/160)*1.5*float(hours))
        overtime_pay = xovertime+xxovertime
        Employee.objects.filter(pk=pk).update(overtime_pay=overtime_pay)
        messages.success(request, "Overtime has been added.")
        return redirect('view_employees')
    
    else:
        return render(request, 'payroll_app/employees.html', {'employees':employee_objects})

def update_employee(request, pk):
    temp = Employee.objects.get(pk=pk)
    if(request.method=="POST"):
        id_number = request.POST.get('id_number')
        if id_number != temp.id_number and len(Employee.objects.filter(id_number=id_number)) > 0:
            messages.error(request, "That ID number is already in use.")
            return redirect('update_employee', pk=pk)
        name = request.POST.get('name')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')
        
        Employee.objects.filter(pk=pk).update(name=name,id_number=id_number,rate=rate,allowance=allowance)
        messages.success(request, "Employee details were successfully updated.")
        return redirect ('view_employees')
    else:
        item = Employee.objects.get(pk=pk)
        employee_objects = Employee.objects.all()
        return render(request, 'payroll_app/update_employee.html', {'employees':employee_objects, 'pk':pk, "item":item})

def view_payslips(request, pk):
    p= get_object_or_404(Payslip, pk=pk)
    cycle_rate = p.getCycleRate()
    grosspay= p.getCycleRate()+ p.getEarnings_allowance()+ p.getOvertime()
    if p.pay_cycle == 1:
        deduct= p.getDeductions_tax() + p.getPag_ibig()
        return render(request, 'payroll_app/view_payslips1.html', {'p':p, 'gross': grosspay, 'deduct':deduct, 'cyclerate':cycle_rate})
    elif p.pay_cycle ==2:
        deduct= p.getDeductions_tax() + p.getDeductions_health() + p.getSSS()
        return render(request, 'payroll_app/view_payslips2.html', {'p':p, 'gross': grosspay, 'deduct':deduct, 'cyclerate':cycle_rate})

def create_payslip(request):
    payslip_objects = Payslip.objects.all()
    employee_objects = Employee.objects.all()
    if(request.method=="POST"):
        payrollfor = request.POST.get('payrollfor')  
        month = request.POST.get('month')
        pc = request.POST.get('cycle')
        if (payrollfor=='Choose...' or month=='Choose...'):
           messages.error(request, "Please complete the form")
           return redirect('create_payslip')
        try:
            pay_cycle = int(pc)
        except:
            messages.error(request, "Please complete the form")
            return redirect('create_payslip')
        try:
            year = int(request.POST.get('year'))
        except:
            messages.error(request,"Please enter a valid year.")
            return redirect('create_payslip')
        if(year<2000 or year>2024):
            messages.error(request,"Please enter a year from 2000 to 2024.")
            return redirect('create_payslip')
        
        if payrollfor=='All':
            ids = list(Employee.objects.all())
            for x in employee_objects:
                if(Payslip.objects.filter(id_number=x, month=month, year=year, pay_cycle=pay_cycle).exists()):
                    ids.remove(x)
            if len(ids) == 0:
                messages.error(request,"All payslips for this period have already been generated.")
                return redirect('create_payslip')                 
        else:
            ids = []
            e = get_object_or_404(Employee,id_number=payrollfor)
            if(Payslip.objects.filter(id_number=e, month=month, year=year, pay_cycle=pay_cycle).exists()):
                messages.error(request,"Payslip for this employee at this period already exists.")
                return redirect('create_payslip')
            else:
                ids.append(Employee.objects.get(id_number=payrollfor))
        for x in ids:
            pag_ibig = 0
            sss = 0
            deductions_health = 0
            deductions_tax = 0
            total_pay = 0

            id_number=x.getID()
            overtime=x.getOvertime()
            earnings_allowance = x.getAllowance()
            rate = x.getRate()
            e = get_object_or_404(Employee,id_number=id_number)

            if pay_cycle==1:
                date_range = '1-15' 
                pag_ibig= 100
                deductions_tax = ((float(rate)/2)+ earnings_allowance + overtime - pag_ibig)*0.2
                total_pay= ((float(rate)/2)+ earnings_allowance + overtime - pag_ibig)- deductions_tax
            elif pay_cycle==2:
                m31=['January', 'March', 'May', 'July', 'August', 'October', 'December']
                m30 =['April', 'June','September', 'November']
                if month in m31:
                    date_range= '16-31'
                if month in m30:
                    date_range= '16-30'
                if month=='February':
                    if (year%4)==0:
                        date_range= '16-29'
                    else:
                        date_range='16-28'
                deductions_health = float(rate)*0.04
                sss = float(rate)*0.045
                deductions_tax= ((float(rate)/2)+ earnings_allowance + overtime - deductions_health - sss)*0.2
                total_pay= ((float(rate)/2)+ earnings_allowance + overtime- deductions_health- sss)- deductions_tax
            Payslip.objects.create(id_number=e, month=month, date_range=date_range, year=year, pay_cycle=pay_cycle, rate=rate, earnings_allowance = earnings_allowance, deductions_tax = deductions_tax, deductions_health = deductions_health, pag_ibig = pag_ibig, sss = sss, overtime = overtime, total_pay = total_pay)
            Employee.objects.filter(pk=x.pk).update(overtime_pay=0)
        messages.success(request, "Payslip generated.")
        return redirect('create_payslip')                              
    else:
        return render(request, 'payroll_app/create_payslip.html', {'payslips':payslip_objects,'employees':employee_objects})

def delete_payslip(request, pk):
    payslip_objects = Payslip.objects.all()
    item = Payslip.objects.get(pk=pk)

    if(request.method == 'POST'):
        item.delete()  
        messages.info(request, "Payslip has been deleted.")      
        return redirect('create_payslip')
    else:
        return render(request, 'payroll_app/delete_payslip.html', {'payslips':payslip_objects,'pk':pk})
    
def deleteall(request):
    Payslip.objects.all().delete()
    messages.info(request, "All payslips have been deleted.")
    return redirect('create_payslip')