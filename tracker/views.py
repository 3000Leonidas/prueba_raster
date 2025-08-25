# tracker/views.py
import requests
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse
import uuid

from .models import TrackerURL, Visit

def create_tracker(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image_file = request.FILES.get('image_to_show')

        tracker = TrackerURL.objects.create(name=name, image_to_show=image_file) # ¡CAMBIADO!

        tracking_url = request.build_absolute_uri(reverse('track_image', args=[tracker.tracker_id]))

        return render(request, 'tracker/tracker_created.html', {'tracking_url': tracking_url, 'tracker': tracker})

    return render(request, 'tracker/create_tracker.html')

def track_image(request, tracker_id):
    tracker_url = get_object_or_404(TrackerURL, tracker_id=tracker_id)

    ip_address = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT')
    referer = request.META.get('HTTP_REFERER')

    try:
        response = requests.get(f'http://ip-api.com/json/{ip_address}')
        response.raise_for_status()
        geo_data = response.json()
    except (requests.exceptions.RequestException, ValueError):
        geo_data = None

    country, city, latitude, longitude = None, None, None, None
    if geo_data and geo_data.get('status') == 'success':
        country = geo_data.get('country')
        city = geo_data.get('city')
        latitude = geo_data.get('lat')
        longitude = geo_data.get('lon')

    Visit.objects.create(
        tracker_url=tracker_url,
        ip_address=ip_address,
        user_agent=user_agent,
        referer=referer,
        country=country,
        city=city,
        latitude=latitude,
        longitude=longitude
    )

    if tracker_url.image_to_show:
        with tracker_url.image_to_show.open('rb') as f:
            return HttpResponse(f.read(), content_type="image/jpeg")

    raise Http404("No se ha encontrado la imagen para este rastreador.")