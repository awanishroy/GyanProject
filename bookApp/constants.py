class CbtArrayName:
    Common = 'DATA'
    
class ApiStatus:
    Success='SUCCESS'
    Status="STATUS"
    Exception='EXCAPTION'
    Message='MESSAGE'
    Failure='FAILURE'
    Permission = 'PERMISSION'
    Exist = 'EXIST'
    Pending = 'PENDING'

class CbtMessage:
    Successfully = 'Check-In Successfully!!'
    DataNotFound = 'Data Not Found'
    LoginSuccessMsg = 'Logged in has been successfully!!'
    LoginFailedMsg = "Login credential doesn't exist!!"
    SendSuccessMsg = 'Message has been successfully send!!'
    PermissionMsg = 'You do not have permission!!'
    SubmitSuccessMsg = 'Data has been successfully submited!!'
    UpdateSuccessMsg = 'Data has been successfully updated!!'
    FatchSuccessMsg = 'Data has been fatched successfully!!'
    DeleteSuccessMsg = 'Data has been successfully deleted!!'
    DataNotValid = "Data isn't valid!!"
    MessageFailed = "Message isn't send!!"
    MessageNotValid = "Data isn't valid!!"
    MessageException = 'Something went wrong!!'
    ExistMsg = 'already exist!!'
    UserDetailNotValid = "User details does't Valid!!"
    PendingDayplanMsg = "Please close pending day plan then create new one!!"

    def existMsg(message):
        return message+" "+CbtMessage.ExistMsg
    
    def cbtMsg(message):
        return message
    
    def CbtExceptionMsg(ex):
        return f"Something went wrong. Like - {ex}!!"
    
    def cbtImportMsg(count, total):
        return f"Data has been successfully Uploaded {count} in {total}.!!"
    
class ClickType:
    list = "LIST"
    form = "FORM"
    download = "DOWNLOAD"
    convert = "CONVERT"
    web = "WEB"
    ra = 'RA'

class BtnClickType:
    native = "NATIVE"
    web = "WEB"

class BtnType:
    add = "A"
    view = "V"
    edit = "E"
    delete = "D"


def statusTxt(value):
    if value == 1:
        return 'Active'
    elif value == 0:
        return 'Inactive'
    else:
        return 'Inactive'

def statusCol(value):
    if value == 1:
        return '#3cb371'
    else:
        return '#ff0000'

def dateTime(date_time):
    try:
        x = str(date_time).split('T')
        y = str(x[1]).split('.')
        return str(x[0])+" "+str(y[0])
    except:
        return ''
    



class CBTFlex:
    low = 1
    medium = 2
    normal = 3
    high = 4
    over = 5

class CbtHeader:
    
    def __init__(self, title, value, color:str='', bg_color:str='', flex:int=1, is_click:bool=False, font_size:int=14, align_row:str='LEFT', align:str='LEFT', icon:str='', click_url:str='', click_type_method='POST', request_key='', request_value='', click_type='', btn_click_type=BtnClickType.native, btn_type=BtnType.view):
        self.title = title
        self.value = value
        self.color = color
        self.bg_color = bg_color
        self.flex = flex
        self.is_click = is_click
        self.font_size = font_size
        self.align_row = align_row
        self.align = align
        self.icon = icon
        self.click_url = click_url
        self.click_type_method = click_type_method
        self.request_key = request_key
        self.request_value = request_value
        self.click_type = click_type
        self.btn_click_type = btn_click_type
        self.btn_type = btn_type

    def hRes(self):
        
        data = {
            'TITLE': self.title,
            'VALUE': self.value,
            'COLOR': self.color,
            'BG_COLOR': self.bg_color,
            'FLEX': self.flex,
            'IS_CLICK': self.is_click,
            'ALIGN_ROW': self.align_row,
            'ALIGN': self.align,
            'FONT_SIZE': self.font_size,
            'ICON': self.icon,
            'CLICK_URL': self.click_url,
            'CLICK_TYPE_METHOD': self.click_type_method,
            'REQUEST_KEY': self.request_key,
            'REQUEST_VALUE': self.request_value,
            'CLICK_TYPE': self.click_type,
            'BTN_CLICK_TYPE': self.btn_click_type,
            "BTN_TYPE": self.btn_type
        }
        return data
