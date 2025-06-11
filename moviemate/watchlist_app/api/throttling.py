from rest_framework.throttling import UserRateThrottle



class ReviewCreateThrottle(UserRateThrottle):
    """
    Custom throttle class to limit the number of requests a user can make.
    """
    scope = 'review-create'
    # rate = '10/minute'  # Limit to 10 requests per minute per user


class ReviewListThrottle(UserRateThrottle):
    """
    Custom throttle class to limit the number of requests a user can make.
    """
    scope = 'review-list'