#### Flask App for Image and Query Processing

from flask import Flask, request, jsonify
from llama_index.core import SimpleDirectoryReader  # For reading image data
import os  # For file path manipulation
from util import openai_mm_llm, coteach_openai_agent  # For agent interaction

# Initialize Flask app
app = Flask(__name__)

# Configure directory for uploaded images
UPLOAD_FOLDER = 'image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/query', methods=['GET', 'POST'])
def upload_file():
    """
    Handles image upload and query processing requests.

    Expects a POST request with the following:
        - query (form data): The user's query string.
        - file (file): The uploaded image file.

    Returns a JSON response with the agent's response message.
    """

    # Get query string from form data
    query_string = request.form.get("query")

    if "file" in request.files:
        # Get uploaded image file
        image_file = request.files["file"]

        # Create filename with path
        filename = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)

        # Save the uploaded image file
        image_file.save(filename)

        # Use SimpleDirectoryReader to load image data
        image_documents = SimpleDirectoryReader(app.config['UPLOAD_FOLDER']).load_data()

        # Generate image description using OpenAI Multimodal LLM
        response = openai_mm_llm.complete(
            prompt="Describe the images as an alternative text",
            image_documents=image_documents,
        )

        # Delete the uploaded image file
        os.remove(filename)

        # Combine query string with processed image data
        query_string = query_string + " \nHere is the data from the image \n####" + str(response) + "####"

    # Call coteach_openai_agent to get response based on combined query
    response = coteach_openai_agent.chat(query_string)

    # Return agent's response message as JSON
    return jsonify({'message': str(response.response)}), 200


if __name__ == '__main__':
    # Run the Flask app on port 5050 in debug mode
    app.run(port=5050, debug=True)

