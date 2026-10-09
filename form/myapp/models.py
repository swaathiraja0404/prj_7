from django.db import models
class MyappStudent(models.Model):

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    dod = models.DateField(null=True)
    phone=models.CharField(max_length=10,null=True)
    email = models.CharField(unique=True, max_length=254)
    
    class Meta:
        db_table = 'myapp_student'

class MyappStaff(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    dod = models.DateField(null=True)
    phone=models.CharField(max_length=10,null=True)
    email = models.CharField(unique=True, max_length=254)
    department = models.CharField(max_length=100,null=True)
    

    def __str__(self):
        return self.name
class Department(models.Model):
    id = models.BigAutoField(primary_key=True)
    dept_name = models.CharField(max_length=100)

class UserAuth(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=254)
    password = models.CharField(max_length=254, null=True, blank=True)
    role = models.CharField(max_length=20)

    class meta:
        db_table = 'myapp_userauth'

    def __str__(self):
        return self.username

