from flask import Flask, render_template, request
import pandas as pd
from transform import *
from stats import *
import os


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    global fname
    global text_data
    if request.method == 'POST':
        f = request.files['file'] 
        fname = f.filename    
        f.save(f"uploads/{f.filename}") 
        data = pd.read_csv(f"uploads/{fname}")
        removenan(data)
        run_transform(data)       

        with open("results.txt", "r") as file:
            text_data = file.read()

        line = "/Users/vishwajeetpanda/Desktop/datos/plots/line"
        bar = "/Users/vishwajeetpanda/Desktop/datos/plots/barplots"

        line_lst = []
        bar_lst = []

        for dir in os.listdir(line):
            line_lst.append(os.path.join(line, dir))

        if os.listdir(bar)!=[]:
            for dir in os.listdir(bar):
                bar_lst.append(os.path.join(bar, dir))

        print(type(text_data))
        return render_template('/Acknowledgement.html', text_data = text_data)
    return render_template('/home.html')

@app.route('/column', methods=['POST', 'GET'])
def column():
    return render_template('column.html')

@app.route('/process_data', methods=['POST', 'GET'])
def process():
    return render_template('process.html')

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
