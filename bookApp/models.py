from django.db import models

# Subject Model
class CbtSubject(models.Model):
    PR_SUBJECT_ID = models.AutoField(primary_key=True)
    PR_NAME = models.CharField(max_length=100)
    PR_IMAGE = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_DESCRIPTION = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_STATUS = models.IntegerField(null=True, blank=True, default=0)
    PR_IMAGE = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cbt_subject'

# Class Level Model
class CbtClasses(models.Model):
    PR_CLASS_ID = models.AutoField(primary_key=True)
    PR_NAME = models.CharField(max_length=100, default='')
    PR_SUBJECT = models.ManyToManyField(CbtSubject, through='CbtClassSubject', related_name='pr_classes')
    PR_IMAGE = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_DESCRIPTION = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_STATUS = models.IntegerField(null=True, blank=True, default=0)
    PR_CREATED_AT = models.DateTimeField(auto_now_add=True)
    PR_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cbt_classes'

# Pivot Table (CbtClassSubject)
class CbtClassSubject(models.Model):
    PR_CLASS_SUBJECT_ID = models.AutoField(primary_key=True)
    PR_SUBJECT = models.ForeignKey(CbtSubject, on_delete=models.CASCADE, related_name='PR_SUBJECT', null=True, blank=True)
    PR_CLASS = models.ForeignKey(CbtClasses, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cbt_class_subject'

# class CbtDepartment(models.Model):
#     PR_DEPARTMENT_ID = models.BigAutoField(primary_key=True)
#     PR_NAME = models.CharField(max_length=255, unique=True)
#     PR_ICON = models.CharField(max_length=255, null=True, blank=True, default='')
#     PR_DESCRIPTION = models.TextField(max_length=255, null=True, blank=True, default='')
#     PR_STATUS = models.IntegerField(null=True, blank=True, default=0)
#     PR_CREATED_AT = models.DateTimeField(auto_now_add=True)
#     PR_MODIFIED_AT = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'cbt_department'        

# class CbtDesignation(models.Model):
#     PR_DESIGNATION_ID = models.BigAutoField(primary_key=True)
#     PR_NAME = models.CharField(max_length=255, unique=True)
#     PR_ICON = models.CharField(max_length=255, null=True, blank=True, default='')
#     PR_DESCRIPTION = models.TextField(max_length=255, null=True, blank=True, default='')
#     PR_STATUS = models.IntegerField(null=True, blank=True, default=0)
#     PR_CREATED_AT = models.DateTimeField(auto_now_add=True)
#     PR_MODIFIED_AT = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'cbt_designation'

# class CbtDepartmentDesignation(models.Model):
#     PR_ID = models.BigAutoField(primary_key=True)
#     PR_DEPARTMENT = models.ForeignKey(CbtDepartment, on_delete=models.CASCADE, related_name='PR_DESIGNATIONS', null=True, blank=True)
#     PR_DESIGNATION = models.ForeignKey(CbtDesignation, on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'cbt_department_designation'


# Board Model
class CbtBoard(models.Model):
    PR_BOARD_ID = models.AutoField(primary_key=True)
    PR_NAME = models.CharField(max_length=100, default='')
    # Timestamps
    PR_IMAGE = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_DESCRIPTION = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_STATUS = models.IntegerField(null=True, blank=True, default=0)
    PR_CREATED_AT = models.DateTimeField(auto_now_add=True)
    PR_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cbt_board'

# Series Model (Updated)
class CbtSeries(models.Model):
    PR_SERIES_ID = models.AutoField(primary_key=True)
    PR_NAME = models.CharField(max_length=255, default='')
    # Relationships
    PR_BOARD = models.ForeignKey(CbtBoard, on_delete=models.SET_NULL, null=True, blank=True ,related_name='pr_series')
    # Many-to-Many Relationship with CbtClasses
    PR_CLASSES = models.ManyToManyField(CbtClasses, through='CbtSeriesClass', related_name='pr_series_classes')
    # Timestamps
    PR_IMAGE = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_DESCRIPTION = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_STATUS = models.IntegerField(null=True, blank=True, default=0)
    PR_CREATED_AT = models.DateTimeField(auto_now_add=True)
    PR_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cbt_series'

# Pivot Table (CbtSeriesClass)
class CbtSeriesClass(models.Model):
    PR_SERIES_CLASS_ID = models.AutoField(primary_key=True)
    PR_CLASS = models.ForeignKey(CbtClasses, on_delete=models.CASCADE)
    PR_SERIES = models.ForeignKey(CbtSeries, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cbt_series_class'
        unique_together = ('PR_CLASS', 'PR_SERIES')  # Ensures uniqueness between the class and series pair

# Book Type Model
class CbtBookType(models.Model):
    PR_BOOK_TYPE_ID = models.AutoField(primary_key=True)
    PR_NAME = models.CharField(max_length=255, default='')
    # Timestamps
    PR_IMAGE = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_DESCRIPTION = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_STATUS = models.IntegerField(null=True, blank=True, default=0)
    PR_CREATED_AT = models.DateTimeField(auto_now_add=True)
    PR_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cbt_book_type'

# Main Data Model (CbtExcelData)
class CbtBookData(models.Model):
    PR_BOOK_ID = models.AutoField(primary_key=True)

    PR_TITLE = models.CharField(max_length=255, null=True, blank=True, default='')
    PR_SUB_TITLE = models.CharField(max_length=255, null=True, blank=True, default='')

    PR_SERIES = models.ForeignKey(CbtSeries, on_delete=models.SET_NULL, null=True, blank=True)
    PR_BOARD = models.ForeignKey(CbtBoard, on_delete=models.SET_NULL, null=True, blank=True)
    PR_CLASS = models.ForeignKey(CbtClasses, on_delete=models.SET_NULL, null=True, blank=True)
    PR_BOOK_TYPE = models.ForeignKey(CbtBookType, on_delete=models.SET_NULL, null=True, blank=True)
    PR_SUBJECT = models.ForeignKey(CbtSubject, on_delete=models.SET_NULL, null=True, blank=True)

    PR_ISBN = models.CharField(max_length=255, null=True, blank=True, default='')
    PR_IMPRINT = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_AUTHOR = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_EDITION = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_COMPANY = models.CharField(max_length=255, null=True, blank=True, default='')
    PR_BOOK_CODE = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_COPYRIGHT = models.CharField(max_length=50, null=True, blank=True, default='')
    PR_DATE_OF_RELEASE = models.DateField(null=True, blank=True)
    PR_BINDING = models.CharField(max_length=50, null=True, blank=True , default='')
    PR_LANGUAGE = models.CharField(max_length=50, null=True, blank=True, default='')
    PR_PAGES = models.IntegerField(null=True, blank=True)
    PR_TRIM_SIZE = models.CharField(max_length=50, null=True, blank=True, default='')
    PR_WEIGHT = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    PR_LIST_PRICE = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    PR_DISCOUNT = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    PR_BOOK_NUMBER = models.IntegerField(null=True, blank=True)
    PR_CLASS_LEVEL = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_PRODUCT_DIVISION = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_BROAD_SUBJECT = models.CharField(max_length=255, null=True, blank=True, default='')
    PR_DETAILED_SUBJECT = models.CharField(max_length=255, null=True, blank=True, default='')
    PR_PRODUCT_DESCRIPTION = models.TextField(null=True, blank=True)    
    PR_IMAGE = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_DESCRIPTION = models.CharField(max_length=100, null=True, blank=True, default='')
    PR_STATUS = models.IntegerField(null=True, blank=True, default=0)
    PR_CREATED_AT = models.DateTimeField(auto_now_add=True)
    PR_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cbt_book_data'
