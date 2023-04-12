# coding: utf-8




import module
import flask
from flask import Flask, render_template, request, url_for, redirect, session, flash, abort
from flask import Response as response
from datetime import timedelta




app = flask.Flask(__name__, static_folder="static", template_folder="templates")




app.config['SECRET_KEY'] = "python_flask_chatbot_main_in_session_secret_key"




@app.route("/", methods=["GET"])
@app.route("/top", methods=["GET"])
def top():
    session.clear()


    return render_template("top.html")


@app.route("/usage", methods=["GET"])
def usage():
    session.clear()


    return render_template("usage.html")


@app.route("/about", methods=["GET"])
def about():
    session.clear()


    return render_template("about.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if(request.method == "POST"):

        app.permanent_session_lifetime = timedelta(minutes=30)

        if (request.form["username"] == "root" and request.form["password"] == "root"):
            session['logged_in'] = True
            return redirect(url_for("prompt"))

        else:
            if request.form["username"] != "root":
               flash("ユーザー名が間違っています！")
               return render_template("login.html")

            if request.form["password"] != "root":
               flash("パスワードが間違っています！")
               return render_template("login.html")

    else:

        return render_template("login.html")


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()


    return render_template("logout.html")


@app.route('/prompt', methods=["GET","POST"])
def prompt():
    if request.method == "GET":

       if ('logged_in'not in session or session['logged_in'] == False):

          return redirect(url_for("login"))

       else:

          return render_template("prompt.html")


    if request.method == "POST":

       if ('logged_in'not in session or session['logged_in'] == False):

          return redirect(url_for("login"))

       if not request.form["sent_msg_txt"]:

          flash("メッセージが入力されていません！")

          return redirect(url_for("prompt"))

       if not request.files["sent_msg_img"]:

          flash("画像が指定されていません！")

          return redirect(url_for("prompt"))


       orign_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst = module.analyze_text(request.form["sent_msg_txt"])
       orign_img = module.restoration_image_from_datastream(request.files["sent_msg_img"].stream)
       anlyzd_img, img_ttl, img_dscrptn = module.analyze_image(orign_img)

       orign_img_pth  = module.generate_image_file(orign_img)
       anlyzd_img_pth = module.generate_image_file(anlyzd_img)

       cntxt, tpc, usr_info, uttrnc_mdl = module.inference_and_speculate(orign_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst, anlyzd_img, img_ttl, img_dscrptn)
       gnrtd_txts  = module.generate_text(orign_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info, uttrnc_mdl)
       lrnng_rslts = module.learning(orign_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info, uttrnc_mdl, anlyzd_img_pth, img_ttl, img_dscrptn)

       session["origin_texts"]        = orign_txts
       session["generated_texts"]     = gnrtd_txts
       session["text_mean"]           = txt_mean
       session["text_tokens"]         = txt_tkns
       session["text_sentiment"]      = txt_sntmnt
       session["text_dijest"]         = txt_djst
       session["context"]             = cntxt
       session["topic"]               = tpc
       session["user_infomation"]     = usr_info
       session["utterance_modal"]     = uttrnc_mdl
       session["origin_image_path"]   = orign_img_pth
       session["analyzed_image_path"] = anlyzd_img_pth
       session["image_title"]         = img_ttl
       session["image_description"]   = img_dscrptn
       session["learning_results"]    = lrnng_rslts

       return redirect(url_for("reply"))


@app.route("/reply", methods=["GET"])
def reply():

    if request.method == "GET":

       if ('logged_in'not in session or session['logged_in'] == False):

           return redirect(url_for("login"))

       else:

           if ("origin_texts" not in session):

               return redirect(url_for("prompt"))

           else:

               return render_template("reply.html", \
                                      origin_texts=session["origin_texts"], \
                                      generated_texts=session["generated_texts"], \
                                      text_mean=session["text_mean"], \
                                      text_tokens=session["text_tokens"], \
                                      text_sentiment=session["text_sentiment"], \
                                      text_dijest=session["text_dijest"], \
                                      context=session["context"], \
                                      topic=session["topic"], \
                                      user_infomation=session["user_infomation"], \
                                      utterance_modal=session["utterance_modal"], \
                                      origin_image_path=session["origin_image_path"], \
                                      analyzed_image_path=session["analyzed_image_path"], \
                                      image_title=session["image_title"], \
                                      image_description=session["image_description"], \
                                      learning_results=session["learning_results"])


if __name__ == '__main__':
   app.run(debug=True, host="localhost", port=5000)