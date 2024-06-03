import streamlit as st
import json
from PIL import Image
import hashlib
import time
import boto3
from boto3.dynamodb.conditions import Key


class Dynamodb:
    def __init__(self):
        self.MY_REGION = st.session_state['MY_REGION']
        self.MY_KEY_ENV = st.session_state['MY_KEY_ENV']
        self.MY_SECRET_ENV = st.session_state['MY_SECRET_ENV']
        self.conn = self.establish_connection()

    def establish_connection(self):
        sess = boto3.Session(
            aws_access_key_id=self.MY_KEY_ENV
            , aws_secret_access_key=self.MY_SECRET_ENV
            , region_name=self.MY_REGION
        )
        return sess.client('dynamodb')

    def data_upload(self, table_name, item):
        response = self.conn.put_item(
            TableName=table_name,
            Item=item
        )

    def get_data(self, table_name, key, value):
        dynamodb_client = boto3.client('dynamodb', aws_access_key_id=self.MY_KEY_ENV, aws_secret_access_key=self.MY_SECRET_ENV, region_name=self.MY_REGION)
        dynamodb = boto3.resource('dynamodb', aws_access_key_id=self.MY_KEY_ENV, aws_secret_access_key=self.MY_SECRET_ENV, region_name=self.MY_REGION)
        table = dynamodb.Table(table_name)
        response = table.query(
            KeyConditionExpression=Key(key).eq(value)
        )
        return response['Items']


