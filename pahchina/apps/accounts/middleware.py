# Created by zhangwei7@baixing.com on 2015-05-30 14:03

import threading


_thread_locals = threading.local()


def get_current_user():
    """Returns the current user."""
    return getattr(_thread_locals, 'user', None)


class GlobalUserMiddleware(object):
    """Puts the current user in thread_locals."""
    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)
