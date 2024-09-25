from typing import TypeVar, Generic
from bookApp.constants import *
T = TypeVar('T')
        
class CbtCommonDataRes:
    def __init__(self, value: T, is_header=False) -> T:
        self.value = value
        self.is_header = is_header
        
    def bookDataResponse(self)-> T:
        data = []
        data.append(CbtHeader(title='Id', value=self.value['PR_BOOK_ID'] if self.is_header != True else '').hRes())
        data.append(CbtHeader(title='Name', value=self.value['PR_TITLE'] if self.is_header != True else '').hRes())
        # data.append(CbtHeader(title='Status', value=statusTxt(self.value['PR_STATUS']) if self.is_header != True else '', color=statusCol(self.value['PR_STATUS'])).hRes())
        data.append(CbtHeader(title='Created At', value=dateTime(self.value['PR_CREATED_AT']) if self.is_header != True else '').hRes())
        data.append(CbtHeader(title='  Edit  ', value='BUTTON' if self.is_header != True else '', color='#335EFF', is_click=True, click_url='', request_value=str(self.value['PR_BOOK_ID']), btn_click_type=BtnClickType.web, btn_type=BtnType.edit, flex=0).hRes())
        data.append(CbtHeader(title='  Delete  ', value='BUTTON' if self.is_header != True else '', color='#335EFF', is_click=True, click_url='', request_key='PR_BOOK_ID', request_value=str(self.value['PR_BOOK_ID']), btn_click_type=BtnClickType.native, btn_type=BtnType.delete, flex=0).hRes())
        
        return data
    
    
    def classDataResponse(self)-> T:
        data = []
        data.append(CbtHeader(title='Id', value=self.value['PR_CLASS_ID'] if self.is_header != True else '').hRes())
        data.append(CbtHeader(title='Name', value=self.value['PR_NAME'] if self.is_header != True else '').hRes())
        # data.append(CbtHeader(title='Status', value=statusTxt(self.value['PR_STATUS']) if self.is_header != True else '', color=statusCol(self.value['PR_STATUS'])).hRes())
        data.append(CbtHeader(title='Created At', value=dateTime(self.value['PR_CREATED_AT']) if self.is_header != True else '').hRes())
        data.append(CbtHeader(title='  Edit  ', value='BUTTON' if self.is_header != True else '', color='#335EFF', is_click=True, click_url='', request_value=str(self.value['PR_CLASS_ID']), btn_click_type=BtnClickType.web, btn_type=BtnType.edit, flex=0).hRes())
        data.append(CbtHeader(title='  Delete  ', value='BUTTON' if self.is_header != True else '', color='#335EFF', is_click=True, click_url='', request_key='PR_CLASS_ID', request_value=str(self.value['PR_CLASS_ID']), btn_click_type=BtnClickType.native, btn_type=BtnType.delete, flex=0).hRes())
        
        return data
    
    
    def boardDataResponse(self)-> T:
        data = []
        data.append(CbtHeader(title='Id', value=self.value['PR_BOARD_ID'] if self.is_header != True else '').hRes())
        data.append(CbtHeader(title='Name', value=self.value['PR_NAME'] if self.is_header != True else '').hRes())
        # data.append(CbtHeader(title='Status', value=statusTxt(self.value['PR_STATUS']) if self.is_header != True else '', color=statusCol(self.value['PR_STATUS'])).hRes())
        data.append(CbtHeader(title='Created At', value=dateTime(self.value['PR_CREATED_AT']) if self.is_header != True else '').hRes())
        data.append(CbtHeader(title='  Edit  ', value='BUTTON' if self.is_header != True else '', color='#335EFF', is_click=True, click_url='', request_value=str(self.value['PR_BOARD_ID']), btn_click_type=BtnClickType.web, btn_type=BtnType.edit, flex=0).hRes())
        data.append(CbtHeader(title='  Delete  ', value='BUTTON' if self.is_header != True else '', color='#335EFF', is_click=True, click_url='', request_key='PR_BOARD_ID', request_value=str(self.value['PR_BOARD_ID']), btn_click_type=BtnClickType.native, btn_type=BtnType.delete, flex=0).hRes())
        
        return data
    
    
    def seriesDataResponse(self)-> T:
        data = []
        data.append(CbtHeader(title='Id', value=self.value['PR_SERIES_ID'] if self.is_header != True else '').hRes())
        data.append(CbtHeader(title='Name', value=self.value['PR_NAME'] if self.is_header != True else '').hRes())
        # data.append(CbtHeader(title='Status', value=statusTxt(self.value['PR_STATUS']) if self.is_header != True else '', color=statusCol(self.value['PR_STATUS'])).hRes())
        data.append(CbtHeader(title='Created At', value=dateTime(self.value['PR_CREATED_AT']) if self.is_header != True else '').hRes())
        data.append(CbtHeader(title='  Edit  ', value='BUTTON' if self.is_header != True else '', color='#335EFF', is_click=True, click_url='', request_value=str(self.value['PR_SERIES_ID']), btn_click_type=BtnClickType.web, btn_type=BtnType.edit, flex=0).hRes())
        data.append(CbtHeader(title='  Delete  ', value='BUTTON' if self.is_header != True else '', color='#335EFF', is_click=True, click_url='', request_key='PR_SERIES_ID', request_value=str(self.value['PR_SERIES_ID']), btn_click_type=BtnClickType.native, btn_type=BtnType.delete, flex=0).hRes())
        
        return data
    
    
    def bookTypeDataResponse(self)-> T:
        data = []
        data.append(CbtHeader(title='Id', value=self.value['PR_BOOK_TYPE_ID'] if self.is_header != True else '').hRes())
        data.append(CbtHeader(title='Name', value=self.value['PR_NAME'] if self.is_header != True else '').hRes())
        # data.append(CbtHeader(title='Status', value=statusTxt(self.value['PR_STATUS']) if self.is_header != True else '', color=statusCol(self.value['PR_STATUS'])).hRes())
        data.append(CbtHeader(title='Created At', value=dateTime(self.value['PR_CREATED_AT']) if self.is_header != True else '').hRes())
        data.append(CbtHeader(title='  Edit  ', value='BUTTON' if self.is_header != True else '', color='#335EFF', is_click=True, click_url='', request_value=str(self.value['PR_BOOK_TYPE_ID']), btn_click_type=BtnClickType.web, btn_type=BtnType.edit, flex=0).hRes())
        data.append(CbtHeader(title='  Delete  ', value='BUTTON' if self.is_header != True else '', color='#335EFF', is_click=True, click_url='', request_key='PR_BOOK_TYPE_ID', request_value=str(self.value['PR_BOOK_TYPE_ID']), btn_click_type=BtnClickType.native, btn_type=BtnType.delete, flex=0).hRes())
        
        return data
    
    