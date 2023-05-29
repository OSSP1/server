import test
from flask import Flask, request, render_template
from flask_cors import CORS

application = Flask(__name__)
CORS(application) # apply CORS on all routes

@application.route("/")
def hello():
    return "Hello JEJU!"

@application.route("/translation", methods=["GET", "POST"])
def translation():
    form_data = request.get_json()
    
    response = {}

    if request.method == "POST":
        text = form_data["text"]

        if form_data["button"] == "s2d":
            answer = test.s2d(text)
            response["result_text"]= answer
            return response
        
        if form_data["button"] == "d2s":
            answer = test.d2s(text)
            response["result_text"]= answer
            return response

    return render_template("testpage.html", title="testpage")

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, threaded=True)
