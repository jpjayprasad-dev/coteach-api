## Flask App for Image and Query Processing
a chatbot API that is able to ingest images or text by a user. The chatbot should be able to fetch accurate YouTube links and respond to the user while answering their query on the chat. This Flask app allows users to submit an image and a query string. It then processes the image using a Multimodal LLM and combines the processed information with the query string before sending it to another agent for a final response.

### Requirements

* Python 3.11
* Flask
* llama_index  # for image processing (replace with your preferred library)
* OpenAI API Key  # Set the `OPENAI_API_TOKEN` environment variable

**Install dependencies:**

```bash
pip install -r requirements.txt
```
### Usage
Set the OPENAI_API_TOKEN environment variable with your OpenAI API key.
Run the app:

```bash
python app.py
```

### cURL Example
This cURL command sends a POST request to the app with a query string "algebra" and an image file "linear-equations.png":

```bash
curl -X POST http://localhost:5050/query \
  -H "Content-Type: multipart/form-data" \
  -F "query=algebra" \
  -F "file=@linear-equations.png"
```
