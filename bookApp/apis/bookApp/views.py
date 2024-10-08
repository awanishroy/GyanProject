from rest_framework import viewsets
from bookApp.response.cbt_api_response import *
from bookApp.helpers import *
from . helpers import *
from . serializers import *
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from django.http import HttpResponse


def index(self):
    return HttpResponse("Hello, you are lost.")

# ================================= BOOK VIEW SET =================================

class cbtBookViewSet(viewsets.ModelViewSet):
    
    # ========================== ADD OR UPDATE BOOK DATA ==========================
    def addUpdateBookData(self, request , PR_BOOK_ID = None):
        try:
            data = request.data
            msg, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                if PR_BOOK_ID is not None:
                    try:
                        instance = CbtBookData.objects.get(PR_BOOK_ID=PR_BOOK_ID)
                        serializer = CbtBookDataSerializer(instance, data=data, partial=True)
                    except ObjectDoesNotExist:
                        return CbtDataResponse([], ApiStatus.Failure, CbtMessage.DataNotFound).cbtResponse()
                else:
                    serializer = CbtBookDataSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return CbtDataResponse(serializer.data, ApiStatus.Success ,CbtMessage.SubmitSuccessMsg).cbtResponse()
                return CbtDataResponse(serializer.errors, ApiStatus.Failure, CbtMessage.DataNotValid).cbtResponse()
            
            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(msg)).cbtResponse()

        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()   

    # ============================ UPLOAD CSV BOOK DATA ===========================
    def importBookData(self, request):  
        try:
            data = request.data
            msg, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                file = request.FILES.get('PR_FILE')
                if not file:
                    return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg("Please Excel Upload File")).cbtResponse()

                df = pd.read_excel(file)
                
                df.fillna({
                    'Title': '','Sub Title': '','ISBN': '','Board Id':'','Class Id':'','Series Id':'','BookType Id': '','Subject Id':'' ,'Imprint':'','Author':'','Edition':'','Company': '','Book Code': '', 
                    'Copyright': '','Date Of Release': pd.NaT,'Binding': '','Language': '','Pages': 0,'TrimSize': '','Weight': 0.0,'List Price': 0.0,'Discount': 0.0,'BookNumber': 0, 
                    'ClassLevel': '','ProductDivision': '','BroadSubject': '','Detailed Subject': '','ProductDescription': ''}, inplace=True)

                book_objects = []
                for index, row in df.iterrows():
                    book = CbtBookData(
                        PR_TITLE=row['Title'],
                        PR_SUB_TITLE=row['Sub Title'],
                        PR_ISBN=row['ISBN'],
                        PR_BOARD_id=row['Board Id'],
                        PR_CLASS_id=row['Class Id'],
                        PR_SERIES_id=row['Series Id'],
                        PR_BOOK_TYPE_id=row['BookType Id'], 
                        PR_SUBJECT_id=row['Subject Id'], 
                        PR_IMPRINT=row['Imprint'],
                        PR_AUTHOR=row['Author'],
                        PR_EDITION=row['Edition'],
                        PR_COMPANY=row['Company'],
                        PR_BOOK_CODE=row['Book Code'],
                        PR_COPYRIGHT=row['Copyright'],
                        PR_DATE_OF_RELEASE=pd.to_datetime(row['Date Of Release']).date() if pd.notna(row['Date Of Release']) else None,
                        PR_BINDING=row['Binding'],
                        PR_LANGUAGE=row['Language'],
                        PR_PAGES=int(row['Pages']) if pd.notnull(row['Pages']) else None,
                        PR_TRIM_SIZE=row['TrimSize'],
                        PR_WEIGHT=float(row['Weight']) if pd.notnull(row['Weight']) else None,
                        PR_LIST_PRICE=float(row['List Price']) if pd.notnull(row['List Price']) else None,
                        PR_DISCOUNT=float(row['Discount']) if pd.notnull(row['Discount']) else None,
                        PR_BOOK_NUMBER=int(row['BookNumber']) if pd.notnull(row['BookNumber']) else None,
                        PR_CLASS_LEVEL=row['ClassLevel'],
                        PR_PRODUCT_DIVISION=row['ProductDivision'],
                        PR_BROAD_SUBJECT=row['BroadSubject'],
                        PR_DETAILED_SUBJECT=row['Detailed Subject'],
                        PR_PRODUCT_DESCRIPTION=row['ProductDescription'],
                    )
                    book_objects.append(book)

                CbtBookData.objects.bulk_create(book_objects)

                return CbtDataResponse([], ApiStatus.Success ,CbtMessage.SubmitSuccessMsg).cbtResponse()
            
            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(msg)).cbtResponse()
        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()  
        
    # ================================ BOOK LIST DATA ===============================
    def bookList(self, request):
        try:            
            data = request.data

            user_data, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                
                if data.get('PR_BOOK_ID') is not None:
                    data_obj = CbtBookData.objects.get(PR_BOOK_ID=data.get('PR_BOOK_ID'))
                    serializer = CbtBookDataListSerializer(data_obj)
                
                else:
                    data_objs = CbtBookData.objects.get()
                    serializer = CbtBookDataListSerializer(data_objs, many=True)

                return CbtDataResponse(serializer.data, ApiStatus.Success).cbtResponse()
                
            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(user_data)).cbtResponse()
            
        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse() 

    # ============================= BOOK DATA LIST DATA =============================
    def bookDataList(self,request):
        try:
            request_data = request.data
            data = request_data.get('CBT_REQUEST_DATA')
            
            msg, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                
                total_data = 0
                pgn = cbtPagination(int(data.get('PR_PAGE_NO')), int(data.get('PR_DATA_LIMIT')))
                if pgn is None:
                    return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg("Page number and data limit must be required !!")).cbtResponse()
                
                if data.get('PR_QUERY') != '':
                    data_objs = CbtFliterData(data.get('PR_QUERY')).bookFilter()
                    total_data = data_objs.count()
                
                else: 
                    data_objs = CbtBookData.objects.all().order_by('-PR_BOOK_ID')[pgn['start']:pgn['end']]
                    total_data = CbtBookData.objects.all().count()

                
                serializer = CbtBookDataListSerializer(data_objs, many=True)
                page_count = cbtPageCount(data_limit=pgn['data_limit'], total_data=total_data)
                
                return CbtDataListResponse(serializer.data, ApiStatus.Success, pageCount=page_count, apiType='CBT_BOOK_DATA').cbtResponse()
            
            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(msg)).cbtResponse()

        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()

    def fetchBookData(self, request):
        try:
            data = request.data
            msg, isValid = userPermission(data.get('PR_TOKEN'))

            if isValid:
                # Get all boards
                board_obj = CbtBoard.objects.all()

                result_data = []
                for board in board_obj:
                    series_data = []

                    # Get all series related to this board
                    series_obj = CbtSeries.objects.filter(PR_BOARD=board)

                    for series in series_obj:
                        classes_data = []

                        # Get all classes related to this series
                        classes_obj = CbtSeriesClass.objects.filter(PR_SERIES=series)

                        for class_relation in classes_obj:
                            cbt_class = class_relation.PR_CLASS
                            subjects_data = []

                            # Get all subjects related to this class
                            subjects_obj = CbtClassSubject.objects.filter(PR_CLASS=cbt_class)

                            for subject_relation in subjects_obj:
                                subject = subject_relation.PR_SUBJECT

                                # Get all books related to this subject and class
                                books_data = CbtBookData.objects.filter(
                                    PR_SUBJECT=subject,
                                    PR_CLASS=cbt_class,
                                    PR_BOARD=board,      # Assuming books may also relate to board
                                    PR_SERIES=series     # Assuming books may also relate to series
                                )

                                # Create a dictionary to group books by type
                                books_by_type = {}
                                for book in books_data:
                                    book_type_id = book.PR_BOOK_TYPE.PR_BOOK_TYPE_ID if book.PR_BOOK_TYPE else None
                                    book_type_name = book.PR_BOOK_TYPE.PR_NAME if book.PR_BOOK_TYPE else "Unknown"

                                    if book_type_id not in books_by_type:
                                        books_by_type[book_type_id] = {
                                            "PR_BOOK_TYPE_ID": book_type_id,
                                            "PR_BOOK_TYPE_NAME": book_type_name,
                                            "PR_BOOKS": []
                                        }

                                    # Append book data to the respective book type
                                    books_by_type[book_type_id]["PR_BOOKS"].append({
                                        "PR_BOOK_ID": book.PR_BOOK_ID,
                                        "PR_TITLE": book.PR_TITLE,
                                        "PR_SERIES": book.PR_SERIES_id,
                                        "PR_BOARD": book.PR_BOARD_id,
                                        "PR_CLASS": book.PR_CLASS_id,
                                        "PR_SUBJECT": book.PR_SUBJECT_id,
                                        "PR_AUTHOR": book.PR_AUTHOR,
                                        "PR_ISBN": book.PR_ISBN,
                                        # Add more fields as needed
                                    })

                                # Convert the dictionary to a list for subjects_data
                                subject_books_data = [{"PR_BOOK_TYPE": book_type["PR_BOOK_TYPE_NAME"], "PR_BOOKS": book_type["PR_BOOKS"]}
                                                    for book_type in books_by_type.values()]

                                # Create subject data
                                subjects_data.append({
                                    "PR_SUBJECT_ID": subject.PR_SUBJECT_ID,
                                    "PR_SUBJECT_NAME": subject.PR_NAME,
                                    "PR_BOOK_TYPE": subject_books_data  # Add grouped books by type here
                                })

                            # Append the class data
                            classes_data.append({
                                "PR_CLASS_ID": cbt_class.PR_CLASS_ID,
                                "PR_CLASS_NAME": cbt_class.PR_NAME,
                                "PR_SUBJECTS": subjects_data,  # Add subjects with books here
                            })

                        # Append the series data
                        series_data.append({
                            "PR_SERIES_ID": series.PR_SERIES_ID,
                            "PR_NAME": series.PR_NAME,
                            "PR_CLASSES": classes_data  # Add all related classes here
                        })

                    # Append the board data
                    board_data = {
                        "PR_BOARD_ID": board.PR_BOARD_ID,
                        "PR_NAME": board.PR_NAME,
                        "PR_SERIES": series_data
                    }

                    result_data.append(board_data)

                # Return the response with board, series, class, subject, and book data
                return CbtDataResponse(result_data, ApiStatus.Success, CbtMessage.FatchSuccessMsg).cbtResponse()

            else:
                return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(msg)).cbtResponse()

        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(str(ex))).cbtResponse()

