
import inspect


def get_request():
    """
    Walk up the stack, return the nearest first argument named "request".

    http://nedbatchelder.com/blog/201008/global_django_requests.html
    """
    frame = None
    try:
        for f in inspect.stack()[1:]:
            frame = f[0]
            code = frame.f_code
            if code.co_varnames and code.co_varnames[0] == 'request':
                return frame.f_locals.get('request')
    finally:
        del frame


def get_request_user():
    request = get_request()
    if request:
        return request.user
