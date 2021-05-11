from PyCursed.urls import Url
from views import Base

urlpatterns = [
    #Каретка(^) - Начало строки, Доллар($) - конец
    Url('^S', Base),

]