def login():
    f = open('output/users.json', "r")
    users = json.loads(f.read())
    registration_1 = st.empty()
    c = registration_1.container()
    buff, col, buff2 = c.columns([1, 1.5, 1])
    st.session_state['page_start_time'] = time.time()
    with col.container():
        image = Image.open("static/images/bobo1.png")
        st.image(image)
        login_page_form = st.form('Login Page')
        login_page_form.subheader("Login Page")
        login_username = login_page_form.text_input('Username').lower()
        login_password = login_page_form.text_input('Password', type='password')
        login_password_length = len(login_password)
        login_password = login_password.encode('utf-8')
        h = hashlib.sha256(login_password)
        login_password = h.hexdigest()
        if 'login_attempt' not in st.session_state:
            st.session_state['login_attempt'] = [(login_username, login_password)]
        else:
            st.session_state['login_attempt'].append((login_username, login_password))

        if login_page_form.form_submit_button('Login'):
            dynamoz = Dynamodb()
            user_in_db = dynamoz.get_data("users", "username", login_username)
            if len(user_in_db) > 0:
                flag = False
                for item in user_in_db:
                    if item['password'] == login_password:
                        flag = True
                if flag:
                    if 'form_display' in st.session_state:
                        cookies = {}
                        to_save = {}
                        to_save['page'] = 'Login'
                        to_save['login_status'] = 'successful'
                        to_save['username'] = login_username
                        to_save['password_length'] = login_password_length
                        to_save['password_count_numeric'] = \
                            sum(1 for elem in login_password if elem.isnumeric())
                        to_save['password_count_alpha'] = \
                            sum(1 for elem in login_password if elem.isalpha())
                        to_save['password_count_uppercase'] = \
                            sum(1 for elem in login_password if elem.isupper())
                        to_save['password_count_symbols'] = \
                            len(login_password) - sum(1 for elem in login_password if elem.isalnum())
                        item = {
                            "page": {'S': 'login_phase_2'},
                            "username": {'S': str(login_username)},
                            "login_status": {'S': 'successful'},
                            "password_hashed": {'S': login_password},
                            "password_length": {'S': str(login_password_length)},
                            "password_count_numeric": {
                                'S': str(to_save['password_count_numeric'])},
                            "password_count_alpha": {'S': str(to_save['password_count_alpha'])},
                            "password_count_uppercase": {
                                'S': str(to_save['password_count_uppercase'])},
                            "password_count_symbols": {
                                'S': str(to_save['password_count_symbols'])},
                            "page_start_time": {'S': str(st.session_state['page_start_time'])},
                            "page_end_time": {'S': str(time.time())},
                            "failed_logins_password": {'S': str(st.session_state['failed_logins_password'])},
                            "failed_logins_user": {'S': str(st.session_state['failed_logins_user'])}
                        }
                        dynamoz = Dynamodb()
                        dynamoz.data_upload("logins", item)

                        st.session_state['form_display'] = 'successful_login'
                    registration_1.empty()
                    return True
                else:
                    st.session_state['failed_logins_password'] += 1
                    if st.session_state['failed_logins_password'] + st.session_state['failed_logins_user'] >= 5:
                        if 'form_display' in st.session_state:
                            cookies = {}
                            to_save = {}
                            to_save['page'] = 'Login'
                            to_save['login_status'] = 'failed'
                            to_save['username'] = login_username
                            to_save['password_length'] = len(login_password)
                            to_save['password_count_numeric'] = \
                                sum(1 for elem in login_password if elem.isnumeric())
                            to_save['password_count_alpha'] = \
                                sum(1 for elem in login_password if elem.isalpha())
                            to_save['password_count_uppercase'] = \
                                sum(1 for elem in login_password if elem.isupper())
                            to_save['password_count_symbols'] = \
                                len(login_password) - sum(1 for elem in login_password if elem.isalnum())
                            item = {
                                "page": {'S': 'login_phase_2'},
                                "username": {'S': str(login_username)},
                                "login_status": {'S': 'failed'},
                                "password_hashed": {'S': login_password},
                                "password_length": {'S': str(login_password_length)},
                                "password_count_numeric": {
                                    'S': str(to_save['password_count_numeric'])},
                                "password_count_alpha": {'S': str(to_save['password_count_alpha'])},
                                "password_count_uppercase": {
                                    'S': str(to_save['password_count_uppercase'])},
                                "password_count_symbols": {
                                    'S': str(to_save['password_count_symbols'])},
                                "page_start_time": {'S': str(st.session_state['page_start_time'])},
                                "page_end_time": {'S': str(time.time())},
                                "failed_logins_password": {'S': str(st.session_state['failed_logins_password'])},
                                "failed_logins_user": {'S': str(st.session_state['failed_logins_user'])}
                            }
                            dynamoz = Dynamodb()
                            dynamoz.data_upload("logins", item)
                            st.session_state['form_display'] = 'failed_login'
                        registration_1.empty()
                        return True
                    else:
                        st.error("Password is incorrect")
            else:
                st.session_state['failed_logins_user'] += 1
                if st.session_state['failed_logins_password'] + st.session_state['failed_logins_user'] >= 5:
                    if 'form_display' in st.session_state:
                        cookies = {}
                        to_save = {}
                        to_save['page'] = 'Login'
                        to_save['login_status'] = 'failed'
                        to_save['username'] = login_username
                        to_save['password_length'] = len(login_password)
                        to_save['password_count_numeric'] = \
                            sum(1 for elem in login_password if elem.isnumeric())
                        to_save['password_count_alpha'] = \
                            sum(1 for elem in login_password if elem.isalpha())
                        to_save['password_count_uppercase'] = \
                            sum(1 for elem in login_password if elem.isupper())
                        to_save['password_count_symbols'] = \
                            len(login_password) - sum(1 for elem in login_password if elem.isalnum())
                        item = {
                            "page": {'S': 'login_phase_2'},
                            "username": {'S': str(login_username)},
                            "login_status": {'S': 'failed'},
                            "password_hashed": {'S': login_password},
                            "password_length": {'S': str(login_password_length)},
                            "password_count_numeric": {
                                'S': str(to_save['password_count_numeric'])},
                            "password_count_alpha": {'S': str(to_save['password_count_alpha'])},
                            "password_count_uppercase": {
                                'S': str(to_save['password_count_uppercase'])},
                            "password_count_symbols": {
                                'S': str(to_save['password_count_symbols'])},
                            "page_start_time": {'S': str(st.session_state['page_start_time'])},
                            "page_end_time": {'S': str(time.time())},
                            "failed_logins_password": {'S': str(st.session_state['failed_logins_password'])},
                            "failed_logins_user": {'S': str(st.session_state['failed_logins_user'])}
                        }
                        dynamoz = Dynamodb()
                        dynamoz.data_upload("logins", item)

                        st.session_state['form_display'] = 'failed_login'
                    registration_1.empty()
                    return True
                else:
                    st.error("Username doesn't exist")
