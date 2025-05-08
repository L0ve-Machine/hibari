from django.db import models


class Attendance(models.Model):
    CLASS_CHOICES = [
        ('月', '月'),
        ('星', '星'),
        ('雪', '雪'),
        ('虹', '虹'),
        ('その他', 'その他'),
    ]
    ATTEND_CHOICES = [
        ('出席', '出席'),
        ('欠席', '欠席'),
    ]
    student_class = models.CharField('クラス', max_length=10, choices=CLASS_CHOICES)
    name = models.CharField('名前', max_length=50)
    status = models.CharField('出欠', max_length=10, choices=ATTEND_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_class}組 {self.name} - {self.status}"
