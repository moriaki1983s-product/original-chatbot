# coding: utf-8




import chatbot_text_analyze
import chatbot_text_generate




#当該アプリケーションのエントリィポイント
init_shw_txt = "hello! (original-chatbot)"

print(init_shw_txt)


while True:

      inpt_txt = input(' > ')

      if (inpt_txt == "exit" or inpt_txt == "close"):

          break


      txt_mean, anlyzd_tkns1, anlyzd_tkns2, txt_sntmnt, txt_djst = chatbot_text_analyze.analyze_text(inpt_txt)
      gnrtd_txt, txt_mean, anlyzd_tkns1, anlyzd_tkns2, txt_sntmnt, txt_djst, uttrnc_mdl = \
      chatbot_text_generate.generate_text(txt_mean, anlyzd_tkns1, anlyzd_tkns2, txt_sntmnt, txt_djst)

      print(gnrtd_txt)
      print(txt_mean)
      print(anlyzd_tkns1)
      print(anlyzd_tkns2)
      print(txt_sntmnt)
      print(txt_djst)
      print(uttrnc_mdl)
