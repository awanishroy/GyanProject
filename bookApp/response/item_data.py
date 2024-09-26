from typing import TypeVar, Generic
T = TypeVar('T')
from bookApp.apis.bookApp.common_data import CbtCommonDataRes

class ItemData(Generic[T]):
    
    def __init__(self, value: T, apiType:str=''):
        self.value = value
        self.apiType = apiType
    
    def itemRes(self, generic_value='')-> T:
        
        if self.apiType == 'CBT_BOOK_DATA':
            data = {
                'ID': self.value['PR_BOOK_ID'],
                'TITLE': self.value['PR_TITLE'],
                'IMAGE': '',
                'SUBTITLE': '',
                'SELECTED': False,
                'IS_EXPANDED': False,
                'ORIGINAL_DATA': self.value,
                'ROW_DATA': CbtCommonDataRes(value=self.value).bookDataResponse(),
                'EXPANDABLE_DATA': [],
                'BG_COLOR': '',
            }            
            return data
        
       
        if self.apiType == 'CBT_BOARD_DATA':
            data = {
                'ID': self.value['PR_BOARD_ID'],
                'TITLE': self.value['PR_NAME'],
                'IMAGE': '',
                'SUBTITLE': '',
                'SELECTED': False,
                'IS_EXPANDED': False,
                'ORIGINAL_DATA': self.value,
                'ROW_DATA': CbtCommonDataRes(value=self.value).boardDataResponse(),
                'EXPANDABLE_DATA': [],
                'BG_COLOR': '',
            }            
            return data
        
       
        if self.apiType == 'CBT_SERIES_DATA':
            data = {
                'ID': self.value['PR_SERIES_ID'],
                'TITLE': self.value['PR_NAME'],
                'IMAGE': '',
                'SUBTITLE': '',
                'SELECTED': False,
                'IS_EXPANDED': False,
                'ORIGINAL_DATA': self.value,
                'ROW_DATA': CbtCommonDataRes(value=self.value).seriesDataResponse(),
                'EXPANDABLE_DATA': [],
                'BG_COLOR': '',
            }            
            return data
        
       
        if self.apiType == 'CBT_BOOK_TYPE_DATA':
            data = {
                'ID': self.value['PR_BOOK_TYPE_ID'],
                'TITLE': self.value['PR_NAME'],
                'IMAGE': '',
                'SUBTITLE': '',
                'SELECTED': False,
                'IS_EXPANDED': False,
                'ORIGINAL_DATA': self.value,
                'ROW_DATA': CbtCommonDataRes(value=self.value).bookTypeDataResponse(),
                'EXPANDABLE_DATA': [],
                'BG_COLOR': '',
            }            
            return data
        
       
        if self.apiType == 'CBT_CLASS_DATA':
            data = {
                'ID': self.value['PR_CLASS_ID'],
                'TITLE': self.value['PR_NAME'],
                'IMAGE': '',
                'SUBTITLE': '',
                'SELECTED': False,
                'IS_EXPANDED': False,
                'ORIGINAL_DATA': self.value,
                'ROW_DATA': CbtCommonDataRes(value=self.value).classDataResponse(),
                'EXPANDABLE_DATA': [],
                'BG_COLOR': '',
            }            
            return data
        
        if self.apiType == 'PR_SUBJECT_ID':
            data = {
                'ID': self.value['PR_SUBJECT_ID'],
                'TITLE': self.value['PR_NAME'],
                'IMAGE': '',
                'SUBTITLE': '',
                'SELECTED': False,
                'IS_EXPANDED': False,
                'ORIGINAL_DATA': self.value,
                'ROW_DATA': CbtCommonDataRes(value=self.value).subjectDataResponse(),
                'EXPANDABLE_DATA': [],
                'BG_COLOR': '',
            }            
            return data
        
       