from dotenv import load_dotenv

from flask import Flask
from flask import request
from flask import jsonify
from flask import send_from_directory

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from langchain_core.chat_history import InMemoryChatMessageHistory

load_dotenv()

app = Flask(__name__, static_folder='public')

# =========================
# LLM
# =========================

llm = ChatOpenAI(
    model='gpt-4o-mini'
)

# =========================
# Prompt
# =========================

prompt = ChatPromptTemplate.from_messages([
    ('system', '당신은 친절한 챗봇입니다.'),
    MessagesPlaceholder('history'),
    ('user', '{input}')
])

chain = prompt | llm | StrOutputParser()

# =========================
# Memory
# =========================

history = InMemoryChatMessageHistory()

# =========================
# 화면
# =========================

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

# =========================
# API
# =========================

@app.route('/api/chat', methods=['POST'])
def chat():

    data = request.get_json()

    message = data.get('message')

    answer = chain.invoke({
        'input': message,
        'history': history.messages[-10:]
    })

    history.add_user_message(message)
    history.add_ai_message(answer)

    return jsonify({
        'answer': answer
    })

# =========================

if __name__ == '__main__':
    app.run(debug=True)