from django.db.backends.signals import connection_created
from django.dispatch import receiver

@receiver(connection_created)
def db_connection_handler(sender, connection, **kwargs):
    print("Kết nối với cơ sở dữ liệu đã thành công!")
