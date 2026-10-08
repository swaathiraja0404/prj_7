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
    
    def __str__(self):
        return self.name