from flask import Flask, render_template, request, jsonify
import os
import shutil
import random

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    # Route for the main page
    # It lists image files and corresponding captions from the 'img' folder
    image_folder = './static/target/'
    
    # List and sort image files
    image_files = [image_folder + f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg', '.webp'))]
    random.shuffle(image_files)
    midpoint = len(image_files) // 2
    image_files_left = image_files[0:midpoint]
    image_files_right = image_files[midpoint:]
    random_numbers = random.sample(range(100000, 1000000), len(image_files_right))
    image_files = list(zip(image_files_left, image_files_right, random_numbers))

    # Render the index page with the lists of image and caption files
    return render_template('index.html', image_files=image_files, )

@app.route('/move_image', methods=['POST'])
def move_image():
    # Route to handle the moving of images and updating captions
    data = request.get_json()

    if data["caption"].lower() == "y": 
        # Move image and caption files to new destination
        shutil.move(data["srcPathImg1"], data["dstPathImg1"])
        shutil.move(data["srcPathImg2"], data["dstPathImg2"])

    try:
        # Respond with success message if no errors
        return jsonify({'message': 'Image moved successfully'}), 200  # HTTP 200 OK
    except Exception as e:
        # Handle exception and return an error response
        return jsonify({'error': str(e)}), 500  # HTTP 500 Internal Server Error

@app.route('/reshuffle_images', methods=['GET'])
def reshuffle_images():
    image_folder = './static/target/'
    
    # List and sort image files
    image_files = [image_folder + f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg', '.webp'))]
    random.shuffle(image_files)
    midpoint = len(image_files) // 2
    image_files_left = image_files[0:midpoint]
    image_files_right = image_files[midpoint:]
    random_numbers = random.sample(range(10000, 100000), len(image_files_right))
    image_files = list(zip(image_files_left, image_files_right, random_numbers))

    return jsonify(newImagePaths=image_files)
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
