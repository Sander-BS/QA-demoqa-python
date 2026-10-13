def test_create_and_auth_user(api_user):
    assert api_user['user_id'] is not None
    assert api_user['token'] is not None
    assert api_user['username'].startswith('qa_user_')
