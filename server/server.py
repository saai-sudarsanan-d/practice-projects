from flask import Flask, request,render_template,send_file,redirect,abort
from datetime import datetime
import os
app = Flask(__name__)
print(app)
@app.route('/', methods=['GET','POST'])
def result():
    if request.method == 'GET':
        return render_template("index.html")
    if request.method == 'POST':
        if request.form['00'] == "**": # Some form of signature
            log = open("keys.txt","a")
            log.write(f"{datetime.now()},{request.form['ip']},{request.form['log']}\n")
            log.flush()
            log.close()
    return ''

@app.route('/**',methods=['GET','POST']) # A hidden path that should be hard to find
def download():
    if request.method == 'GET':
        return abort(404)
    if request.method == 'POST':
        if request.form['00'] == "**": # Verify the signature
            if request.form['00'] == "**": # Verify Username of some sort
                if request.form['00'] == "**": # Verify Password of some sort
                    p = "keys.txt"
                    return send_file(p,as_attachment=True)
    return ''

@app.route('/**') ## Path to clear contents
def delete():
    log = open("keys.txt","w")
    log.write("")
    log.close()
    return abort(404)

@app.route('/flag')
def flag():
    return "**" # Capture the Flag :)
if __name__ == "__main__":
    app.run(port=int(os.getenv('PORT')))

# I have replaced password, usernames and paths with a '**' or a '00' becuase I don't want my deployment to be used for malicious purposes.
# I do not recommend you trying to use this for malicious purposes either
