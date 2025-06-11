from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WatchListPagination(PageNumberPagination):
    """
    Custom pagination class for watchlist view.
    """
    page_size = 4  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow clients to set the page size via query parameter
    max_page_size = 20  # Maximum number of items per page allowed by the client
    page_query_param = 'page'  # Query parameter for the page number
    last_page_strings = 'end'  # String to indicate the last page in the response


class WatchListLimitOffsetPagination(LimitOffsetPagination):
    """
    Custom pagination class for watchlist view using limit and offset.
    """
    default_limit = 4  # Default number of items per page
    max_limit = 20  # Maximum number of items per page allowed by the client
    limit_query_param = 'limit'  # Query parameter for the limit
    offset_query_param = 'offset'  # Query parameter for the offset
    
    
class WatchListCursorPagination(CursorPagination):
    """
    Custom pagination class for watchlist view using cursor-based pagination.
    """
    page_size = 4  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow clients to set the page size via query parameter
    max_page_size = 20  # Maximum number of items per page allowed by the client
    cursor_query_param = 'cursor'  # Query parameter for the cursor
    ordering = '-created'  # Default ordering for the items
    
