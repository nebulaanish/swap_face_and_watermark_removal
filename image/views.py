from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import ImageSerializer
from .utils import face_swap, download_image, create_mask, remove_watermark, image_to_b64


class ImageView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()   
            instance.result_url = face_swap(instance.image_url, instance.face_url)
            instance.save()

            # Download image
            result_path = f'media/results/{instance.pk}_result.jpg'
            download_image(instance.result_url, result_path)

            # Create Mask
            mask_path = f'media/masks/{instance.pk}_mask.png'
            create_mask(instance.result_url, result_path, mask_path)

            # remove Watermark
            path = f"media/output/{instance.pk}_result.jpg"
            result_binary = remove_watermark(result_path, mask_path, path)
            instance.result_image_path = path
            instance.save()
            # print(result_binary)
            return Response({'binary_file': result_binary}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FaceSwapView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()   
            instance.result_url = face_swap(instance.image_url, instance.face_url)
            instance.save()
            result_path = f'media/results/{instance.pk}_result.jpg'
            download_image(instance.result_url, result_path)   
            return Response({'result_image': image_to_b64(result_path)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveWatermarkView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            result_path = f'media/results/watermark/{instance.pk}_result.jpg' 
            download_image(instance.result_url, result_path)  
            mask_path = f'media/masks/{instance.pk}_mask.png'
            create_mask(instance.result_url, result_path, mask_path)
               
            return Response({'result_image': image_to_b64(result_path)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Create your views here.
# class HelloView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)