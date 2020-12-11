from instamojo_wrapper import Instamojo
API_KEY="test_04d6f40897bebe960c0d2dcc939"
AUTH_TOKEN="test_72b7dd93d6738104f7e78f3c097"
api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')

# Create a new Payment Request
response = api.payment_request_create(
    amount='20',
    purpose='Testing',
    send_email=True,
    email="nidhish2801@gmail.com",
    redirect_url="http://localhost/handle_redirect.py"
    )
# print the long URL of the payment request.
print(response['payment_request']['longurl'])
# print the unique ID(or payment request ID)
print(response['payment_request']['id'])
