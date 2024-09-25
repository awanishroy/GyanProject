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

 
    # def designationFilter(self):
    #     data_objs = CbtDesignation.objects.filter(Q(PR_NAME__istartswith=self.query_data)).order_by('-PR_DESIGNATION_ID')
    #     return data_objs
    
    # def departmentFilter(self):
    #     data_objs = CbtDepartment.objects.filter(Q(PR_NAME__istartswith=self.query_data)).order_by('-PR_DEPARTMENT_ID')
    #     return data_objs
    
    # def menuFilter(self):
    #     data_objs = CbtMenu.objects.filter(Q(PR_NAME__istartswith=self.query_data)).order_by('-PR_MENU_ID')
    #     return data_objs
    
    # def submenuFilter(self):
    #     data_objs = CbtSubmenu.objects.filter(Q(PR_NAME__istartswith=self.query_data)).order_by('-PR_SUBMENU_ID')
    #     return data_objs
    

