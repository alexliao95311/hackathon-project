import face_recognition

# Get user input for the known image filename
known_filename = input("Enter the filename of the known image (e.g., donald_trump.jpeg): ")
known_image_path = f"images/{known_filename}"
known_image = face_recognition.load_image_file(known_image_path)
known_encoding = face_recognition.face_encodings(known_image)[0]

# Get user input for the test image filename
test_filename = input("Enter the filename of the test image (e.g., test_image.png): ")
unknown_image_path = f"images/{test_filename}"
unknown_image = face_recognition.load_image_file(unknown_image_path)
unknown_encoding = face_recognition.face_encodings(unknown_image)[9]

# Compare faces
results = face_recognition.compare_faces([known_encoding], unknown_encoding)

# Check if the faces match
if results[0]:
    print(f"Face Recognized! This is {known_filename.split('.')[0].replace('_', ' ').title()}.")
else:
    print("Face Not Recognized. This is not the known person.")
