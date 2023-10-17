import easyocr
PATH=r"C:\RR.png"
reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
result = reader.readtext(PATH)
print(result)