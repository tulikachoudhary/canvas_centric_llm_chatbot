from flask import Flask, request, jsonify, render_template
from main_controller import process_courses, process_with_openai

app = Flask(__name__)
first_run = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def handle_message():
    global first_run
    response = ""
    message_input = request.form.get('messageInput')

    if message_input.lower() == '/refresh':
        process_courses()
        response = "Data has been refreshed!\n"
    elif first_run:
        process_courses()
        response = "Welcome to the Canvas GPT Chatbot!\n\n"
        response += process_with_openai(message_input) + "\n"
        first_run = False
    else:
        response = "===== OpenAI Response =====\n"
        response += process_with_openai(message_input) + "\n"
    
    return jsonify({'message': response})

if __name__ == '__main__':
    app.run(debug=True)
