from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

payment_status = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    if not data or 'amount_fiat' not in data or 'ln_address' not in data:
        return jsonify({"message": "Invalid data", "status": "error"}), 400

    try:
        amount = float(data['amount_fiat'])
    except ValueError:
        return jsonify({"message": "Amount is not a valid number", "status": "error"}), 400

    response = requests.post('http://127.0.0.1:5000/generate-invoice', json=data)

    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError:
        return jsonify({"message": "Error processing API response", "status": "error"}), 500

    if 'data' not in response_data:
        return jsonify({"message": "Invalid API response", "status": "error"}), 500

    invoice = response_data['data']['quote']['lnInvoice']  # Use invoice as ID
    payment_status[invoice] = False  # Initialize status as unpaid

    return jsonify({
        "time": response_data['data']['expiration_time'],
        "amount_btc": response_data['data']['quote']['sourceAmount']['amount'],
        "qr_code": response_data['data']['qr_code'],
        "invoice": invoice
    })


@app.route('/qr_code.html')
def qr_code():
    amount_btc = request.args.get('amount_btc')
    time = request.args.get('time')
    qr_code = request.args.get('qr_code')
    invoice = request.args.get('invoice')

    return render_template('qr_code.html', amount_btc=amount_btc, time=time, qr_code=qr_code, invoice=invoice)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"Webhook received: {data}")

    if not data or 'invoice' not in data:
        print("Webhook has wrong data!")
        return jsonify({"message": "Invalid data", "status": "error"}), 400

    invoice = data['invoice']

    if data.get('status') == 'success':
        print(f"Payment confirmed for {invoice}")
        payment_status[invoice] = True
        print(f"New status: {payment_status}")

    return jsonify({"message": "Webhook received", "status": "success"}), 200


@app.route('/check_payment_status')
def check_payment_status():
    invoice = request.args.get('invoice')

    if not invoice:
        return jsonify({"message": "Invoice ID required", "status": "error"}), 400

    return jsonify({"invoice_id": invoice, "success": payment_status.get(invoice, False)})


@app.route('/payment_success')
def payment_success():
    invoice = request.args.get('invoice')

    print(f"invoice: {invoice}")

    if invoice in payment_status:
        payment_status.pop(invoice)

    heading = request.args.get('heading', 'Payment Completed!')
    message = request.args.get('message', 'Thank you for testing 😀!')

    return render_template('payment_success.html', title="Success", heading=heading, message=message)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
