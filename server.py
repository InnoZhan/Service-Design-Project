from flask import Flask
from flask import render_template, request, jsonify, url_for
from datetime import datetime
import qrcode
import json 
import sqlite3
import uuid
app = Flask(__name__)
from PIL import Image

services = {}

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/sendFeedback", methods=['POST'])
def save_feedback():
    con = sqlite3.connect('barber.db')
    cur = con.cursor()
    temp = dict(request.form)
    employee = temp['name']
    service = temp['service']
    phone = "89876543210"
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
    cur.execute(f"INSERT INTO feedback (employee, rate, service, phone, feedback, alias, timedate) VALUES ('{employee}', '{temp['rate']}', '{service}', '{phone}', '{temp['feedback']}', '{temp['alias']}', '{date}')")
    con.commit()
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200), 200

@app.route("/imageUpload", methods=['POST'])
def image_upload():
    temp = dict(request.form)
    beforeImage = request.files['imageBefore']
    afterImage = request.files['imageAfter']
    beforeImage.save('/home/zhandos/Study/Service design project/uploadedImage.png')
    afterImage.save('/home/zhandos/Study/Service design project/uploadedImage.png')
    print(type(fileimage))
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200), 200


@app.route("/feedback/<id>")
def feedback_page(id):
    temp = services[str(id)]
    return render_template("feedback.html", name = temp['employee'], service = temp['service'], before_image_url = temp['before_photo'], after_image_url = temp['after_photo'])


@app.route("/create_qr")
def create_qr():
    return render_template("create_qr.html")

@app.route("/generate_qr", methods=['POST'])
def generate_qr():
    temp = dict(request.form)
    # beforeImage = request.files['imageBefore']
    # afterImage = request.files['imageAfter']

    new_id = str(uuid.uuid4())
    # path_for_image = 'resources/'+new_id
    # before_image_path = path_for_image+'_before.png'
    # after_image_path = path_for_image+'_after.png'
    # beforeImage.save(before_image_path)
    # afterImage.save(after_image_path)
    before_image_path = 'resources/before.png'
    after_image_path = 'resources/after.png'
    
    services[new_id] = {'employee': temp['name'], 'service': temp['service'], 'before_photo': url_for('static', filename = before_image_path), 'after_photo': url_for('static', filename = after_image_path)}
    img = qrcode.make('http://ec2-18-224-37-124.us-east-2.compute.amazonaws.com:5000/feedback/'+str(new_id))
    # img = qrcode.make('http://192.168.1.56:5000/feedback/'+str(new_id))
    img.save("static/resources/some_file.png")
    return jsonify(isError= False,
                    message= "Success",
                    image = url_for('static', filename = 'resources/some_file.png'),
                    statusCode= 200), 200


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
    app.run(host="0.0.0.0", port=5000, debug = True)