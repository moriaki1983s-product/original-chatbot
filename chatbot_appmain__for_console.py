# coding: utf-8




import chatbot_text_analyze
import chatbot_text_generate




#当該アプリケーションのエントリィポイント
init_shw_txt = ">hello! (original-chatbot)"

print(init_shw_txt)


while True:

      inpt_txt = input(' > ')

      if (inpt_txt == "exit" or inpt_txt == "close"):

          break

      origin_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info = chatbot_text_analyze.analyze_text(inpt_txt)
      origin_txts, gnrtd_txt, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info, uttrnc_mdl = \
      chatbot_text_generate.generate_text(origin_txts, txt_mean, txt_tkns, txt_sntmnt, txt_djst, cntxt, tpc, usr_info)

      print(origin_txts)
      print(gnrtd_txt)
      print(txt_mean)
      print(txt_tkns)
      print(txt_sntmnt)
      print(txt_djst)
      print(cntxt)
      print(tpc)
      print(usr_info)
      print(uttrnc_mdl)
