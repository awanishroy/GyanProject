import uuid
from django.conf import settings
from django.core.mail import send_mail
from bookApp.models import *
import os
from datetime import *
from django.core.files.storage import FileSystemStorage

def tokenUpdate(user_data):
    try:
        token = uuid.uuid4()
        CbtUser.objects.filter(PR_USER_ID=user_data.PR_USER_ID).update(PR_TOKEN=token)
        return CbtUser.objects.get(PR_USER_ID=user_data.PR_USER_ID)
    except:
        return None

# def userPermission(user_token, submenu_code=None):
#     if submenu_code is None:
#         try:
#             user_obj = CbtUser.objects.get(PR_TOKEN=user_token)
#             return user_obj, True
        
#         except:
#             return "You aren't valid!!", False
#     else:
#         try:
#             user_obj = CbtUser.objects.get(PR_TOKEN=user_token)
#         except:
#             return "You aren't valid!!", False
        
#         try:
#             submenu_obj = CbtSubmenu.objects.get(PR_CODE=submenu_code)
#         except:
#             return "Link isn't valid!!", False
        
#         try:
#             data_obj = CbtSubmenuPermission.objects.get(PR_DESIGNATION=user_obj.PR_DESIGNATION, PR_SUBMENU=submenu_obj, PR_STATUS=1)
#         except:
#             data_obj = None
        
#         if data_obj is not None:
#             return user_obj, True
        
#         return "You haven't permission!!", False

def userPermission(user_token, submenu_code=None):
    user_obj = []
    return user_obj, True

def cbtPagination(page_no:int=0, data_limit:int=0):
    try:
        if data_limit < 10:
            data_limit = 10

        if page_no < 1:
            page_no = 1
        
        start = 0
        end = data_limit
        
        if page_no >= 1:
            for i in range(2, page_no+1):
                start = end
                end = data_limit*i

        dt = {
            'start': start,
            'end': end,
            'data_limit': data_limit
        }
        return dt     
        
    except:
        return None

def cbtPageCount(data_limit:int=0, total_data:int=0):
    
    if total_data <= data_limit:
        page_count = 1
    
    else:
        x = str(total_data/data_limit).split('.')
        page_count = int(x[0])
        if int(x[1]) > 0:
            page_count += 1

    return page_count

def pagination(page):
    try:
        limit = 500
        start = 0
        end = limit

        if page >= 1:
            for i in range(2, page+1):
                start = end
                end = limit*i

            dt = {
                'start': start,
                'end': end
            }
            return dt     
        
        else:
            return None
        
    except:
        return None

def loginDetail(user_obj):
    try:
        subject = "User login details"
        message = f"""
            Dear {user_obj.PR_NAME},
            Your account has been successfully created, use below details to login the account:
            
            Email id: {user_obj.PR_EMAIL},
            Password: {user_obj.PR_PASSWORD_Hint}

            WEBSITE URL: https://learn.gyantantra.org/
        """
        email = user_obj.PR_EMAIL
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)
    
        return True
    
    except:
        return False

def sendOtp(user_obj, otp):
    try:
        subject = "Forget password - "
        message = f"""
            Dear {user_obj.PR_NAME},
            Your OTP is {otp}. Use this otp to change password. Thank you. - Gyan Tantra.
        """
        email = user_obj.PR_EMAIL
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)
    
        return True
    
    except:
        return False

class CbtStudent:
    def __init__(self, user_obj) -> None:
        self.user_obj = user_obj
        self.class_objs = CbtUserClass.objects.filter(PR_USER=self.user_obj, PR_STATUS=1)

    # THIS FUNCTION RETURN TO CLASS OBJECT
    def classObject(self):
        if self.class_objs.exists():
            return  self.class_objs[0].PR_CLASS
        
        return None
    
    # THIS FUNCTION RETURN TO SUBJECT OBJECTS
    def subjectObjects(self):
        
        sub_ids = []
        if self.class_objs.exists():
            
            clsub_objs = CbtClassSubject.objects.filter(PR_CLASS=self.class_objs[0].PR_CLASS)
            for clsub_obj in clsub_objs:
                sub_ids.append(clsub_obj.PR_SUBJECT.PR_SUBJECT_ID)
                
        subject_objs = CbtSubject.objects.filter(PR_SUBJECT_ID__in=sub_ids, PR_STATUS=1)
        
        return subject_objs
    
class CbtUpload:
    
    def __init__(self, file_dir, file_data) -> None:
        self.file_dir = str(file_dir)+str(date.today().isoformat())+"/"
        self.file_data = file_data

        if not os.path.exists(self.file_dir):
            os.makedirs(self.file_dir)
    
    def file(self):
        try:
            fs = FileSystemStorage(location=self.file_dir)
            filename = fs.save(self.file_data.name, self.file_data)
            path = f"{self.file_dir}{filename}"
            
            response_data = {
                'PR_FILE': path
            }
            return True, response_data
        
        except:
            return False, 'Something went wrong !!'
        