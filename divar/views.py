from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from divar.models import Category, Divar, Attribute, DivarImage
from divar.serializers import DivarSerializer, AttributeSerializer, CategorySerializer


class CategoryListView(APIView):
    """
    API برای دریافت لیست همه دسته‌بندی‌ها.
    """

    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AttributeListView(APIView):
    """
    API برای دریافت لیست ویژگی‌های یک دسته‌بندی خاص و زیرمجموعه‌های آن.
    """

    def get(self, request, category_id, format=None):
        # دریافت دسته‌بندی خاص با شناسه category_id
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        # ویژگی‌های اختصاصی
        specific_attributes = Attribute.objects.filter(category=category)

        # ویژگی‌های عمومی: ویژگی‌هایی که به دسته‌بندی‌های عمومی تعلق دارند
        # دریافت دسته‌بندی والد
        parent_category = category.parent

        # جمع‌آوری ویژگی‌های عمومی
        if parent_category:
            # ویژگی‌های عمومی
            general_attributes = Attribute.objects.filter(category=parent_category)
        else:
            # اگر دسته‌بندی والد وجود ندارد، ویژگی‌های عمومی را فقط از خود دسته‌بندی دریافت کنید
            general_attributes = Attribute.objects.filter(category=category)

        # ترکیب ویژگی‌های عمومی و اختصاصی
        attributes = general_attributes | specific_attributes

        # حذف تکراری‌ها
        attributes = attributes.distinct()

        serializer = AttributeSerializer(attributes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DivarListCreateView(APIView):
    """
    API برای دریافت لیست آگهی‌ها و ایجاد آگهی جدید.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        divars = Divar.objects.all()
        serializer = DivarSerializer(divars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = DivarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DivarImageUploadView(APIView):
    """
    API برای آپلود تصاویر مربوط به یک آگهی خاص.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, divar_id, format=None):
        try:
            divar = Divar.objects.get(pk=divar_id)
        except Divar.DoesNotExist:
            return Response({"error": "Divar not found"}, status=status.HTTP_404_NOT_FOUND)

        for file in request.FILES.getlist('images'):
            image = DivarImage.objects.create(divar=divar, image=file)
            image.save()

        return Response({"message": "Images uploaded successfully"}, status=status.HTTP_201_CREATED)


class DivarDetailView(APIView):
    """
    این ویو برای مشاهده، ویرایش و حذف یک آگهی خاص استفاده می‌شود.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        متد کمکی برای دریافت یک آگهی خاص با استفاده از شناسه آن.
        """
        try:
            return Divar.objects.get(pk=pk)
        except Divar.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        متد GET برای دریافت جزئیات یک آگهی خاص.
        """
        divar = self.get_object(pk)
        serializer = DivarSerializer(divar)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        متد PUT برای ویرایش یک آگهی خاص.
        """
        divar = self.get_object(pk)
        serializer = DivarSerializer(divar, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        متد DELETE برای حذف یک آگهی خاص.
        """
        divar = self.get_object(pk)
        divar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
