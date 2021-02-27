def get_percent(num, percent):
    return round((num * percent) / 100, 2)

def get_iva(num):
        return round(get_percent(num, 16), 2)