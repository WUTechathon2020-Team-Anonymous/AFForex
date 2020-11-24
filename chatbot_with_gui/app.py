from flask import Flask, render_template, request
from chatbot_with_gui.dialogflow_bot import chat,exchange

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    paramsPresent, amount, curr_from, curr_to, fulfillment_text,action = chat(userText)

    if paramsPresent == "True" and action!="input.welcome":
        rate = exchange(curr_from, curr_to)
        mystring = "Exchange rate from {} to {} is {}".format(curr_from,curr_to,rate)
        return mystring
    else:
        return fulfillment_text


if __name__ == "__main__":
    app.run()