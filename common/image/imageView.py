from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from common.image.imageServices import upload_image
from .models import RefType



class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        image_file = request.FILES.get('image_file')
        ref_type = request.data.get('ref_type')
        ref_id = request.data.get('ref_id')

        if not image_file or not ref_type or not ref_id:
            return Response({'error': '필수 항목 누락'}, status=status.HTTP_400_BAD_REQUEST)

        image = upload_image(
            user=request.user,
            image_file=image_file,
            ref_type=ref_type,
            ref_id=int(ref_id)
        )

        return Response({
            'id': image.id,
            'url': image.url,
            'ref_type': image.ref_type,
            'ref_id': image.ref_id
        }, status=status.HTTP_201_CREATED)
