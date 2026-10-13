from api.account_api import AccountAPI

account_api = AccountAPI('https://demoqa.com')

test_user = 'babenko_qa_user_1'
test_pass = 'Password123!'

create_resp = account_api.create_user(test_user, test_pass)
print(f'Create User Status: {create_resp.status_code}')
print(f'Create User Body: {create_resp.json()}')

token_resp = account_api.generate_token(test_user, test_pass)
print(f'Generate Token Status: {token_resp.status_code}')
print(f'Generate Token Body: {token_resp.json()}')
