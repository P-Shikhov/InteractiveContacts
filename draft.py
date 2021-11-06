# from django.contrib.sessions.models import Session
# from django.contrib.auth.models import User

# session_key = '9icvtnrx3fxe4ebd8ti52s3sf5lty5xi'

# session = Session.objects.get(session_key=session_key)
# # uid = session.get_decoded().get('_auth_user_id')
# uid = session.get_decoded()

# print(uid)

import pickle
import base64
import json

session_data = '9icvtnrx3fxe4ebd8ti52s3sf5lty5xi'

# data = pickle.loads(session_data.decode('base64'))
data = json.loads(session_data.decode('base64')[41:])

# data = pickle.loads(base64.decode("9icvtnrx3fxe4ebd8ti52s3sf5lty5xi"))

print(data)