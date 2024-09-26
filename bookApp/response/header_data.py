from typing import TypeVar, Generic
T = TypeVar('T')
from bookApp.apis.bookApp.common_data import CbtCommonDataRes

class IListH:
    def __init__(self, value: T, apiType:str='') -> T:
        self.value = value
        self.apiType = apiType

    def listResH(self) -> T:
            
        original_list = []

        if len(self.value) == 0:
            original_list = []
        
        elif self.apiType == 'CBT_BOOK_DATA':
            original_list.append(CbtCommonDataRes(self.value[0], is_header=True).bookDataResponse())

        elif self.apiType == 'CBT_CLASS_DATA':
            original_list.append(CbtCommonDataRes(self.value[0], is_header=True).classDataResponse())

        elif self.apiType == 'CBT_BOARD_DATA':
            original_list.append(CbtCommonDataRes(self.value[0], is_header=True).boardDataResponse())
        
        elif self.apiType == 'CBT_SERIES_DATA':
            original_list.append(CbtCommonDataRes(self.value[0], is_header=True).seriesDataResponse())
        
        elif self.apiType == 'CBT_BOOK_TYPE_DATA':
            original_list.append(CbtCommonDataRes(self.value[0], is_header=True).bookTypeDataResponse())

        elif self.apiType == 'PR_SUBJECT_ID':
            original_list.append(CbtCommonDataRes(self.value[0], is_header=True).subjectDataResponse())
        
        return original_list
