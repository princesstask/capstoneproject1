from flask import Flask, render_template, request, jsonify
# Mengimpor logika otomata dari file automata_engine.py di folder yang sama
from automata_engine import process_fsa, process_regex, process_pda, process_chomsky

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/fsa', methods=['GET', 'POST'])
def fsa():
    if request.method == 'POST':
        data = request.json
        result = process_fsa(data)
        return jsonify(result)
    return render_template('fsa.html')

@app.route('/regex', methods=['GET', 'POST'])
def regex():
    if request.method == 'POST':
        data = request.json
        result = process_regex(data)
        return jsonify(result)
    return render_template('regex.html')

@app.route('/pda', methods=['GET', 'POST'])
def pda():
    if request.method == 'POST':
        data = request.json
        result = process_pda(data)
        return jsonify(result)
    return render_template('pda.html')

@app.route('/chomsky', methods=['GET', 'POST'])
def chomsky():
    if request.method == 'POST':
        data = request.json
        result = process_chomsky(data)
        return jsonify(result)
    return render_template('chomsky.html')

if __name__ == '__main__':
    app.run(debug=True)