from rest_framework import serializers
from rest_framework.validators import *
from bookApp.models import *

class CbtClassesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CbtClasses
        fields = '__all__'

# SERIALIZER FOR ADD OR UPDATE 

class CbtBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CbtBoard
        fields = '__all__'

# SERIALIZER FOR ADD OR UPDATE 

class CbtSeriesSerializer(serializers.ModelSerializer):

    PR_NAME = serializers.CharField(required=True)
    PR_BOARD_id = serializers.IntegerField(write_only=True, required=True)
    PR_CLASSES = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )

    class Meta:
        model = CbtSeries
        fields = ['PR_SERIES_ID', 'PR_NAME', 'PR_BOARD_id', 'PR_CLASSES', 'PR_CREATED_AT', 'PR_MODIFIED_AT']
        read_only_fields = ['PR_CREATED_AT', 'PR_MODIFIED_AT']
        
    def validate_PR_CLASSES(self, value):
        non_existing_classes = [PR_CLASS_ID for PR_CLASS_ID in value if not CbtClasses.objects.filter(PR_CLASS_ID=PR_CLASS_ID).exists()]
        if non_existing_classes:
            raise serializers.ValidationError(
                f"The following classes id's do not exist: {non_existing_classes}"
            )
        return value
    
class CbtSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CbtSubject
        fields = '__all__'

# SERIALIZER FOR ADD OR UPDATE 

class CbtBookTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CbtBookType
        fields = '__all__'

# SERIALIZER FOR ADD OR UPDATE 

class CbtBookDataSerializer(serializers.ModelSerializer):

    PR_TITLE = serializers.CharField(required=True)    
    PR_SERIES_id = serializers.IntegerField(required=True)
    PR_CLASS_id = serializers.IntegerField(required=True)
    PR_BOARD_id = serializers.IntegerField(required=True)
    PR_BOOK_TYPE_id = serializers.IntegerField(required=True)

    class Meta:
        model = CbtBookData
        fields = ['PR_TITLE', 'PR_SUB_TITLE', 'PR_BOOK_TYPE_id','PR_CLASS_id', 'PR_BOARD_id', 'PR_SERIES_id', 'PR_ISBN','PR_BOOK_NUMBER','PR_CLASS_LEVEL','PR_PRODUCT_DIVISION','PR_BROAD_SUBJECT','PR_DETAILED_SUBJECT','PR_AUTHOR',
                  'PR_EDITION' , 'PR_IMPRINT','PR_BOOK_CODE','PR_COPYRIGHT','PR_DATE_OF_RELEASE','PR_BINDING','PR_LANGUAGE','PR_PAGES','PR_TRIM_SIZE','PR_WEIGHT','PR_LIST_PRICE','PR_DISCOUNT','PR_PRODUCT_DESCRIPTION',
                  'PR_COMPANY']
        read_only_fields = ['PR_CREATED_AT', 'PR_MODIFIED_AT']

# SERIALIZAR FOR BOOK DATA OR LIST

class CbtBookDataListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CbtBookData
        fields = '__all__'

class CbtSeriesDataListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CbtSeries
        fields = '__all__'
