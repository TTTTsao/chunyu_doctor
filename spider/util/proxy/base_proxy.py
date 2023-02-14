import threading
import queue

lock = threading.RLock()


class Proxy:
    def __init__(self, key, proxy):
        self.key = key
        self.proxy = proxy
        self.bad_request = 0


class ProxyPool:
    in_use = {}
    waiting = queue.Queue()

    @staticmethod
    def get_proxy(old_key, fetch_proxy, check_discard):
        old_proxy = None
        if old_key in ProxyPool.in_use:
            old_proxy = ProxyPool.in_use.pop(old_key)
        if ProxyPool.waiting.empty():
            ProxyPool.waiting.put(fetch_proxy())
        new_proxy = ProxyPool.waiting.get()
        if old_proxy is not None:
            old_proxy.bad_request += 1
            if not check_discard(old_proxy):
                ProxyPool.waiting.put(old_proxy)
        ProxyPool.in_use[new_proxy.key] = new_proxy
        return new_proxy.proxy, new_proxy.key

    @staticmethod
    def request_success(key):
        ProxyPool.in_use[key].bad_request = 0
