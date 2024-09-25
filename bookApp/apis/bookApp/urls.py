from django.urls import path
from . import views

urlpatterns = [

    # ================================= BOOK URL'S =================================

    path('add-book', views.cbtBookViewSet.as_view({'post': 'addUpdateBookData'})),
    path('update-book/<int:PR_BOOK_ID>', views.cbtBookViewSet.as_view({'post': 'addUpdateBookData'})),
    path('book-list', views.cbtBookViewSet.as_view({'post': 'bookList'})),
    path('book-data-list', views.cbtBookViewSet.as_view({'post': 'bookDataList'})),
    
    path('import-book-data', views.cbtBookViewSet.as_view({'post': 'importBookData'})),


    # ================================= CLAS URL'S ==================================

    path('add-class', views.cbtClassViewSet.as_view({'post': 'addUpdateClassData'})),
    path('update-class/<int:PR_CLASS_ID>', views.cbtClassViewSet.as_view({'post': 'addUpdateClassData'})),
    path('class-list', views.cbtClassViewSet.as_view({'post': 'classList'})),
    path('class-data-list', views.cbtClassViewSet.as_view({'post': 'classDataList'})),


    # ================================= BOARD URL'S =================================

    path('add-board', views.cbtBoardViewSet.as_view({'post': 'addUpdateBoardData'})),
    path('update-board/<int:PR_BOARD_ID>', views.cbtBoardViewSet.as_view({'post': 'addUpdateBoardData'})),
    path('board-list', views.cbtBoardViewSet.as_view({'post': 'boardList'})),
    path('board-data-list', views.cbtBoardViewSet.as_view({'post': 'boardDataList'})),

    # ================================= SERIES URL'S =================================

    path('add-series', views.cbtSeriesViewSet.as_view({'post': 'addUpdateSeriesData'})),
    path('update-series/<int:PR_SERIES_ID>', views.cbtSeriesViewSet.as_view({'post': 'addUpdateSeriesData'})),
    path('series-list', views.cbtSeriesViewSet.as_view({'post': 'seriesList'})),
    path('series-data-list', views.cbtSeriesViewSet.as_view({'post': 'seriesDataList'})),


    # ================================= BOOK TYPE URL'S ===============================

    path('add-book-type', views.cbtBookTypeViewSet.as_view({'post': 'addUpdateBookTypeData'})),
    path('update-book-type', views.cbtBookTypeViewSet.as_view({'post': 'addUpdateBookTypeData'})),
    path('book-type-list', views.cbtBookTypeViewSet.as_view({'post': 'bookTypeList'})),
    path('book-type-data-list', views.cbtBookTypeViewSet.as_view({'post': 'bookTypeDataList'})),
  
]