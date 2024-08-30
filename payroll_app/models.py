'''
We have not discussed the Python language code in our program with anyone other than our instructor
or the teaching assistants assigned to this course.
We have not used Python language code obtained from another student, or any other unauthorized
source, either modified or unmodified.
If any Python language code or documentation used in our program was obtained from another source,
such as a textbook or course notes, that has been clearly noted with a proper citation in the
comments of our program.
'''

from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=300)
    id_number = models.CharField(max_length=300)
    rate = models.FloatField(max_length=300)
    overtime_pay = models.FloatField(null=True)
    allowance = models.FloatField(null=True)
    objects = models.Manager()
    
    def getName(self):
        return self.name
    
    def getID(self):
        return self.id_number

    def getRate(self):
        return self.rate    
    
    def getOvertime(self):
        return self.overtime_pay
    
    def resetOvertime(self):
        self.overtime_pay = 0 

    def getAllowance(self):
        return self.allowance
    
    def __str__(self):
        return 'pk: ' +self.id_number +', rate: ' + str(self.rate)
    
class Payslip(models.Model):
    id_number = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=300)
    date_range = models.CharField(max_length=300)
    year = models.CharField(max_length=300)
    pay_cycle = models.IntegerField(null=True)
    rate = models.FloatField(max_length=300)
    earnings_allowance = models.FloatField(max_length=300)
    deductions_tax = models.FloatField(max_length=300)
    deductions_health = models.FloatField(max_length=300)
    pag_ibig = models.FloatField(max_length=300)
    sss = models.FloatField(max_length=300)
    overtime = models.FloatField(max_length=300)
    total_pay = models.FloatField(max_length=300)
    objects = models.Manager()
        
    def getIDNumber(self):
        return self.id_number

    def getMonth(self):
        return self.month    
    
    def getDate_range(self):
        return self.date_range
    
    def getYear(self):
        return self.year
        
    def getPay_cycle(self):
        return self.pay_cycle
    
    def getRate(self):
        return self.rate

    def getCycleRate(self):
        return self.rate*0.5    
    
    def getEarnings_allowance(self):
        return self.earnings_allowance
    
    def getDeductions_tax(self):
        return self.deductions_tax
    
    def getDeductions_health(self):
        return self.deductions_health
    
    def getPag_ibig(self):
        return self.pag_ibig  
    
    def getSSS(self):
        return self.sss
    
    def getOvertime(self):
        return self.overtime
    
    def  getTotal_pay(self):
        return self.total_pay
    
    def __str__(self):
        return 'pk: ' + str(self.pk) + ', Employee: ' + str(self.id_number) + ', Period: '+ str(self.month) + ' ' + str(self.date_range) + ', ' + str(self.year) +', Cycle: ' + str(self.pay_cycle) + ', Total Pay: ' + str(self.total_pay)