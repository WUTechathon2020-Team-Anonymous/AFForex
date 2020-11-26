import os
import dialogflow_v2 as dialogflow
import requests
from google.api_core.exceptions import InvalidArgument
from django.conf import settings

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(settings.BASE_DIR, 'Resources/private_key.json')

DIALOGFLOW_PROJECT_ID = 'afforex-gsnn'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'

def exchange(from_currency,to_currency):
    # Where USD is the base currency you want to use

    url = 'https://v6.exchangerate-api.com/v6/a88c3104a088a837bd097063/latest/%s' % from_currency

    # Making our request
    response = requests.get(url)
    data = response.json()

    return str(data['conversion_rates'][to_currency])



def chat(msg):
    text_to_be_analyzed = msg

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    # print("Query text:", response.query_result.query_text)
    # print("Detected intent:", response.query_result.intent.display_name)
    # print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    # print("Fulfillment text:", response.query_result.fulfillment_text)
    # print(response)
    paramsPresent = str(response.query_result.all_required_params_present)
    amount = str(response.query_result.parameters.fields["amount"].number_value)
    curr_from = str(response.query_result.parameters.fields["currency-from"].string_value)
    curr_to = str(response.query_result.parameters.fields["currency-to"].string_value)
    fulfillment_text = str(response.query_result.fulfillment_text)
    action = str(response.query_result.action)

    if amount == "0.0":
        amount = ""

    return paramsPresent, amount, curr_from, curr_to, fulfillment_text,action