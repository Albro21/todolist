from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from collections import defaultdict
from datetime import timedelta
import json

from .models import TimeEntry

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f'{hours:02}:{minutes:02}:{seconds:02}'

def timetracker(request):
    user = request.user
    
    tasks = user.tasks.filter(is_completed=False)
    projects = user.projects.all()
    time_entries = user.time_entries.filter(end_time__isnull=False)
    
    # Initialize defaultdict to store time entries grouped by date and name
    grouped_time_entries = defaultdict(lambda: defaultdict(lambda: {'time_entries': [], 'total_duration': timedelta()}))

    for entry in time_entries:
        date_key = entry.end_time.strftime('%A, %d-%m')
        name_key = entry.name

        # Group time entries by date and name
        grouped_time_entries[date_key][name_key]['time_entries'].append(entry)
        grouped_time_entries[date_key][name_key]['total_duration'] += entry.duration
    
    def recursive_dict(d):
        if isinstance(d, defaultdict):
            d = {k: recursive_dict(v) for k, v in d.items()}
        return d

    grouped_time_entries = recursive_dict(grouped_time_entries)

    # Calculate total duration for each date group
    for date_key, name_groups in grouped_time_entries.items():
        # Initialize total duration for the date group
        date_total_duration = timedelta()
        
        for name_key, group in name_groups.items():
            # Add the total duration for each name group to the date's total duration
            date_total_duration += group['total_duration']
            group['total_duration'] = format_timedelta(group['total_duration'])  # Format name group duration

        # Add the total duration for the entire date group
        grouped_time_entries[date_key]['date_total_duration'] = format_timedelta(date_total_duration)
    
    context = {
        'tasks': tasks,
        'projects': projects,
        'grouped_time_entries': grouped_time_entries,
    }

    return render(request, 'timetracker/timetracker.html', context)

@require_POST
def start_timer(request):
    data = json.loads(request.body) 
    task_id = data.get('task_id')
    name = data.get('name')
    project_id = data.get('project_id')

    task = request.user.tasks.filter(id=task_id).first() if task_id else None
    project = request.user.projects.filter(id=project_id).first() if project_id else None

    if task:
        time_entry = TimeEntry.objects.create(
            user=request.user, 
            task=task, 
            name=task.title, 
            project=task.project,
        )
    else:
        time_entry = TimeEntry.objects.create(
            user=request.user, 
            name=name, 
            project=project,
        )

    time_entry.start()
    return JsonResponse({'success': True,})

@require_POST
def stop_timer(request):
    request.user.time_entries.filter(end_time__isnull=True).first().stop()
    return JsonResponse({'success': True,})