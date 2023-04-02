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

       origin_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info = chatbot_text_analyze.analyze_text(request.form["sent_txt"])
       origin_txts, gnrtd_txt, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info, uttrnc_mdl = \
       chatbot_text_generate.generate_text(origin_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info)

       return render_template("bot_reply.html", reply_txt1=origin_txts, reply_txt2=gnrtd_txt, \
                               reply_txt3=txt_mean, reply_txt4=txt_tkns, reply_txt5=txt_sntmnt, \
                               reply_txt6=txt_djst, reply_txt7=cntxt, reply_txt8=tpc, reply_txt9=usr_info, reply_txt10=uttrnc_mdl)


@app.route("/bot_reply", methods=["GET"])
def bot_reply():

    if request.method == "GET":

       return render_template("index.html")




if __name__ == "__main__":
   app.run(debug=True, host="localhost", port=5000)