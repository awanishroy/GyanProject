from django.db import models

# Board Model
class CbtSubject(models.Model):
    PR_SUBJECT_ID = models.AutoField(primary_key=True)
    PR_NAME = models.CharField(max_length=100)
    PR_CREATED_AT = models.DateTimeField(auto_now_add=True)
    PR_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cbt_subject'

# Class Level Model
class CbtClasses(models.Model):
    PR_CLASS_ID = models.AutoField(primary_key=True)
    PR_NAME = models.CharField(max_length=100)
    PR_SUBJECT = models.ManyToManyField(CbtSubject, through='CbtClassSubject', related_name='series')
    PR_CREATED_AT = models.DateTimeField(auto_now_add=True)
    PR_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cbt_classes'

# Pivot Table (CbtSeriesClass)
class CbtClassSubject(models.Model):
    PR_CLASS_SUBJECT_ID = models.AutoField(primary_key=True)
    PR_CLASS = models.ForeignKey(CbtClasses, on_delete=models.CASCADE)
    PR_SUBJECT = models.ForeignKey(CbtSubject, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cbt_class_subject'

# Board Model
class CbtBoard(models.Model):
    PR_BOARD_ID = models.AutoField(primary_key=True)
    PR_NAME = models.CharField(max_length=100)
    # Timestamps
    PR_CREATED_AT = models.DateTimeField(auto_now_add=True)
    PR_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cbt_board'

# Series Model (Updated)
class CbtSeries(models.Model):
    PR_SERIES_ID = models.AutoField(primary_key=True)
    PR_NAME = models.CharField(max_length=255)
    # Relationships
    PR_BOARD = models.ForeignKey(CbtBoard, on_delete=models.SET_NULL, null=True, blank=True)
    # Many-to-Many Relationship with CbtClasses
    PR_CLASSES = models.ManyToManyField(CbtClasses, through='CbtSeriesClass', related_name='series')
    # Timestamps
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
    PR_NAME = models.CharField(max_length=255)
    # Timestamps
    PR_CREATED_AT = models.DateTimeField(auto_now_add=True)
    PR_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cbt_book_type'

# Main Data Model (CbtExcelData)
class CbtBookData(models.Model):
    PR_BOOK_ID = models.AutoField(primary_key=True)

    PR_TITLE = models.CharField(max_length=255, null=True, blank=True)
    PR_SUB_TITLE = models.CharField(max_length=255, null=True, blank=True)

    PR_SERIES = models.ForeignKey(CbtSeries, on_delete=models.SET_NULL, null=True, blank=True)
    PR_BOARD = models.ForeignKey(CbtBoard, on_delete=models.SET_NULL, null=True, blank=True)
    PR_CLASS = models.ForeignKey(CbtClasses, on_delete=models.SET_NULL, null=True, blank=True)
    PR_BOOK_TYPE = models.ForeignKey(CbtBookType, on_delete=models.SET_NULL, null=True, blank=True)
    PR_SUBJECT = models.ForeignKey(CbtSubject, on_delete=models.SET_NULL, null=True, blank=True)

    PR_ISBN = models.CharField(max_length=255, null=True, blank=True)
    PR_IMPRINT = models.CharField(max_length=100, null=True, blank=True)
    PR_AUTHOR = models.CharField(max_length=100, null=True, blank=True)
    PR_EDITION = models.CharField(max_length=100, null=True, blank=True)
    PR_COMPANY = models.CharField(max_length=255, null=True, blank=True)
    PR_BOOK_CODE = models.CharField(max_length=100, null=True, blank=True)
    PR_COPYRIGHT = models.CharField(max_length=50, null=True, blank=True)
    PR_DATE_OF_RELEASE = models.DateField(null=True, blank=True)
    PR_BINDING = models.CharField(max_length=50, null=True, blank=True)
    PR_LANGUAGE = models.CharField(max_length=50, null=True, blank=True)
    PR_PAGES = models.IntegerField(null=True, blank=True)
    PR_TRIM_SIZE = models.CharField(max_length=50, null=True, blank=True)
    PR_WEIGHT = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    PR_LIST_PRICE = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    PR_DISCOUNT = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    PR_BOOK_NUMBER = models.IntegerField(null=True, blank=True)
    PR_CLASS_LEVEL = models.CharField(max_length=100, null=True, blank=True)
    PR_PRODUCT_DIVISION = models.CharField(max_length=100, null=True, blank=True)
    PR_BROAD_SUBJECT = models.CharField(max_length=255, null=True, blank=True)
    PR_DETAILED_SUBJECT = models.CharField(max_length=255, null=True, blank=True)
    PR_PRODUCT_DESCRIPTION = models.TextField(null=True, blank=True)

    PR_CREATED_AT = models.DateTimeField(auto_now_add=True)
    PR_MODIFIED_AT = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cbt_book_data'
