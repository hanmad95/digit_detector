from django.shortcuts import render
from .forms import CanvasForm
import tensorflow as tf
from tensorflow import Graph, Session
from tensorflow.keras.models import load_model
from django.contrib.staticfiles import finders
import numpy as np
import cv2
import os
import base64
from PIL import Image,ImageOps
from io import BytesIO
import matplotlib.pyplot as plt

# ==========================================================================
# LOAD MODEL
#============================================================================
model_graph = Graph()
with model_graph.as_default():
    tf_session = Session()
    with tf_session.as_default():
        model = load_model('./models/mnist_model/keras_mnist.h5')

# ==========================================================================
# Functions
#===========================================================================

def predict_digit(img):
    """ Handwritten Image -> Digit """
    print("START")

    # Initialize prediction
    prediction = None

    # Convert Data String to Image
    image_b64 = img.split(",")[1]
    binary = base64.b64decode(image_b64)
    image = np.asarray(bytearray(binary), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # Convert to Grayscale
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print("Size before: ", img_gray.shape)

    # Invert Image
    img_transformed = 255 - img_gray
    img_transformed = img_transformed.astype('float32')
    img_transformed /= 255


    # Resize
    target_dimensions =(28,28)
    img_transformed  = cv2.resize(img_transformed , target_dimensions,interpolation = cv2.INTER_CUBIC)
    print("Size after: ", img_transformed.shape)

    with model_graph.as_default():
        with tf_session.as_default():
            img_transformed_input = img_transformed.reshape(1,784) #keras_mnist: (1,784)
            prediction = model.predict_classes(img_transformed_input)


    print("Prediction Done: ", prediction[0])
    output = "Predicted digit is: " + str(prediction[0]) +"."
    return output
    
# ==========================================================================
#  Views
#===========================================================================

# Create your views here.
def detect_numb_mainPage(request):
    return render(request,'app_detect_numb/detect_numb_main.html')

def detect_numb_process(request):

    # Initialize the variables
    down_arrow = " "
    canvas_data = " "
    headline = " "
    prediction = " "


    if request.method == "POST":
        # Make visible
        canvas_data = request.POST['canvasData']
        headline = " The submitted drawing: "
        down_arrow = r"&#8675;"


        # Predict the canvas data ------------------------
        with model_graph.as_default():
            with tf_session.as_default():
                prediction = predict_digit(canvas_data)

    return render(request,'app_detect_numb/detect_numb_main.html',{'prediction':prediction,'canvas_data':canvas_data,'headline':headline,'down_arrow':down_arrow})
