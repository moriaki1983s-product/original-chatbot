# coding: utf-8




import chatbot_text_analyze
import chatbot_text_generate
from flask import Flask, render_template, request




app = Flask(__name__, static_folder="./templates/images")




@app.route("/", methods=["GET","POST"])
def index():

    if request.method == "GET":

       return render_template("index.html")


    if request.method == "POST":

       txt_mean, anlyzd_tkns1, anlyzd_tkns2, txt_sntmnt, txt_djst = chatbot_text_analyze.analyze_text(request.form["sent_txt"])
       gnrtd_txt, txt_mean, anlyzd_tkns1, anlyzd_tkns2, txt_sntmnt, txt_djst, uttrnc_mdl = \
       chatbot_text_generate.generate_text(txt_mean, anlyzd_tkns1, anlyzd_tkns2, txt_sntmnt, txt_djst)

       return render_template("bot_reply.html", reply_txt1=gnrtd_txt, reply_txt2=txt_mean, reply_txt3=anlyzd_tkns1, \
                               reply_txt4=anlyzd_tkns2, reply_txt5=txt_sntmnt, reply_txt6=txt_djst, reply_txt7=uttrnc_mdl)


@app.route("/bot_reply", methods=["GET"])
def bot_reply():

    if request.method == "GET":

       return render_template("index.html")




if __name__ == "__main__":
   app.run(debug=True, host="localhost", port=5000)