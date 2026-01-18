from django.shortcuts import render
from .models import Subject, Grade
from .forms import GradeForm
import pandas as pd
import matplotlib.pyplot as plt
import os
from django.conf import settings


def dashboard(request):
    grades = Grade.objects.select_related('subject')

    data = [{
        'subject': g.subject.name,
        'grade': g.value,
        'hours': g.subject.weekly_hours
    } for g in grades]

    df = pd.DataFrame(data)

    stats = {}
    chart_url = None

    if not df.empty:
        grouped = df.groupby('subject').agg(
            average_grade=('grade', 'mean'),
            weekly_hours=('hours', 'mean')
        ).round(2)

        stats = grouped.to_dict('index')

        plt.figure(figsize=(10, 6))

        grouped['average_grade'].plot(kind='bar')

        plt.title('Средний балл по предметам', fontsize=14)
        plt.ylabel('Средний балл', fontsize=12)
        plt.xlabel('Предмет', fontsize=12)

        plt.xticks(rotation=45, ha='right')
        plt.ylim(0, 5)

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()


        chart_path = os.path.join(settings.MEDIA_ROOT, 'charts', 'avg_grades.png')
        plt.savefig(chart_path)
        plt.close()

        chart_url = settings.MEDIA_URL + 'charts/avg_grades.png'

    form = GradeForm(request.POST or None)
    if form.is_valid():
        form.save()

    return render(request, 'analyzer/dashboard.html', {
        'stats': stats,
        'form': form,
        'chart_url': chart_url
    })
