from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Credenciais da Meta
TOKEN = "EAAPdrdCvyjcBSa1U7F4Bhpg0FsZCEcKvSHZAFb1V7ph72CKKpVVZACVAAgLfpPZCfZCKbk8Ye5foxn1JtXAk3oDIaZBM5KBTbgvclhODZAcsZCs1jXIqJBIEyCZBKA99p189nC7UNzQ2iFBq4zD4W4E1waKmEZCuW70W5zwMZAd031RvCe1xJAdYsnIZBCRQizEBxoZBcFIRMxW3LQNXJomKLdOcmjubZAvw9nSCnqmIZAqWdtSUQ4ZBj0aqEwQvDPUwsV0uTChZCbU2TuesnHgbRUF2Qm6j47z3t"
PHONE_NUMBER_ID = "1313726418496265"
VERIFY_TOKEN = "meutokenseguro123"

# Validação do Webhook (GET)
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Token incorreto", 403

# Receber mensagens (POST)
@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()

    try:
        entry = data["entry"][0]["changes"][0]["value"]
        if "messages" in entry:
            message = entry["messages"][0]
            sender_id = message["from"]
            text = message["text"]["body"]

            print(f"Mensagem recebida de {sender_id}: {text}")
            send_whatsapp_message(sender_id, f"Olá! Recebi sua mensagem: '{text}'")

    except Exception as e:
        print("Erro ao processar mensagem:", e)

    return jsonify({"status": "success"}), 200

def send_whatsapp_message(to_number, text):
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
