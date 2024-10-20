from random import randint
from time import sleep

from flask import Flask, jsonify, request

from bot.ai_bot import AIBot
from services.waha import Waha

app = Flask(__name__)


@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json

    print(f'EVENTO RECEBIDO: {data}')

    waha = Waha()
    ai_bot = AIBot()

    chat_id = data['payload']['from']
    received_message = data['payload']['body']
    is_group = '@g.us' in chat_id
    is_status = 'status@broadcast' in chat_id

    if is_group or is_status:
        return jsonify({'status': 'success', 'message': 'Mensagem de grupo/status ignorada.'})

    waha.star_typing(chat_id=chat_id)

    response = ai_bot.invoke(question=received_message)

    sleep(randint(3, 10))
    waha.send_message(
        chat_id=chat_id,
        message=response,
        # message='Resposta Automática :)',
    )

    waha.stop_typing(chat_id=chat_id)
    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
