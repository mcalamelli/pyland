# pylint: disable=locally-disabled,missing-docstring,invalid-name,unused-variable,line-too-long
# coding: utf-8

import os.path
import sys
#import json

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = '7bb7726d99014802b5f36f9342a315c2'


def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'it'  # optional, default value equal 'en'

    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    request.query = "Grazie mille per il tuo aiuto."

    response = request.getresponse()

    print(response.read())
    #print(json.dumps(response.read(), indent=2))


if __name__ == '__main__':
    main()