# ================================= CLASS VIEW SET =================================

class cbtClassViewSet(viewsets.ModelViewSet):

    # ========================== ADD OR UPDATE CLASS DATA ==========================
    def addUpdateClassData(self, request , PR_CLASS_ID = None):
        try:
            data = request.data
            msg, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                if PR_CLASS_ID != None:
                    try:
                        instance = CbtClasses.objects.get(PR_CLASS_ID=PR_CLASS_ID)
                        serializer = CbtClassesSerializer(instance, data=data, partial=True)
                    except ObjectDoesNotExist:
                        return CbtDataResponse([], ApiStatus.Failure, CbtMessage.DataNotFound).cbtResponse()
                else:
                    serializer = CbtClassesSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()
                    return CbtDataResponse(serializer.data, ApiStatus.Success ,CbtMessage.SubmitSuccessMsg).cbtResponse()
                return CbtDataResponse(serializer.errors, ApiStatus.Failure, CbtMessage.DataNotValid).cbtResponse()
            
            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(msg)).cbtResponse()
        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()   
    
    # ============================ CLASS LIST DATA ==================================
    def classList(self, request):
        try:
            data = request.data
            user_data, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                if data.get('PR_CLASS_ID') is not None:
                    data_obj = CbtClasses.objects.get(PR_CLASS_ID=data.get('PR_CLASS_ID'))
                    serializer = CbtClassesSerializer(data_obj)
                else:
                    data_objs = CbtClasses.objects.all()
                    serializer = CbtClassesSerializer(data_objs, many=True)

                return CbtDataResponse(serializer.data, ApiStatus.Success).cbtResponse()

            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(user_data)).cbtResponse()

        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()

    # ============================= CLASS DATA LIST DATA ============================
    def classDataList(self, request):
        try:
            request_data = request.data
            data = request_data.get('CBT_REQUEST_DATA')
            msg, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                total_data = 0
                pgn = cbtPagination(int(data.get('PR_PAGE_NO')), int(data.get('PR_DATA_LIMIT')))
                if pgn is None:
                    return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg("Page number and data limit must be required !!")).cbtResponse()

                if data.get('PR_QUERY'):
                    data_objs = CbtFliterData(data.get('PR_QUERY')).classFilter()  # Assume there's a filter for classes
                    total_data = data_objs.count()
                else:
                    data_objs = CbtClasses.objects.all().order_by('-PR_CLASS_ID')[pgn['start']:pgn['end']]
                    total_data = CbtClasses.objects.all().count()

                serializer = CbtClassesSerializer(data_objs, many=True)
                page_count = cbtPageCount(data_limit=pgn['data_limit'], total_data=total_data)

                return CbtDataListResponse(serializer.data, ApiStatus.Success, pageCount=page_count, apiType='CBT_CLASS_DATA').cbtResponse()

            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(msg)).cbtResponse()

        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()


