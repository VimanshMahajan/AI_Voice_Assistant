import openai
from config import apikey

openai.api_key = apikey
conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, my name is John and I am a software engineer."}
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=conversation_history,
    max_tokens=50
)

print(response)

# "C:\Users\Vimansh Mahajan\PycharmProjects\pythonProject_AI\.venv\Scripts\python.exe" "C:\Users\Vimansh Mahajan\PycharmProjects\pythonProject_AI\openaitest.py"
# {
#   "id": "chatcmpl-90SrWNud91zrlbQVENlPWtgVYTwgI",
#   "object": "chat.completion",
#   "created": 1709897974,
#   "model": "gpt-3.5-turbo-16k-0613",
#   "choices": [
#     {
#       "index": 0,
#       "message": {
#         "role": "assistant",
#         "content": "Hi John! It's nice to meet you. How can I assist you today?"
#       },
#       "logprobs": null,
#       "finish_reason": "stop"
#     }
#   ],
#   "usage": {
#     "prompt_tokens": 30,
#     "completion_tokens": 17,
#     "total_tokens": 47
#   },
#   "system_fingerprint": null
# }
#
# Process finished with exit code 0
