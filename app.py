from flask import Flask, render_template, request, jsonify

from chatbot import get_response
from chatbot import chatbot_respond   # boss 10.23
#from chatbot import find_pdfResource   # boss 10.23
from chatbot import video_search   # boss 10.23

app = Flask(__name__)
from flask_cors import CORS

CORS(app)

@app.get("/")
def index_get():
    return render_template("index.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


@app.route('/respond', methods=['POST', 'GET'])
#@jwt_required()
def reply():
    response = "NO RESPONSE!"
    if request.method == "POST":
        user_query = request.json.get("text")
        lang = request.json.get("lang")
        state = request.json.get("state") # initial value = None
        lang = 'en'
        #result, related_questions = chatbot.respond(user_query,lang)
        result, related_questions = chatbot_respond(user_query,lang)  # boss 10.23
        response = result.replace('\n','<br />').strip()
        #pdfResponse = find_pdfResource(user_query)
        videoResponse = video_search(user_query,lang)

    xResponse = {}

    xResponse["answer"] = response
    xResponse['related_questions'] = related_questions if related_questions is not None else ''
    xResponse["pdfSrc"] = "" # pdfResponse["pdfSrc"]
    xResponse["pdfTitle"] = "" # pdfResponse["pdfTitle"]
    xResponse["videoSrc"] = videoResponse
    
    return jsonify(xResponse), 200


# @app.route('/getvideo', methods=['POST'])
# #@jwt_required()
# def send_video():
#     response = "NO RESPONSE!"
#     if request.method == "POST":
#         text = request.json.get("text")
#         lang = request.json.get("lang")
#         state = request.json.get("state") # initial value = None
#     try:
#         video = get_voice(text,
#             lang=lang.strip(),
#             encoding='wav',gender="M"
#         )
#         if lang == 'ar': get_video(text)
#         return send_file("output_video.mp4", attachment_filename='output.mp4', mimetype="video/mp4"),200
#     except:
#         return None

#     return None

# @app.route("/gettext",methods=['POST'])
# #@jwt_required()
# def reply_text():
#     if request.method == "POST":
#         save_path = os.path.join('uploads','mic_signal.wav')
#         #print('save path: ',save_path)
#         lang = request.form.get('lang')

#         request.files['audio_data'].save(save_path)

#         text = get_text(save_path, lang)
        
#     return jsonify({"text": text }), 200


if __name__ == "__main__":
    app.run(debug=True) 