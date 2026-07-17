import datetime

# Used to keep address formatting consistent between the address_index_map and the package address components when doing lookups in nearest neighbor.
def format_address(street_address, zip_code):
    clean_street_address = street_address.strip().lower()
    clean_zip_code = zip_code.strip(" ()")
    return clean_street_address + '|' + clean_zip_code

# Used on import of package details to convert string dates to python datetime objects
def parse_delivery_deadline(delivery_deadline):
    if delivery_deadline == "EOD": return datetime.time(17, 0, 0)
    time_parts = delivery_deadline.strip().replace(':', ' ' ).split(' ')
    hour = int(time_parts[0])
    minute = int(time_parts[1])
    if time_parts[2] == 'PM': hour += 12
    return datetime.time(hour, minute, 0)