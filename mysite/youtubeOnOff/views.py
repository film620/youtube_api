from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime, timedelta, date
from .models import OnOff

def index(request):
    on_off_list = OnOff.objects.all()
    result = []

    for idx in range(len(on_off_list)):
        on_off_list[idx].title = "A"
        on_off_list[idx].work_time += timedelta(hours=9)

    return render(request, 'youtubeOnOff/index.html', {'on_off_list': on_off_list})

def create_onoff(request):
    if request.method == 'POST':
        title = request.POST['title']
        modified_time = datetime.today().isoformat()
        video_id = request.POST['video_id']

        work_time_str = request.POST['work_time']
        work_time = datetime.strptime(work_time_str, '%Y-%m-%dT%H:%M')  - timedelta(hours=9)

        privacy_status = request.POST['privacy_status']

        OnOff.objects.create(title=title, modified_time=modified_time, video_id=video_id, work_time=work_time, privacy_status=privacy_status)
        
        return redirect(reverse('index'))
    else:
        return render(request, 'youtubeOnOff/create_onoff.html')

def edit_onoff(request, onoff_id):
    onoff = OnOff.objects.get(id=onoff_id)
    context = { 'onoff': onoff }

    if request.method == 'POST':
        onoff.title = request.POST['title']
        onoff.modified_time = datetime.today().isoformat()
        onoff.video_id = request.POST['video_id']

        work_time_str = request.POST['work_time']
        onoff.work_time = datetime.strptime(work_time_str, '%Y-%m-%dT%H:%M')  - timedelta(hours=9)

        onoff.privacy_status = request.POST['privacy_status']
        onoff.save()

        return redirect(reverse('index'))
    else: # GET request from index.html
        return render(request, 'youtubeOnOff/edit_onoff.html', context)

def delete_onoff(request, onoff_id):
    onoff = OnOff.objects.get(id=onoff_id)
    context = { 'onoff': onoff }

    if request.method == 'POST':
        onoff.delete()
        return redirect(reverse('index'))
    else: # GET request from index.html
        return render(request, 'youtubeOnOff/delete_onoff.html', context)
