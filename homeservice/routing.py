from django.urls import re_path, path
from . import consumers


websocket_urlpatterns = [ 
    # re_path(r'ws/notifications/', consumers.NotificationConsumer.as_asgi()),

    # url = ws://yourdomain.com/ws/employee/123/
    re_path(r'ws/employee/(?P<employee_id>\d+)/$', consumers.NotificationConsumer.as_asgi()),
    
]