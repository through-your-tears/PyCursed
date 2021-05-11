import os

from PyCursed.main import PyCursed
from urls import urlpatterns
from PyCursed.miiddleware import middlewares

settings = {
    'BASE_DIR': os.path.dirname(os.path.abspath(__file__)),
    'TEMPLATE_DIR_NAME': 'templates'
}

app = PyCursed(
    urls=urlpatterns,
    settings=settings,
    middlewares=middlewares
)
