import datetime

def get_booking_end_time(days: int =14):

    return datetime.utcnow() + datetime.timedelta(days=days)