# ================================= SUBJECT VIEW SET ================================

class cbtSubjectViewSet(viewsets.ModelViewSet):

    # ========================== ADD OR UPDATE SUBJECT DATA =========================
    def addUpdateSubjectData(self, request , PR_SUBJECT_ID = None):
        try:
            data = request.data
            msg, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                if PR_SUBJECT_ID != None:
                    try:
                        instance = CbtSubject.objects.get(PR_SUBJECT_ID=PR_SUBJECT_ID)
                        serializer = CbtSubjectSerializer(instance, data=data, partial=True)
                    except ObjectDoesNotExist:
                        return CbtDataResponse([], ApiStatus.Failure, CbtMessage.DataNotFound).cbtResponse()
                else:
                    serializer = CbtSubjectSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()
                    return CbtDataResponse(serializer.data, ApiStatus.Success ,CbtMessage.SubmitSuccessMsg).cbtResponse()
                return CbtDataResponse(serializer.errors, ApiStatus.Failure, CbtMessage.DataNotValid).cbtResponse()
            
            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(msg)).cbtResponse()
        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()   
    
    # ============================ SUBJECT LIST DATA ===============================
    def subjectList(self, request):
        try:
            data = request.data
            user_data, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                if data.get('PR_SUBJECT_ID') is not None:
                    data_obj = CbtSubject.objects.get(PR_SUBJECT_ID=data.get('PR_SUBJECT_ID'))
                    serializer = CbtSubjectSerializer(data_obj)
                else:
                    data_objs = CbtSubject.objects.all()
                    serializer = CbtSubjectSerializer(data_objs, many=True)

                return CbtDataResponse(serializer.data, ApiStatus.Success).cbtResponse()

            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(user_data)).cbtResponse()

        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()

    # ============================= SUBJECT DATA LIST DATA ===========================
    def subjectDataList(self, request):
        try:
            request_data = request.data
            data = request_data.get('CBT_REQUEST_DATA')
            msg, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                total_data = 0
                pgn = cbtPagination(int(data.get('PR_PAGE_NO')), int(data.get('PR_DATA_LIMIT')))
                if pgn is None:
                    return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg("Page number and data limit must be required !!")).cbtResponse()

                if data.get('PR_QUERY'):
                    data_objs = CbtFliterData(data.get('PR_QUERY')).subjectFilter()
                    total_data = data_objs.count()
                else:
                    data_objs = CbtSubject.objects.all().order_by('-PR_SUBJECT_ID')[pgn['start']:pgn['end']]
                    total_data = CbtSubject.objects.all().count()

                serializer = CbtSubjectSerializer(data_objs, many=True)
                page_count = cbtPageCount(data_limit=pgn['data_limit'], total_data=total_data)

                return CbtDataListResponse(serializer.data, ApiStatus.Success, pageCount=page_count, apiType='CBT_SUBJECT_DATA').cbtResponse()

            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(msg)).cbtResponse()

        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()


