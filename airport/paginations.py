from rest_framework.pagination import PageNumberPagination


class TwoSizePagination(PageNumberPagination):
    page_size = 2
    page_query_param = "page_size"
    max_page_size = 100


class FiveSizePagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class TenSizePagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page_size"
    max_page_size = 100