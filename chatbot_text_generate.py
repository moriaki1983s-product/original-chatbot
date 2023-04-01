# coding: utf-8




#モジュールの読み込み
import random




#返信・返答テキストを生成する。
def generate_text(txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info):
    uttrnc_mdl = "発話モーダル:実装予定"


    sntmnt_cnddt = ["JOY", "ANGER", "PITY", "COMFORT", "MIXED", "NEUTRAL"]

    sntmnt = random.choice(sntmnt_cnddt)


    if sntmnt == "JOY":
       gnrtd_txt_cnddt = ["お世話になってます♪", "またまた～♪"]
       gnrtd_txt = random.choice(gnrtd_txt_cnddt)

    if sntmnt == "ANGER":
       gnrtd_txt_cnddt = ["それで？", "何が言いたいの？"]
       gnrtd_txt = random.choice(gnrtd_txt_cnddt)

    if sntmnt == "PITY":
       gnrtd_txt_cnddt = ["ええと・・・", "・・・"]
       gnrtd_txt = random.choice(gnrtd_txt_cnddt)

    if sntmnt == "COMFORT":
       gnrtd_txt_cnddt = ["くつろいでね", "元気でね"]
       gnrtd_txt = random.choice(gnrtd_txt_cnddt)

    if sntmnt == "MIXED":
       gnrtd_txt_cnddt = ["どうしたらいいですか？", "オロオロ 汗"]
       gnrtd_txt = random.choice(gnrtd_txt_cnddt)

    if sntmnt == "NEUTRAL":
       gnrtd_txt_cnddt = ["どうしました？", "お元気そうで"]
       gnrtd_txt = random.choice(gnrtd_txt_cnddt)


    return txts, gnrtd_txt, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info, uttrnc_mdl