# ================================= BOARD VIEW SET ================================

class cbtBoardViewSet(viewsets.ModelViewSet):
    
    # ========================== ADD OR UPDATE BOARD DATA =========================
    def addUpdateBoardData(self,request , PR_BOARD_ID = None):
        try:
            data = request.data
            msg, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                if PR_BOARD_ID != None:
                    try:
                        instance = CbtBoard.objects.get(PR_BOARD_ID=PR_BOARD_ID)
                        serializer = CbtBoardSerializer(instance, data=data, partial=True)
                    except ObjectDoesNotExist:
                        return CbtDataResponse([], ApiStatus.Failure, CbtMessage.DataNotFound).cbtResponse()
                else:
                    serializer = CbtBoardSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()
                    return CbtDataResponse(serializer.data, ApiStatus.Success ,CbtMessage.SubmitSuccessMsg).cbtResponse()
                return CbtDataResponse(serializer.errors, ApiStatus.Failure, CbtMessage.DataNotValid).cbtResponse()
            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(msg)).cbtResponse()
        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()   
    
    # ============================ BOARD LIST DATA ================================
    def boardList(self, request):
        try:
            data = request.data
            user_data, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                if data.get('PR_BOARD_ID') is not None:
                    data_obj = CbtBoard.objects.get(PR_BOARD_ID=data.get('PR_BOARD_ID'))
                    serializer = CbtBoardSerializer(data_obj)
                else:
                    data_objs = CbtBoard.objects.all()
                    serializer = CbtBoardSerializer(data_objs, many=True)

                return CbtDataResponse(serializer.data, ApiStatus.Success).cbtResponse()

            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(user_data)).cbtResponse()

        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()

    # ============================= BOARD DATA LIST DATA ===========================
    def boardDataList(self, request):
        try:
            request_data = request.data
            data = request_data.get('CBT_REQUEST_DATA')
            msg, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                total_data = 0
                pgn = cbtPagination(int(data.get('PR_PAGE_NO')), int(data.get('PR_DATA_LIMIT')))
                if pgn is None:
                    return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg("Page number and data limit must be required !!")).cbtResponse()

                if data.get('PR_QUERY'):
                    data_objs = CbtFliterData(data.get('PR_QUERY')).boardFilter()  # Assume there's a filter for boards
                    total_data = data_objs.count()
                else:
                    data_objs = CbtBoard.objects.all().order_by('-PR_BOARD_ID')[pgn['start']:pgn['end']]
                    total_data = CbtBoard.objects.all().count()

                serializer = CbtBoardSerializer(data_objs, many=True)
                page_count = cbtPageCount(data_limit=pgn['data_limit'], total_data=total_data)

                return CbtDataListResponse(serializer.data, ApiStatus.Success, pageCount=page_count, apiType='CBT_BOARD_DATA').cbtResponse()

            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(msg)).cbtResponse()

        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()

