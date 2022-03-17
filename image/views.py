import base64
import io
import json
import os
import torch
from PIL import Image
from django.shortcuts import render
from django.conf import settings

from .forms import ImageUploadForm
from .image_captioning.image_captioning import inference



def index(request):
    image_uri = None
    predicted_res = None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # passing the image as base64 string to avoid storing it to DB or filesystem
            image = form.cleaned_data['image']
            image_bytes = image.file.read()
            encoded_img = base64.b64encode(image_bytes).decode('ascii')
            image_uri = 'data:%s;base64,%s' % ('image/jpeg', encoded_img)

            # get predicted label
            try:
                predicted_res = inference(image_bytes)
            except RuntimeError as re:
                print(re)
                # predicted_label = "Prediction Error"

    else:
        form = ImageUploadForm()

    context = {
        'form': form,
        'image_uri': image_uri,
        'predicted_res': predicted_res,
    }
    return render(request, 'image/index.html', context)
