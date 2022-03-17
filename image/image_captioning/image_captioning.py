import datetime
import torch
import torchvision.transforms as transforms

from django.conf import settings
from PIL import Image
import pickle
import math
import io
import os
from .models import EncoderCNN, DecoderRNN


#hyperparameters
EMBEDDING_DIM = 256
HIDDEN_DIM = 512
NUM_LAYERS = 2
BEAM_SIZE = 5
MAX_SEG_LENGTH = 20
ID_TO_WORD_PATH = os.path.join(settings.STATIC_ROOT, 'vocab/id_to_word.pkl')
with open(ID_TO_WORD_PATH, 'rb') as f:
        ID_TO_WORD = pickle.load(f)
END_ID = [k for k, v in ID_TO_WORD.items() if v == '<end>'][0]
VOCAB_SIZE = len(ID_TO_WORD)
ENCODER_PATH =  os.path.join(settings.STATIC_ROOT, 'model/encoder.pth')
DECODER_PATH = os.path.join(settings.STATIC_ROOT, 'model/decoder.pth')

# load models only once
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Running in %s." % device)
encoder = EncoderCNN(EMBEDDING_DIM)
encoder = encoder.to(device).eval()

decoder = DecoderRNN(EMBEDDING_DIM, HIDDEN_DIM, VOCAB_SIZE, NUM_LAYERS, MAX_SEG_LENGTH)
decoder = decoder.to(device).eval()

# Load the trained model parameters
# encoder.linear.load_state_dict(torch.load(ENCODER_LINEAR_PATH))
# encoder.bn.load_state_dict(torch.load(ENCODER_BN_PATH))
encoder.load_state_dict(torch.load(ENCODER_PATH))
decoder.load_state_dict(torch.load(DECODER_PATH))

def transform_image(image_bytes):
    """
    Transform image into required DenseNet format: 224x224 with 3 RGB channels and normalized.
    Return the corresponding tensor.
    """
    my_transforms = transforms.Compose([transforms.Resize([224, 224], Image.LANCZOS),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    return my_transforms(image).unsqueeze(0)

def inference(image_bytes):
    """For given image bytes, output the cations and probilities using the EncoderCNN and DecoderRNN"""
    # Choose Device
    
    # Prepare an image
    image = transform_image(image_bytes).to(device)

    # Generate an caption from the image
    with torch.no_grad():
        feature = encoder(image)
        sampled_ids = decoder.beam_search(feature, BEAM_SIZE, END_ID)
    res=[]
    # Convert word_ids to words
    for i, (sampled_id, prob) in enumerate(sampled_ids):
        sampled_id = sampled_id.cpu().numpy()
        sampled_caption = []
        for word_id in sampled_id:
            word = ID_TO_WORD[word_id]
            if word != '<end>' and word != '<start>':
                sampled_caption.append(word)
            if word == '<end>':
                break
        sentence = ' '.join(sampled_caption)
        res.append((sentence, math.exp(prob.item()/len(sampled_id))*100))
    return res