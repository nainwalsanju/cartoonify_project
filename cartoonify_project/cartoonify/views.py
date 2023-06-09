import cv2
import numpy as np
from django.shortcuts import render
import base64

def cartoonify(request):
    if request.method == 'POST':
        image = request.FILES['image']
        img = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)
        
        # 1) Edges
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        
        # 2) Color
        color = cv2.bilateralFilter(img, d=9, sigmaColor=300, sigmaSpace=300)
        
        # 3) Cartoon
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        
        _, img_encoded = cv2.imencode('.jpg', cartoon)
        img_data = img_encoded.tobytes()
        cartoon_data_url = f"data:image/jpeg;base64,{base64.b64encode(img_data).decode('utf-8')}"
        print("loaaded")
        return render(request, 'cartoonify/cartoonify.html', {'cartoon_data_url': cartoon_data_url})
    
    return render(request, 'cartoonify/cartoonify.html')
