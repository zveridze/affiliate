def test_register(setup):
    rv = setup.post('/register', data=dict(email='test@mail.ru',
                                           password=123,
                                           password2=123), follow_redirects=True)
    assert rv.status == '200 OK'
    assert b'Registration completed successfully' in rv.data


def test_login(setup):
    rv = setup.post('/login', data=dict(email='test@mail.ru',
                                        password=123), follow_redirects=True)
    assert rv.status == '200 OK'
    assert b'Logout' in rv.data