# ================================= SERIES VIEW SET ================================

class cbtSeriesViewSet(viewsets.ModelViewSet):

    # ========================== ADD OR UPDATE SERIES DATA =========================
    def addUpdateSeriesData(self, request, PR_SERIES_ID=None):
        try:
            data = request.data
            msg, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:

                if PR_SERIES_ID is not None:
                    try:
                        instance = CbtSeries.objects.get(PR_SERIES_ID=PR_SERIES_ID)
                        serializer = CbtSeriesSerializer(instance, data=data, partial=True)
                    except ObjectDoesNotExist:
                        return CbtDataResponse([], ApiStatus.Failure, CbtMessage.DataNotFound).cbtResponse()
                else:
                    serializer = CbtSeriesSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()
                    if PR_SERIES_ID is not None:
                        return CbtDataResponse(serializer.data, ApiStatus.Success ,CbtMessage.SubmitSuccessMsg).cbtResponse()
                    else:
                        return CbtDataResponse(serializer.data, ApiStatus.Success ,CbtMessage.SubmitSuccessMsg).cbtResponse()
                else:
                    return CbtDataResponse(serializer.errors, ApiStatus.Failure, CbtMessage.DataNotValid).cbtResponse()
        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()   

    # ============================ SERIES LIST DATA ================================
    def seriesList(self, request):
        try:
            data = request.data
            user_data, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                if data.get('PR_SERIES_ID') is not None:
                    data_obj = CbtSeries.objects.get(PR_SERIES_ID=data.get('PR_SERIES_ID'))
                    serializer = CbtSeriesDataListSerializer(data_obj)
                else:
                    data_objs = CbtSeries.objects.all()
                    serializer = CbtSeriesDataListSerializer(data_objs, many=True)

                return CbtDataResponse(serializer.data, ApiStatus.Success).cbtResponse()

            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(user_data)).cbtResponse()

        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()

    # ============================= SERIES DATA LIST DATA ===========================
    def seriesDataList(self, request):
        try:
            request_data = request.data
            data = request_data.get('CBT_REQUEST_DATA')
            msg, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                total_data = 0
                pgn = cbtPagination(int(data.get('PR_PAGE_NO')), int(data.get('PR_DATA_LIMIT')))
                if pgn is None:
                    return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg("Page number and data limit must be required !!")).cbtResponse()

                if data.get('PR_QUERY'):
                    data_objs = CbtFliterData(data.get('PR_QUERY')).seriesFilter()  # Assume there's a filter for series
                    total_data = data_objs.count()
                else:
                    data_objs = CbtSeries.objects.all().order_by('-PR_SERIES_ID')[pgn['start']:pgn['end']]
                    total_data = CbtSeries.objects.all().count()

                serializer = CbtSeriesDataListSerializer(data_objs, many=True)
                page_count = cbtPageCount(data_limit=pgn['data_limit'], total_data=total_data)

                return CbtDataListResponse(serializer.data, ApiStatus.Success, pageCount=page_count, apiType='CBT_SERIES_DATA').cbtResponse()

            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(msg)).cbtResponse()

        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()

