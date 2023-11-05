from flask import Flask, render_template, request

app = Flask("__main__")

@app.route("/")
def data():
    if request.method=="POST":
        col_name = request.form.get("column-name")
        dtype_name = request.form.get("column-dtype-name")
        print(col_name, dtype_name)
    return render_template("main.html")




if __name__=="__main__":
    app.run(debug=True)

