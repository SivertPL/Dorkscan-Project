import settings 

def get_proxy_url():
    if settings.TOR_ENABLED:
        return "socks5://127.0.0.1:9060"   
    if settings.PROXY_ENABLED:
        return "{}://{}:{}".format(settings.PROXY_PROTOCOL, settings.PROXY_HOST, settings.PROXY_PORT)

def is_proxied():
    return settings.TOR_ENABLED or settings.PROXY_ENABLED


## TO BE IMPLEMENTED
def check_proxy_alive():
    pass