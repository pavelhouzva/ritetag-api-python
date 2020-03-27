import functools


def api_call(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        ret = f(self, *args, **kwargs)
        self._check_api_limits()
        return ret

    return wrapper


def api_request(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        ret = f(self, *args, **kwargs)
        self._set_api_limits(ret.status_code, ret.headers)
        return ret

    return wrapper
