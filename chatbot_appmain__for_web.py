# coding: utf-8




from flask import Flask, render_template, request
import chatbot_module




app = Flask(__name__, static_folder="./templates/images")




@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "GET":
       return render_template("index.html")
    if request.method == "POST":
       txt_mean, anlyzd_txt, anlyzd_txt2 = chatbot_module.analyze_text(request.form["sent_txt"])
       txt_mean, anlyzd_txt, anlyzd_txt2 = chatbot_module.generate_text(txt_mean, anlyzd_txt, anlyzd_txt2)
       return render_template("reply.html", reply_txt=txt_mean, reply_txt2=anlyzd_txt, reply_txt3=anlyzd_txt2)


@app.route("/reply", methods=["GET"])
def reply():
    if request.method == "GET":
       return render_template("index.html")




if __name__ == "__main__":
   app.run(debug=True, host="localhost", port=5000)