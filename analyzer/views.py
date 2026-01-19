from django.shortcuts import render, redirect
from django.conf import settings
from .models import Subject, Grade
from .forms import GradeForm, SubjectForm
import pandas as pd
import matplotlib.pyplot as plt
import os


def dashboard(request):
    grades = Grade.objects.select_related('subject')

    form = GradeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard')

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
        plt.tight_layout()

        charts_dir = os.path.join(settings.MEDIA_ROOT, 'charts')
        os.makedirs(charts_dir, exist_ok=True)

        chart_path = os.path.join(charts_dir, 'avg_grades.png')
        plt.savefig(chart_path)
        plt.close()

        chart_url = settings.MEDIA_URL + 'charts/avg_grades.png'

    return render(request, 'analyzer/dashboard.html', {
        'form': form,
        'grades': grades,
        'stats': stats,
        'chart_url': chart_url
    })


def delete_grade(request, grade_id):
    Grade.objects.get(id=grade_id).delete()
    return redirect('dashboard')


def subject_list(request):
    subjects = Subject.objects.all()

    form = SubjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('subject_list')

    return render(request, 'analyzer/subject_list.html', {
        'subjects': subjects,
        'form': form
    })


def delete_subject(request, subject_id):
    Subject.objects.get(id=subject_id).delete()
    return redirect('subject_list')
