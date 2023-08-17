
from ursina import invoke
def after(delay):
    '''@after  decorator for calling a function after some time.
        example:
        @after(.4)
        def reset_cooldown():
            self.on_cooldown = False
            self.color = color.green
    '''
    def decorator(func):
        def wrapper(*args, **kwargs):
            invoke(func, *args, **kwargs, delay=delay)
        return wrapper()
    return decorator