import base64

# Raw-строка: игнорирует escape-символы
with open(r'C:\Users\Юлия\Desktop\test_image.jpg', 'rb') as image_file:
    encoded = base64.b64encode(image_file.read()).decode('utf-8')
    print(encoded)  # Скопируйте эту чистую base64-строку!

# Если нужно data URI для JSON:
print(f"data:image/jpeg;base64,{encoded}")
