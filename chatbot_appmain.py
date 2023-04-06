# coding: utf-8




import chatbot_module
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


       orign_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst = chatbot_module.analyze_text(request.form["sent_msg_txt"])
       orign_img = chatbot_module.restoration_image_from_datastream(request.files["sent_msg_img"].stream)
       anlyzd_img, img_ttl, img_dscrptn = chatbot_module.analyze_image(orign_img)

       orign_img_pth  = chatbot_module.generate_image_file(orign_img)
       anlyzd_img_pth = chatbot_module.generate_image_file(anlyzd_img)

       cntxt, tpc, usr_info, uttrnc_mdl = chatbot_module.inference_and_speculate(orign_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst, anlyzd_img, img_ttl, img_dscrptn)
       gnrtd_txts  = chatbot_module.generate_text(orign_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info, uttrnc_mdl)
       lrnng_rslts = chatbot_module.learning(orign_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info, uttrnc_mdl, anlyzd_img_pth, img_ttl, img_dscrptn)


       return render_template("bot_reply.html",          origin_texts=orign_txts, generated_texts=gnrtd_txts, \
                               text_mean=txt_mean,       text_tokens=txt_tkns,    text_sentiment=txt_sntmnt, \
                               text_dijest=txt_djst,     context=cntxt,           topic=tpc,
                               user_infomation=usr_info, utterance_modal=uttrnc_mdl, \
                               original_image_path=orign_img_pth, analyzed_image_path=anlyzd_img_pth, \
                               image_title=img_ttl, image_description=img_dscrptn, \
                               learning_results=lrnng_rslts)


@app.route("/bot_reply", methods=["GET"])
def bot_reply():

    if request.method == "GET":

       return render_template("index.html")



if __name__ == "__main__":
   app.run(debug=True, host="localhost", port=5000)
