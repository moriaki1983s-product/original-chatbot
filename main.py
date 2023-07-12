# coding: utf-8




import module
import flask
import sqlite3
import datetime
import pytz
from datetime import timedelta
from flask import Flask, render_template, request, url_for, redirect, session, flash, abort




app = flask.Flask(__name__, static_folder="static", template_folder="templates")

app.config["SECRET_KEY"] = "python_flask_chatbot__session_secret_key"








@app.route("/",      methods=["GET"])
@app.route("/index", methods=["GET"])
def index():

    session.clear()


    return render_template("index.html")




@app.route("/usage", methods=["GET"])
def usage():

    session.clear()


    return render_template("usage.html")




@app.route("/about", methods=["GET"])
def about():

    session.clear()


    return render_template("about.html")




@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

       conn = sqlite3.connect("app_db.db")
       cur  = conn.cursor()


       sql1 = """CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                   usr_nm TEXT NOT NULL, ml_addr TEXT NOT NULL, psswrd TEXT NOT NULL);"""
       cur.execute(sql1)
       conn.commit()


       sql2 = """SELECT usr_nm FROM users WHERE usr_nm=?;"""
       cur.execute(sql2, [request.form["username"]])

       for row in cur.fetchall():
           if row == (request.form["username"],):
              flash("そのユーザー名は既に登録されています！")
              cur.close()
              conn.close()

              return render_template("signup.html")


       sql2 = """INSERT INTO users(usr_nm, ml_addr, psswrd) VALUES (?, ?, ?);"""
       cur.execute(sql2, (request.form["username"], request.form["mailaddress"], request.form["password"]))
       conn.commit()

       cur.close()
       conn.close()


       session["logged_in"] = True
       app.permanent_session_lifetime = timedelta(minutes=30)


       return redirect(url_for("prompt"))


    else:


       return render_template("signup.html")




@app.route("/signout", methods=["GET", "POST"])
def signout():
    if request.method == "POST":

       conn = sqlite3.connect("app_db.db")
       cur  = conn.cursor()


       sql1 = """DELETE FROM users WHERE usr_nm=? AND ml_addr=? AND psswrd=?;"""
       cur.execute(sql1, (request.form["username"], request.form["mailaddress"], request.form["password"]))
       conn.commit()

       cur.close()
       conn.close()

       session.clear()

       return render_template("byebye.html")


    else:


         return render_template("signout.html")




@app.route("/login", methods=["GET", "POST"])
def login():
    row_num = 0


    if   request.method == "POST":

         conn = sqlite3.connect("app_db.db")
         cur  = conn.cursor()

         sql1 = """CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                     usr_nm TEXT NOT NULL, ml_addr TEXT NOT NULL, psswrd TEXT NOT NULL);"""
         cur.execute(sql1)
         conn.commit()


         sql2 = """SELECT usr_nm FROM users WHERE usr_nm=?;"""
         cur.execute(sql2, [request.form["username"]])

         for row in cur.fetchall():
             row_num = row_num + 1

         if row_num == 0:
            flash("そのユーザー名は登録されていません！")
            cur.close()
            conn.close()

            return render_template("login.html")


         sql3 = """SELECT usr_nm FROM users WHERE usr_nm=?;"""
         cur.execute(sql3, [request.form["password"]])

         for row in cur.fetchall():
             if row != request.form["password"]:
                flash("そのパスワードは間違っています！")
                cur.close()
                conn.close()

                return render_template("login.html")

         cur.close()
         conn.close()


         session["logged_in"] = True
         app.permanent_session_lifetime = timedelta(minutes=30)


         return redirect(url_for("prompt"))


    else:

         return render_template("login.html")




@app.route("/logout", methods=["GET"])
def logout():

    session.clear()


    return render_template("logout.html")




@app.route("/show_users", methods=["GET"])
def show_users():
    itms1 = []
    itms2 = []


    if  "logged_in" not in session:
         if session["logged_in"] == False:

            return redirect(url_for("login"))

    conn = sqlite3.connect("app_db.db")
    cur  = conn.cursor()


    sql1 = """SELECT * From users;"""
    cur.execute(sql1)

    for row in cur.fetchall():
        itms1.append(row)


    cur.close()
    conn.close()


    return render_template("show_users.html", items1=itms1)




@app.route("/prompt", methods=["GET", "POST"])
def prompt():
    if request.method == "GET":

       if  "logged_in" not in session:
            if session["logged_in"] == False:

               return redirect(url_for("login"))
       else:
               return render_template("prompt.html")


    if request.method == "POST":

       if ("logged_in" not in session and session["logged_in"] == False):

           return redirect(url_for("login"))


       orign_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst = module.analyze_text(request.form["sent_msg_txt"])
       orign_img = module.restoration_image_from_datastream(request.files["sent_msg_img"].stream)
       anlyzd_img, img_ttl, img_dscrptn = module.analyze_image(orign_img)
       gnrtd_img                        = module.generate_image(anlyzd_img)
       orign_img_pth = module.generate_image_file(orign_img, "(O)")
       gnrtd_img_pth = module.generate_image_file(gnrtd_img, "(A)")
       cntxt, tpc, usr_info, uttrnc_mdl = module.inference_and_speculate(orign_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst, anlyzd_img, img_ttl, img_dscrptn)
       gnrtd_txts  = module.generate_text(orign_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info, uttrnc_mdl)
       lrnng_rslts = module.learning(orign_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info, uttrnc_mdl, gnrtd_img_pth, img_ttl, img_dscrptn)

       session["origin_texts"]         = orign_txts
       session["generated_texts"]      = gnrtd_txts
       session["text_mean"]            = txt_mean
       session["text_tokens"]          = txt_tkns
       session["text_sentiment"]       = txt_sntmnt
       session["text_dijest"]          = txt_djst
       session["context"]              = cntxt
       session["topic"]                = tpc
       session["user_infomation"]      = usr_info
       session["utterance_modal"]      = uttrnc_mdl
       session["origin_image_path"]    = orign_img_pth
       session["generated_image_path"] = gnrtd_img_pth
       session["image_title"]          = img_ttl
       session["image_description"]    = img_dscrptn
       session["learning_results"]     = lrnng_rslts


       return redirect(url_for("reply"))




@app.route("/reply", methods=["GET"])
def reply():
    if request.method == "GET":

       if  "logged_in" not in session:
            if session["logged_in"] == False:

               return redirect(url_for("login"))

       else:

            if "origin_texts" not in session:

                return redirect(url_for("prompt"))

            else:

                return render_template("reply.html", \
                                        origin_texts         = session["origin_texts"], \
                                        generated_texts      = session["generated_texts"], \
                                        text_mean            = session["text_mean"], \
                                        text_tokens          = session["text_tokens"], \
                                        text_sentiment       = session["text_sentiment"], \
                                        text_dijest          = session["text_dijest"], \
                                        context              = session["context"], \
                                        topic                = session["topic"], \
                                        user_infomation      = session["user_infomation"], \
                                        utterance_modal      = session["utterance_modal"], \
                                        origin_image_path    = session["origin_image_path"], \
                                        generated_image_path = session["generated_image_path"], \
                                        image_title          = session["image_title"], \
                                        image_description    = session["image_description"], \
                                        learning_results     = session["learning_results"])








if __name__ == '__main__':
   app.run(debug=True, host="localhost", port=5000)