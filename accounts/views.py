from django.shortcuts import render, redirect
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.db import IntegrityError
from .models import *
import cv2
import numpy as np

# Create your views here.

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        face_image_data = request.POST.get('face_image')
        print(face_image_data)
        face_image_data = face_image_data.split(',')[1]
        face_image = ContentFile(base64.b64decode(face_image_data), name=f'{username}_.jpg')
        print(face_image)
        try:
            user = User.objects.create(username = username)
        except IntegrityError:
            return JsonResponse({
                'status': 'error',
                'message': 'username already taken'
            })
        
        UserImages.objects.create(user = user, face_image = face_image)
        return JsonResponse({
            'status': 'success',
            'message': 'User registered successfully',
            'redirect': f'/dashboard/?username={username}'
        })
        
        

    return render(request, 'register.html')

    
    
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        face_image_data = request.POST.get('face_image')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User not found'
            })
        
        face_image_data = face_image_data.split(",")[1]
        uploaded_image_bytes = base64.b64decode(face_image_data)
        
        # Convert bytes to numpy array for OpenCV
        nparr = np.frombuffer(uploaded_image_bytes, np.uint8)
        uploaded_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Load stored face image
        user_image = UserImages.objects.filter(user=user).last()
        if not user_image:
            return JsonResponse({
                'status': 'error',
                'message': 'No face image found for user'
            })
        
        stored_image = cv2.imread(user_image.face_image.path)
        
        # Initialize face detector
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Detect faces in both images
        uploaded_faces = face_cascade.detectMultiScale(uploaded_image, 1.1, 4)
        stored_faces = face_cascade.detectMultiScale(stored_image, 1.1, 4)
        
        if len(uploaded_faces) == 0 or len(stored_faces) == 0:
            return JsonResponse({
                'status': 'error',
                'message': 'No face detected in one of the images'
            })
        
        # Extract face regions for comparison
        (x1, y1, w1, h1) = stored_faces[0]  # Use first detected face from stored image
        (x2, y2, w2, h2) = uploaded_faces[0]  # Use first detected face from uploaded image
        
        stored_face = stored_image[y1:y1+h1, x1:x1+w1]
        uploaded_face = uploaded_image[y2:y2+h2, x2:x2+w2]
        
        # Resize faces to same size for comparison
        size = (100, 100)
        stored_face_resized = cv2.resize(stored_face, size)
        uploaded_face_resized = cv2.resize(uploaded_face, size)
        
        # Convert to grayscale for comparison
        stored_gray = cv2.cvtColor(stored_face_resized, cv2.COLOR_BGR2GRAY)
        uploaded_gray = cv2.cvtColor(uploaded_face_resized, cv2.COLOR_BGR2GRAY)
        
        # Calculate histogram correlation for face matching
        hist_stored = cv2.calcHist([stored_gray], [0], None, [256], [0, 256])
        hist_uploaded = cv2.calcHist([uploaded_gray], [0], None, [256], [0, 256])
        
        # Normalize histograms
        cv2.normalize(hist_stored, hist_stored, 0, 255, cv2.NORM_MINMAX)
        cv2.normalize(hist_uploaded, hist_uploaded, 0, 255, cv2.NORM_MINMAX)
        
        # Compare histograms using correlation
        correlation = cv2.compareHist(hist_stored, hist_uploaded, cv2.HISTCMP_CORREL)
        
        # Set threshold for face matching (0.6 is a reasonable threshold)
        threshold = 0.6
        
        if correlation < threshold:
            return JsonResponse({
                'status': 'error',
                'message': 'Face does not match. Please try again.'
            })
        
        return JsonResponse({
            'status': 'success',
            'message': 'User logged in successfully',
            'redirect': f'/dashboard/?username={username}'
        })

    return render(request, 'login.html')


def logout(request):
    return redirect('home')

def profile(request):
    return render(request, 'profile.html')

def settings(request):
    return render(request, 'settings.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def home(request):
    return render(request,'home.html')