# ================================= BOOK TYPE VIEW SET ==============================

class cbtBookTypeViewSet(viewsets.ModelViewSet):

    # ========================= ADD OR UPDATE BOOK TYPE DATA ========================
    def addUpdateBookTypeData(self,request,PR_BOOK_TYPE_ID = None):
        try:
            data = request.data
            msg, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                if PR_BOOK_TYPE_ID != None:
                    try:
                        instance = CbtBookType.objects.get(PR_BOOK_TYPE_ID=PR_BOOK_TYPE_ID)
                        serializer = CbtBookTypeSerializer(instance, data=data, partial=True)
                    except ObjectDoesNotExist:
                        return CbtDataResponse([], ApiStatus.Failure, CbtMessage.DataNotFound).cbtResponse()
                else:
                    serializer = CbtBookTypeSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()
                    return CbtDataResponse(serializer.data, ApiStatus.Success ,CbtMessage.SubmitSuccessMsg).cbtResponse()
                return CbtDataResponse(serializer.errors, ApiStatus.Failure, CbtMessage.DataNotValid).cbtResponse()
            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(msg)).cbtResponse()
        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()   
    
    # ============================ BOOK TYPE LIST DATA ===============================
    def bookTypeList(self, request):
        try:
            data = request.data
            user_data, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                data_objs = CbtBookType.objects.all()
                serializer = CbtBookTypeSerializer(data_objs, many=True)

                return CbtDataResponse(serializer.data, ApiStatus.Success).cbtResponse()

            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(user_data)).cbtResponse()

        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbtResponse()

    # ============================= BOOK TYPE DATA LIST DATA =========================
    def bookTypeDataList(self, request):
        try:
            request_data = request.data
            data = request_data.get('CBT_REQUEST_DATA')
            msg, isValid = userPermission(data.get('PR_TOKEN'))
            if isValid:
                total_data = 0
                pgn = cbtPagination(int(data.get('PR_PAGE_NO')), int(data.get('PR_DATA_LIMIT')))
                if pgn is None:
                    return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg("Page number and data limit must be required !!")).cbtResponse()

                if data.get('PR_QUERY'):
                    data_objs = CbtFliterData(data.get('PR_QUERY')).bookTypeFilter()  # Assume there's a filter for book types
                    total_data = data_objs.count()
                else:
                    data_objs = CbtBookType.objects.all().order_by('-PR_BOOK_TYPE_ID')[pgn['start']:pgn['end']]
                    total_data = CbtBookType.objects.all().count()

                serializer = CbtBookTypeSerializer(data_objs, many=True)
                page_count = cbtPageCount(data_limit=pgn['data_limit'], total_data=total_data)

                return CbtDataListResponse(serializer.data, ApiStatus.Success, pageCount=page_count, apiType='CBT_BOOK_TYPE_DATA').cbtResponse()

            return CbtDataResponse([], ApiStatus.Failure, CbtMessage.cbtMsg(msg)).cbtResponse()

        except Exception as ex:
            return CbtDataResponse([], ApiStatus.Exception, CbtMessage.CbtExceptionMsg(ex)).cbResponse()

            