# coding: utf-8



import cv2
import numpy
import datetime
import chatbot_text_analyze
import chatbot_text_generate
import chatbot_image_analyze
import chatbot_image_generate
from flask import Flask, render_template, request, url_for, redirect, flash




app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SECRET_KEY"] = "python_flask_chatbot_appmain"




@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "GET":

       return render_template("index.html")


    if request.method == "POST":

       if not request.form["sent_msg_txt"]:

          flash("メッセージが入力されていません！")

          return redirect(url_for("index"))

       if not request.files["sent_msg_img"]:

          flash("画像が指定されていません！")

          return redirect(url_for("index"))

       img_dir = "static/images/"

       stream = request.files["sent_msg_img"].stream
       img_array = numpy.asarray(bytearray(stream.read()), dtype=numpy.uint8)
       img = cv2.imdecode(img_array, 1)

       dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
       orign_img_pth = img_dir + dt_now + ".jpg"
       cv2.imwrite(orign_img_pth, img)

       img = (img * -1) + 255
       img = numpy.clip(img, 0, 255).astype(numpy.uint8)
       dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
       anlyzd_img_pth = img_dir + dt_now + ".jpg"
       cv2.imwrite(anlyzd_img_pth, img)

       img_ttl     = "画像タイトル:実装予定"
       img_dscrptn = "画像説明:実装予定"
       lrnng_rslts = "学習結果:実装予定"

       orign_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info = chatbot_text_analyze.analyze_text(request.form["sent_msg_txt"])
       orign_txts, gnrtd_txt, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info, uttrnc_mdl = \
       chatbot_text_generate.generate_text(orign_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info)

       return render_template("chat_page__bot_reply.html", original_texts=orign_txts,     generated_text=gnrtd_txt, \
                               text_mean=txt_mean,         text_tokens=txt_tkns,          text_sentiment=txt_sntmnt, \
                               text_dijest=txt_djst,       context=cntxt,                 topic=tpc,
                               user_infomation=usr_info,   utterance_modal=uttrnc_mdl, \
                               original_image_path=orign_img_pth, analyzed_image_path=anlyzd_img_pth, \
                               image_title=img_ttl, image_description=img_dscrptn, learning_results=lrnng_rslts)


@app.route("/chat_page__bot_reply", methods=["GET"])
def chat_page__bot_reply():

    if request.method == "GET":

       return render_template("index.html")



if __name__ == "__main__":
   app.run(debug=True, host="localhost", port=5000)
