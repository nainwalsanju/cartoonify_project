import cv2
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)
def cartoonify(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)

            # Get slider values
            edge_threshold = int(request.POST.get('edge_threshold', 9))
            bilateral_d = int(request.POST.get('bilateral_d', 9))
            bilateral_sigma_color = int(request.POST.get('bilateral_sigma_color', 300))
            bilateral_sigma_space = int(request.POST.get('bilateral_sigma_space', 300))

            # 1) Edges
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.medianBlur(gray, edge_threshold)
            edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, bilateral_d, bilateral_d)

            # 2) Color
            color = cv2.bilateralFilter(img, d=bilateral_d, sigmaColor=bilateral_sigma_color, sigmaSpace=bilateral_sigma_space)

            # 3) Cartoon
            cartoon = cv2.bitwise_and(color, color, mask=edges)

            # Convert the cartoonified image to JPEG format
            _, img_encoded = cv2.imencode('.jpg', cartoon)
            img_data = img_encoded.tobytes()

            # Send the image data as a response
            return HttpResponse(img_data, content_type='image/jpeg')

    return render(request, 'cartoonify/cartoonify.html')
