from flask import Flask,render_template,request,redirect,url_for
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import re


app = Flask(__name__) 
chat_bot = ChatBot("Sid Travel Bot")

trainer = ListTrainer(chat_bot)
# trainer.train("chatterbot.corpus.english")
data = open("data/data_txt.txt" , "r").readlines()
trainer.train(data)

curOption = 1
option_dict = {
     0:"type",
     1:"date" , 
     2:["less than 3 days" , "3 - 7 days" , "more than 7 days"] ,
     3:["Chennai" , "Delhi" , "Hyderabad" ,"Mumbai" ,"Kolkata"],
     4:["Solo &#128102;" , "Couple &#128107;" , "Family &#128106;" , "&#128108; Friends &#128109;"] , 
     5:["1" , "2 - 5 " , "6 - 10" , "More than 10" ],
     6:["upto &#8377;50,000" , "&#8377;50,000 to 1 Lakh" , "Not Decided"],
     7:["Chennai" , "Delhi" , "Hyderabad" ,"Mumbai" ,"Kolkata"],
     8:["Train &#128647;" , "Bus &#128652;" , "Flight &#9992;" , "Car rental &#128661;"],
     9:"type",
     10:"type",
     11:["Plan Again"],
     12:"type"
}

response_tag = ["null","name" , "datex" , "duration" , "destination" , "travelling with" ,"members" , "budget" , "city" , "transport" , "email" , "contact" ]
mail_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
num_pattern = re.compile("[0-9]{10}")
name = "sid"
error = False
err_cur = 0

def get_btn_html(data , type="button"):
     if (type=="button"):
          return '<input type='+type+' class="btn btn-primary btn-lg btn-block" style="padding: 3% 3%;" value = "'+data+'" onclick="changeText(this.value);"/>'
     else:
          return '<input type='+type+' class="btn btn-primary btn-lg btn-block" style="padding: 3% 3%;" value = "'+data+'" onclick="changeTextDate(this.value);"/>'

def get_bot_html(data):
     bot_html=""
     if("+" in data):
          data_arr = data.split(" + ")
          bot_html = '<br><br><p class ="botText"><span class=s1_cont>' + data_arr[0] + '</span><br><br>'
          for data in data_arr[1:-1] :
               bot_html = bot_html + '<span class=s2_mid>' + data + '</span><br><br>'
          bot_html = bot_html + '<span class=s2>' + data_arr[-1] + '</span></p>'
     
     else:
          bot_html = '<br><br><p class ="botText"><span class=s1>' + data + '</span></p>'

     if ("Plan Again" in data):
          bot_html = '<p class ="botText">'
          bot_html = bot_html + '<span class="s1_cont">Hi I am Sidarth</span><br><br> <span class="s2_mid">Welcome to <b>Sid Travel Bot</b> </span><br><br>'
          bot_html = bot_html + '<span class="s2">We \'ll take you mile. . .s with smile. . .s &#128522;</span><br><br><br>'
          bot_html = bot_html + '<span class="s1_cont">Now that the long &#128274;lockdown has come to an end </span><br><br>'
          bot_html = bot_html + '<span class="s2">its time to get some fresh air !!!</span><br><br><br>'
          bot_html = bot_html + '<span class="s1_cont">Well , Let\'s start planning &#128526;</span><br><br> '
          bot_html = bot_html + '<span class="s2">May I know your name please..&#10068;</span><br></p>'     
     
     return str(bot_html) 

@app.route("/")
def index():
     return render_template("index.html")

@app.route("/get")
def get_bot_response():
     global curOption , name , error , err_cur
     print("inside bot_response ==> curOption = ",curOption)
     
     data=""
     #Some conditions directing the flow and response
     if (curOption == 1):
          name = request.args.get("msg")
          data = "Nice to meet you <b>"+name+"</b>  &#128515; + "

     if(curOption==12):
          curOption = 0
          data = data + "Plan Again "

     userText = response_tag[curOption]

     if (userText=="budget"):
          if(request.args.get("msg")=="Not Decided"):
               data = data + "Its Ok + "
          else:
               data = data + "Awesome + "
         
     if (curOption==5):
          userText = request.args.get("msg") 
          print(userText, len(userText))
          if("Friends" in userText):
               userText = userText[2:]     
          userText = userText[:-2]
          print(userText, len(userText))
          if ("Solo" in userText or "Couple" in userText):
               curOption = 6

     if(curOption==10):
          userText = request.args.get("msg")
          print(userText)
          if(re.search(mail_regex,userText)):  
               print("Valid Email")
               userText = response_tag[curOption]
               error=False
          else:  
               print("Invalid Email")  
               userText="Invalid Email"
               error=True
               err_cur = curOption
          print("error")

     if(curOption==11):
          userText = request.args.get("msg")
          if (num_pattern.match(userText)):  
               print("Valid Contact")
               userText = response_tag[curOption]
               error=False
          else:  
               print("Invalid Contact")  
               userText="Invalid Contact"
               error=True  
               err_cur = curOption  

     print(userText)
     data = data + str(chat_bot.get_response(userText))
     return get_bot_html(data)

@app.route("/getOption")
def get_cur_option():
     global curOption
     print("inside cur_Option ==> curOption = ",curOption)
     options="<br>"
     curOption_loc = curOption
     if (error):
          curOption_loc = err_cur - 1

     if (option_dict[curOption_loc]=="type"):
          pass
     elif (option_dict[curOption_loc]=="null"):
          options="null"
     elif (option_dict[curOption_loc]=="date"):
          options = options + get_btn_html(" " , type="date" )
     else :
          for opt in option_dict[curOption_loc] :
               options = options + get_btn_html(opt)
     
     options = options+"<br><br>"
     
     if(not error):
          print("moving to next conv")
          curOption = curOption_loc+1

     return str(options)

if __name__ == "__main__":
     app.run(debug = True , threaded=False)

