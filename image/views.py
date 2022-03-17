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

# PyTorch-related code from: https://pytorch.org/tutorials/intermediate/flask_rest_api_tutorial.html
# load pretrained DenseNet and go straight to evaluation mode for inference
# load as global variable here, to avoid expensive reloads with each request




# def transform_image(image_bytes):
#     """
#     Transform image into required DenseNet format: 224x224 with 3 RGB channels and normalized.
#     Return the corresponding tensor.
#     """
#     my_transforms = transforms.Compose([transforms.Resize(255),
#                                         transforms.CenterCrop(224),
#                                         transforms.ToTensor(),
#                                         transforms.Normalize(
#                                             [0.485, 0.456, 0.406],
#                                             [0.229, 0.224, 0.225])])
#     image = Image.open(io.BytesIO(image_bytes))
#     return my_transforms(image).unsqueeze(0)


# def get_prediction(image_bytes):
#     """For given image bytes, predict the label using the pretrained DenseNet"""
#     tensor = transform_image(image_bytes)
#     outputs = model.forward(tensor)
    
    
#     percentage = torch.nn.functional.softmax(outputs, dim=1)[0] * 100
#     _, indices = torch.sort(outputs, descending=True)
#     # _, y_hat = outputs.max(1)
#     res=[(imagenet_mapping[str(idx.item())][1], percentage[idx.item()].item()) for idx in indices[0][:5]]
#     # predicted_idx = str(y_hat.item())
#     # class_name, human_label = imagenet_mapping[predicted_idx]
#     return res


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

if __name__ == '__main__':
    print(inference(open("D:\R.jpg", 'rb').read()))