from django.http import JsonResponse
from typing import TypeVar, Generic
from bookApp.constants import *
T = TypeVar('T')
from .header_data import *
from . item_data import *

# DATA API RESPONSE CLASS HERE
class CbtDataResponse(Generic[T]):
    
    def __init__(self, value: T, status: str, message:str=CbtMessage.SendSuccessMsg, arrayName:str=CbtArrayName.Common) -> None:
        self.status = status
        self.value = value
        self.arrayName = arrayName
        self.message = message

    def cbtResponse(self)->JsonResponse :

        if self.status == ApiStatus.Success:
            data = {
                ApiStatus.Status: ApiStatus.Success,
                ApiStatus.Message: self.message,
                self.arrayName: self.value
            }
            return JsonResponse(data)

        elif self.status == ApiStatus.Exception:
            data = {
                ApiStatus.Status: ApiStatus.Exception,
                ApiStatus.Message: self.message,
                self.arrayName: []
            }
            return JsonResponse(data)
    
        else :
            data = {
                ApiStatus.Status: ApiStatus.Failure,
                ApiStatus.Message: self.message,
                self.arrayName: self.value
            }
            return JsonResponse(data)

#  DATA LIST RESPONSE CLASS HERE
class CbtDataListResponse(Generic[T]):
    
    def __init__(self, value: T, status: str, message:str=CbtMessage.SendSuccessMsg, pageCount:int=0, arrayName:str=CbtArrayName.Common, apiType:str='') -> None:
        self.status = status
        self.value = value
        self.arrayName = arrayName
        self.message = message
        self.pageCount = pageCount
        self.apiType = apiType

    def cbtResponse(self)->JsonResponse :
        
        if self.status == ApiStatus.Success:
            data = {
                ApiStatus.Status: ApiStatus.Success,
                ApiStatus.Message: self.message,
                'PAGE_COUNT': self.pageCount,
                self.arrayName: CbtData(self.value, apiType=self.apiType).cbtResData()
            }
            return JsonResponse(data)

        elif self.status == ApiStatus.Exception:
            data={
                ApiStatus.Status: ApiStatus.Exception,
                ApiStatus.Message: self.message,
                self.arrayName: []
            }
            return JsonResponse(data)
   
        else :
            data={
                ApiStatus.Status: ApiStatus.Failure,
                ApiStatus.Message: self.message,
                self.arrayName: self.value
            }
            return JsonResponse(data)

class CbtData(Generic[T]):
    
    def __init__(self, value: T, apiType:str='') -> T:
        self.value = value
        self.apiType = apiType

    def cbtResData(self) -> T:
        return {
            'ITEM_DATA': IListRes(self.value, apiType=self.apiType).listRes(),
            'LIST_HEADER': IListH(self.value, apiType=self.apiType).listResH(),
            'IS_HEADER': False,
        }
    
class IListRes:
    
    def __init__(self, value: T, apiType:str='') -> T:
        self.value = value
        self.apiType = apiType

    def listRes(self) -> T:            
        original_list = []

        for i in self.value:
            original_list.append(ItemData(i, apiType=self.apiType).itemRes())

        return original_list



