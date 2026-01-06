from rest_framework.pagination import PageNumberPagination

class StudentPagination(PageNumberPagination):
    page_size = 10                 # students per page
    page_size_query_param = "pageSize"
    max_page_size = 100