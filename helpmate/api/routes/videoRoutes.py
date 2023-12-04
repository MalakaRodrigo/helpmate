from flask import Blueprint, render_template_string, request, jsonify
import base64
from PIL import Image
from io import BytesIO
import random

videos_api_v1 = Blueprint("video_api_v1", "video_api_v1", url_prefix="/api/v1/videos")


@videos_api_v1.route("/", methods=["POST"])
def api_save_video():
    try:
        # Get the base64-encoded image data from the POST request
        base64_image = request.data.decode('utf-8')
        print(base64_image)

        # Remove the header (data:image/jpeg;base64,) from the base64 string
        base64_data = base64_image.split(',')[1]
        print(base64_data)

        # Decode base64 data and create a BytesIO object
        image_data = base64.b64decode(base64_data)
        image_stream = BytesIO(image_data)

        # Open the image using PIL (Pillow)
        original_image = Image.open(image_stream)

        # Resize the image to 64x64 pixels
        resized_image = original_image.resize((64, 64))

        # Save the resized image as a jpeg
        # output_stream = BytesIO()
        # resized_image.save('video/output_stream.jpeg', format='JPEG')
        # output_stream.seek(0)

        # Generate a random number between 1 and 6 (inclusive)
        random_number = random.randint(1, 6)
        # Send the resized image as a response
        return (
            jsonify(
                {
                    "success": True,
                    "data": {'category' : random_number},
                    "message": {},
                }
            ),
            200,
        )
    except Exception as e:
        error_message = str(e)
        return (
            jsonify(
                {
                    "success": False,
                    "data": {},
                    "message": {"error": error_message},
                }
            ),
            500,
        )
