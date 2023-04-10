from flask import Flask, render_template
import yaml
import json
import base64
import gzip
app = Flask(__name__)


@app.route('/')
def index():
  with open('openai_call.yaml') as f:
    data = yaml.safe_load(f)

  interactions = []
  for interaction in data['interactions']:
    request_body = json.loads(interaction['request']['body'])
    # extract response body string as bytes which are gzip compressed json string

    response_json = json.loads(gzip.decompress(interaction['response']['body']['string']))

    model = request_body.get('model', '')
    messages = request_body.get('messages', [])
    print(messages)
    interactions.append({
      'model': model,
      'message': messages[0],
      'response': response_json['choices'][0]['message']['content'],
    })

  return render_template('index.html', interactions=interactions)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=8080)
