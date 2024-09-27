from django.conf import settings
from bookApp.models import *
from django.db.models import Q
import os
import zipfile
import random

def dataUnzip(file):
    try:
        directory = str(random.randint(10000000, 99999999))
        path = os.path.join(str(settings.BASE_DIR)+f'/media/activities/', directory) 
        os.mkdir(path)

        target_file = str(settings.BASE_DIR)+f'/media/activities/{directory}'

        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(target_file)

        return True, f'media/activities/{directory}/index.html'
    
    except:
        return False, 'Something went wrong!!'

# =========== FILTER DATA CLASS HERE ===============
class CbtFliterData:

    def _init_(self, query_data) -> None:
        self.query_data = query_data

 
    def bookTypeFilter(self):
        data_objs = CbtBookType.objects.filter(Q(PR_NAME__istartswith=self.query_data)).order_by('-PR_BOOK_TYPE_ID')
        return data_objs
    
    def seriesFilter(self):
        data_objs = CbtSeries.objects.filter(Q(PR_NAME__istartswith=self.query_data)).order_by('-PR_SERIES_ID')
        return data_objs
    
    def boardFilter(self):
        data_objs = CbtBoard.objects.filter(Q(PR_NAME__istartswith=self.query_data)).order_by('-PR_BOARD_ID')
        return data_objs
    
    def subjectFilter(self):
        data_objs = CbtBoard.objects.filter(Q(PR_NAME__istartswith=self.query_data)).order_by('-PR_SUBJECT_ID')
        return data_objs
    
    def classFilter(self):
        data_objs = CbtClasses.objects.filter(Q(PR_NAME__istartswith=self.query_data)).order_by('-PR_CLASS_ID')
        return data_objs
    
    def bookFilter(self):
        data_objs = CbtBookData.objects.filter(Q(PR_NAME__istartswith=self.query_data)).order_by('-PR_BOOK_ID')
        return data_objs
    
