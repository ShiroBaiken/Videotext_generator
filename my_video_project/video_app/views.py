import os

from django.shortcuts import render
from django.http import HttpResponse
from .forms import VideoForm
from .models import Video
from .video_generator import ScrollingTextMaker
from django.conf import settings


def save_image(image) -> str:
    """
    Saves provided image locally in project media dir
    :param image: data from form
    :return: path to saved image
    """
    image_path = os.path.join(settings.MEDIA_ROOT, image.name)
    with open(image_path, 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)
    return image_path


def generate_video_file(text: str, image_path: str = None) -> str:
    """
    Creates file locally and returns path to saved video file
    :param text: text from form or url
    :param image_path: path to provided image, if exist
    :return: path to generated file
    """
    try:
        output_filename = f"output_{text[:10]}_{os.path.basename(image_path).split('.')[0] if image_path else 'no_image'}.webm"
        output_path = os.path.join(settings.MEDIA_ROOT, output_filename)
        cm = ScrollingTextMaker(text, image_path)
        cm.create_video_from_text(output_path)
        return output_filename

    except Exception as e:
        raise





def generate_video(request, text: str = None) -> HttpResponse:
    """
    Generates HttpResponse based on request method and data from forms. Generates local videofile in webm format
    :param request:
    :param text:
    :return: HttpResponse
    """
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data['text']
            image = form.cleaned_data.get('image')
            image_path = None
            image_name = None
            if image:
                image_path = save_image(image)
                image_name = image.name
            try:
                output_filename = generate_video_file(text, image_path)
                video_url = os.path.join(settings.MEDIA_URL, output_filename)
                video = Video(text=text, image=image_name, video_file=output_filename)
                video.save()
                return render(request, 'video_generated.html', {'video_url': video_url})
            except Exception as e:
                return HttpResponse(f"Error creating video: {e}", status=500)
    else:
        if text:
            form = VideoForm(initial={'text': text})
            return render(request, 'form.html', {'form': form, 'text_from_url': True})
    return render(request, 'form.html', {'form': VideoForm()})
