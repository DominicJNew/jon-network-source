from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Software

from PIL import Image, ImageDraw

def scriptlytics_image(request, software_id):
    img = Image.new('RGB', (190 + len(str(software_id))*6, 20), (16, 0, 155))
    d = ImageDraw.Draw(img)
    d.text((5, 5), "SCRIPTLYTICS #{} @ Jon's Network".format(software_id), fill=(255, 254, 0))
    
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


def graph(request, software_id):
    try:
        software = Software.objects.get(pk=software_id)
    except Software.DoesNotExist:
        return Http404
    
    return render(request, 'scriptlytics/graph.html', {'software': software})


@csrf_exempt
def hit(request):
    software_id = request.POST.get('id', None)
    username = request.POST.get('username', '')
    
    try:
        software = Software.objects.get(pk=software_id)
    except Software.DoesNotExist:
        return JsonResponse({
            'success': False,
            'reason': 'invalid software id'
        })
    
    software.hit(username)
    
    return JsonResponse({
        'success': True,
    })


@csrf_exempt
def new(request):
    software = Software()
    software.save()
    return JsonResponse({'id': software.pk})


@csrf_exempt
def get(request):
    try:
        software = Software.objects.get(pk=int(request.GET.get('id', -1)))
    except Software.DoesNotExist:
        return JsonResponse({'success': False, 'reason': 'invalid software id'})
    
    return JsonResponse({
        'hits': software.hits,
        'unique': software.unique_hits,
        'usernames': software.usernames,
    })
    
    