# coding: utf-8








import chatbot_module








#当該アプリケーションのエントリィポイント
init_shw_txt = "hello! (original-chatbot)"
print(init_shw_txt)

while True:
      inpt_txt = input(' > ')
      if (inpt_txt == "exit" or inpt_txt == "close"):
          break

      txt_mean, anlyzd_txt, anlyzd_txt2 = chatbot_module.analyze_text(inpt_txt)
      txt_mean, anlyzd_txt, anlyzd_txt2 = chatbot_module.generate_text(txt_mean, anlyzd_txt, anlyzd_txt2)
      print(txt_mean)
      print(anlyzd_txt)
      print(anlyzd_txt2)