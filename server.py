from flask import Flask
from flask import render_template, request, jsonify
from datetime import datetime

import json 
import sqlite3
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/sendFeedback", methods=['POST'])
def save_feedback():
    con = sqlite3.connect('barber.db')
    cur = con.cursor()
    temp = dict(request.form)
    employee = "Zhandos"
    service = "Haircut"
    phone = "89876543210"
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
    cur.execute(f"INSERT INTO feedback (employee, rate, service, phone, feedback, allow, timedate) VALUES ('{employee}', '{temp['rate']}', '{service}', '{phone}', '{temp['feedback']}', '{temp['allow']}', '{date}')")
    con.commit()
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200), 200


@app.route("/feedback/<id>")
def feedback_page(id):
    return render_template("feedback.html")


@app.route("/getFeedback")
def get_feedback():
    con = sqlite3.connect('barber.db')
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM feedback ORDER BY id DESC")
    result = []
    for row in rows:
        result.append(row)

    return render_template("feedbacks.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)