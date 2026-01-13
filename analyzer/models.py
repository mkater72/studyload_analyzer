from django.db import models

class Semester(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    weekly_hours = models.PositiveIntegerField()
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name='subjects'
    )

    def __str__(self):
        return self.name


class Grade(models.Model):
    GRADE_CHOICES = [(2, '2'), (3, '3'), (4, '4'), (5, '5')]

    value = models.IntegerField(choices=GRADE_CHOICES)
    date = models.DateField()
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='grades'
    )

    def __str__(self):
        return f'{self.subject.name}: {self.value}'
