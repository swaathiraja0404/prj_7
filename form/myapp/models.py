from django.db import models
class MyappStudent(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    dod = models.DateField(null=True)
    phone=models.CharField(max_length=10,null=True)
    email = models.CharField(unique=True, max_length=254)
    department = models.CharField(max_length=100,null=True)    
    class Meta:
        db_table = 'myapp_student'
    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.dept_name

class UserAuth(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=254)
    password = models.CharField(max_length=254, null=True, blank=True)
    role = models.CharField(max_length=20)

    class Meta:
        db_table = 'myapp_userauth'

    def __str__(self):
        return self.username

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_code = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"


class Timetable(models.Model):
    
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    staff = models.ForeignKey(
        MyappStaff,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    day = models.CharField(
        max_length=15,
        choices=DAY_CHOICES
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    def __str__(self):
        return f"{self.staff.name} - {self.subject.subject_name} - {self.day}"

class StudentMark(models.Model):
    student = models.ForeignKey(
        MyappStudent,
        on_delete=models.CASCADE,
        related_name='marks'
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='student_marks'
    )

    staff = models.ForeignKey(
        MyappStaff,
        on_delete=models.CASCADE,
        related_name='entered_marks'
    )

    internal_marks = models.PositiveSmallIntegerField(default=0)
    external_marks = models.PositiveSmallIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'subject'],
                name='unique_student_subject_marks'
            )
        ]

    @property
    def total_marks(self):
        return self.internal_marks + self.external_marks

    def __str__(self):
        return f"{self.student.name} - {self.subject.subject_name}"


