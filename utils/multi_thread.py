import threading
from django.db import close_old_connections


class ThreadWithResult(threading.Thread):
    def __init__(self, func, args):
        super(ThreadWithResult, self).__init__()
        self.func = func
        self.args = args
        self.exception = None
        self.lock = threading.Lock()

    def run(self):
        try:
            with self.lock:
                self._result = self.func(*self.args)
                close_old_connections()
        except Exception as e:
            self.exception = e

    @property
    def result(self):
        with self.lock:
            if self.exception:
                raise self.exception
            return self._result

        
# Usage
# Run function in a sperate thread:
# t = run_func_in_thread(exectued_function, args, wait=False)
# t.start()
# Run function in a sperate thread with returned result:
# t = run_func_in_thread(exectued_function, args, wait=True)
# t.start()
# result = t.result
def run_func_in_thread(func, args, wait=False):
    """
    :param func: function needed to be executed in an independent thread
    :param args: arguments for the function
    :param wait: Whether to block the thread and wait for output results 
    :return: Thread object
    """
    t = ThreadWithResult(func, args)
    t.start()
    if wait:
        t.join()

    return t
