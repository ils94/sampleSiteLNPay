from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

payment_status = {}  # Store payment status per invoice


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    if not data or 'amount' not in data or 'ln_address' not in data:
        return jsonify({"message": "Invalid data", "status": "error"}), 400

    try:
        amount = float(data['amount'])
    except ValueError:
        return jsonify({"message": "Amount is not a valid number", "status": "error"}), 400

    response = requests.post('http://127.0.0.1:5000/generate-invoice', json=data)

    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError:
        return jsonify({"message": "Error processing API response", "status": "error"}), 500

    if 'data' not in response_data:
        return jsonify({"message": "Invalid API response", "status": "error"}), 500

    invoice_id = response_data['data']['quote']['lnInvoice']  # Use invoice as ID
    payment_status[invoice_id] = False  # Initialize status as unpaid

    return jsonify({
        "invoice_id": invoice_id,
        "time": response_data['data']['expiration_time'],
        "amount_sats": response_data['data']['quote']['sourceAmount']['amount'],
        "qr_code": response_data['data']['qr_code'],
        "invoice": invoice_id
    })


@app.route('/qr_code.html')
def qr_code():
    amount_sats = request.args.get('amount_sats')
    time = request.args.get('time')
    qr_code = request.args.get('qr_code')
    invoice = request.args.get('invoice')

    return render_template('qr_code.html', amount_sats=amount_sats, time=time, qr_code=qr_code, invoice=invoice)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"🔔 Webhook recebido: {data}")  # Log para ver se o webhook chegou

    if not data or 'invoice' not in data:
        print("❌ Dados inválidos recebidos no webhook!")
        return jsonify({"message": "Invalid data", "status": "error"}), 400

    invoice_id = data['invoice']

    if data.get('status') == 'success':
        print(f"✅ Pagamento confirmado para {invoice_id}")
        payment_status[invoice_id] = True  # Atualiza o status do pagamento
        print(f"📌 Novo status: {payment_status}")  # Verifica se está sendo salvo corretamente

    return jsonify({"message": "Webhook received", "status": "success"}), 200


@app.route('/check_payment_status')
def check_payment_status():
    invoice_id = request.args.get('invoice_id')

    if not invoice_id:
        return jsonify({"message": "Invoice ID required", "status": "error"}), 400

    return jsonify({"invoice_id": invoice_id, "success": payment_status.get(invoice_id, False)})


@app.route('/payment_success')
def payment_success():
    invoice_id = request.args.get('invoice_id')

    print(f"invoice: {invoice_id}")

    if invoice_id in payment_status:
        payment_status.pop(invoice_id)  # 🛑 REMOVE A ENTRADA DA MEMÓRIA!

    heading = request.args.get('heading', 'Pagamento Realizado!')
    message = request.args.get('message', 'Sua ordem de compra já foi efetuada!')
    return render_template('payment_success.html', title="Success", heading=heading, message=message)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
