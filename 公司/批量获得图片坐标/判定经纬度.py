def correct_coordinates(longitude, latitude, lon_range=(108, 120), lat_range=(30, 38)):
    """
    Corrects the OCR-extracted longitude and latitude values based on the given ranges.
    """
    # Correct the longitude
    if longitude > lon_range[1] or longitude < lon_range[0]:
        longitude = longitude / 10**(len(str(int(longitude))) - len(str(int(lon_range[1]))))

    # Correct the latitude
    if latitude > lat_range[1] or latitude < lat_range[0]:
        latitude = latitude / 10**(len(str(int(latitude))) - len(str(int(lat_range[1]))))

    return longitude, latitude

# Parse the text to float values
longitude = map(float, text.split())

# Correct the coordinates
longitude, latitude = correct_coordinates(longitude, latitude)

print(longitude, latitude)
