# Used to keep address formatting consistent between the address_index_map and the package address components when doing lookups in nearest neighbor.
def format_address(street_address, zip_code):
    clean_street_address = street_address.strip().lower()
    clean_zip_code = zip_code.strip(" ()")
    return clean_street_address + '|' + clean_zip_code