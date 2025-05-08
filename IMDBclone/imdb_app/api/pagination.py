from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchListPagination(PageNumberPagination):
    # We are overriding the default pagination configurations.
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10

    #in order to directly access the last page of the results, 
    # we can access like this: http://127.0.0.1:8000/watch/list/?page=last
    last_page_strings = ['last']  # This will be used to get the last page of the results.

class WatchListLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5 #page size

class WatchListCursorPagination(CursorPagination):
    #It will use the concept of next page and previous page only not the page number.
    page_size = 5
    ordering = 'created_at'