import os
from llama_index.core.tools import FunctionTool
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from prompt import coteach_prompt
from youtubesearchpython import VideosSearch
from llama_index.multi_modal_llms.openai import OpenAIMultiModal  # For OpenAI Multimodal LLM

# Load OpenAI API token from environment variable (ensure it's set)
OPENAI_API_TOKEN = os.getenv('OPENAI_API_TOKEN')

llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo-0125")

def search_youtube(query):
    """
    Search youtube for the video based on the query. 
    Video links will be returned if searched videos are found.
    """
    videosSearch = VideosSearch(query, limit = 2)
    search_results = videosSearch.result()

    # Check if the request was successful
    if search_results:
        # Parse the response to extract video links
        video_links = ['https://www.youtube.com/watch?v=' + item['id'] 
                            for item in search_results['result']]
        return video_links
    else:
        # Handle errors
        return f'No video results found!'

search_youtube_tool = FunctionTool.from_defaults(fn=search_youtube)

coteach_openai_agent = OpenAIAgent.from_tools(
    system_prompt= coteach_prompt, tools=[search_youtube_tool], 
    llm=llm, verbose=True,
)

# Create OpenAI Multimodal LLM instance
openai_mm_llm = OpenAIMultiModal(
    model="gpt-4-vision-preview",
    api_key=OPENAI_API_TOKEN,
    max_new_tokens=300,
)
