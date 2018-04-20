from flask import jsonify, request, render_template, session
import requests
import config as conf
from . import churn
import json


@churn.route('')
def getChurn():
    return render_template('churn.html')


@churn.route('', methods=['POST'])
def submitChrun():
    parameters = request.get_json(force=True)
    print("Demo churn:", parameters)
    if request.method == 'POST':

        text = parameters['input'].lower()

        # 1. Check if still labels to do = answer is related to churn/non churn
        if 'churn' in session and len(session['churn']) != 0:
            # Compose msg to update db
            send_label(session['text'], session['lang'], session['churn'][-1][0], session['churn'][-1][1], text)
            print(session['churn'])
            session['churn'] = session['churn'][:-1]
            print(session['churn'])
        else:
            result = send_request(text)
            if result is None:
                return json.dumps({'msg': 0, 'lang': 'EN'})

            session['text'] = parameters['input']
            session['lang'] = result['lang']
            session['churn'] = result['churn']

        # 2. Check if all brand labeled
        if len(session['churn']) != 0:
            # 2.a. There are still brands to label -> send result for new tweet
            data_msg = {'lang': session['lang'], 'brand': session['churn'][-1][0], 'label': session['churn'][-1][1]}
            return json.dumps(data_msg)
        else:
            # 2.b. It was the last one. Wat for new entry
            return json.dumps({'msg': 1, 'lang': session['lang']})

        # 1. Check if need to update tweet or to process new tweet
        #
        # if 'churn' in session and len(session['churn']) != 0:
        #     # Compose msg to update db
        #     send_label(session['text'], session['lang'], session['churn'][-1][0], text)
        #     del session['churn'][-1]
        #
        #     # 1.a. Check if all brand labeled
        #     if len(session['churn']) != 0:
        #         # 1.a.1. There are still brands to label -> send result for new tweet
        #         data_msg = {'lang': session['lang'], 'brand': session['churn'][-1][0], 'label': session['churn'][-1][1]}
        #         return json.dumps(data_msg)
        #     else:
        #         # 1.a.2. It was the last one. Wat for new entry
        #         return json.dumps({'msg': 'All brands detected, please enter a new sentence'})
        #
        # # 2. Process new text
        # else:
        #     result = send_request(text)
        #     if result is None:
        #         return json.dumps({'msg': 'Unable to process the tweet ... please try again later'})
        #
        #     session['text'] = parameters['input']
        #     session['lang'] = result['lang']
        #     session['churn'] = result['churn']

        # try:
        #     # data = json.dumps({'text': parameters['input'].lower()})
        #     data = json.dumps({'text': 'hello bitches', 'lang': 'en', 'brand': 'Swisscom', 'label': 'non'})
        #     response = requests.post(conf.churn['api_url'] + 'churn_label', data=data)
        #     # response = requests.post(conf.churn['api_url'], data=data)
        #     result = json.loads(response.text)
        # except Exception as e:
        #     result = {'lang': 'FR', 'churn_b': ['swisscom'], 'nochurn_b': ['salt', 'sunrise']}
        #
        # return jsonify(result)


def send_request(text):
    try:
        data = json.dumps({'text': text.lower()})
        print(data)
        response = requests.post(conf.churn['api_url'] + 'process', data=data)
        return json.loads(response.text)
    except Exception as e:
        print('Error:', e)
        return None


def send_label(text, lang, brand, label, cgt):
    try:
        data = {'text': text, 'lang': lang, 'brand': brand, 'label': label, 'cgt': cgt}
        requests.post(conf.churn['api_url'] + 'churn_label', data=json.dumps(data))
    except Exception as e:
        print('Error:', e)
    return