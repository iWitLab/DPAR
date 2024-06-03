import streamlit as st
from PESrank import mainModel
from PIL import Image
import time
import boto3
import logging
import hashlib
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


def register():
    try:
        st.session_state['page_start_time'] = time.time()
        placeholder = st.empty()
        with placeholder.container():
            col1, col2, = st.columns(2)
            with col1:
                image = Image.open("static/images/bobo1.png")
                st.image(image)
                register_user_form = st.form('Registration Form')
                register_user_form.subheader("Registration Form")
                new_username = register_user_form.text_input('Username',
                                                             value=st.session_state['username_value']).lower()
                new_password = register_user_form.text_input('Password', type='password',
                                                             value=st.session_state['password_value'])
                new_password_repeat = register_user_form.text_input('Repeat password', type='password',
                                                                    value=st.session_state['password2_value'])
                pressed = register_user_form.form_submit_button('Continue')
                new_password1 = new_password.encode('utf-8')
                h = hashlib.sha256(new_password1)
                hashed_password = h.hexdigest()
                if pressed:
                    if len(new_username) * len(new_password) * len(new_password_repeat) > 0:
                        if new_password == new_password_repeat:
                            with st.spinner('Processing your information...'):
                                dynamoz = Dynamodb()
                                user_in_db = dynamoz.get_data("users", "username", new_username)
                            if len(user_in_db) == 0:
                                if len(new_password) >= 8:
                                    if str.isascii(new_password):
                                        if any(i.isdigit() for i in new_password) and any(i.isalpha() for i in new_password):
                                            try:
                                                to_save = {}
                                                model_ui = {}
                                                model_run = {}
                                                with st.spinner('Processing your information...'):
                                                    ui_results, model_results = mainModel.main(new_username, new_password)
                                                st.session_state['ui_results'] = ui_results
                                                st.session_state['model_results'] = model_results
                                                st.session_state['username_value'] = new_username
                                                st.session_state['password_value'] = new_password
                                                st.session_state['password2_value'] = new_password_repeat
                                                to_save['page'] = 'Register1'
                                                to_save['username'] = new_username
                                                to_save['password_length'] = len(new_password)
                                                to_save['password_count_numeric'] = \
                                                    sum(1 for elem in new_password if elem.isnumeric())
                                                to_save['password_count_alpha'] = \
                                                    sum(1 for elem in new_password if elem.isalpha())
                                                to_save['password_count_uppercase'] = \
                                                    sum(1 for elem in new_password if elem.isupper())
                                                to_save['password_count_symbols'] = \
                                                    len(new_password) - sum(1 for elem in new_password if elem.isalnum())
                                                model_ui['password_strength'] = ui_results['password_strength']
                                                model_ui['password_percentile'] = ui_results['password_percentile']
                                                model_ui['hack_time'] = ui_results['hack_time']
                                                model_ui['hack_unit'] = ui_results['hack_unit']
                                                model_ui['rec_lev_1'] = ui_results['rec_lev_1']
                                                model_ui['pass_1'] = ui_results['pass_1']
                                                model_ui['bits_1'] = ui_results['bits_1']
                                                model_ui['hack_time_1'] = ui_results['hack_time_1']
                                                model_ui['hack_unit_1'] = ui_results['hack_unit_1']
                                                model_ui['rec_lev_2'] = ui_results['rec_lev_2']
                                                model_ui['pass_2'] = ui_results['pass_2']
                                                model_ui['bits_2'] = ui_results['bits_2']
                                                model_ui['hack_time_2'] = ui_results['hack_time_2']
                                                model_ui['hack_unit_2'] = ui_results['hack_unit_2']
                                                model_ui['rec_lev_3'] = ui_results['rec_lev_3']
                                                model_ui['pass_3'] = ui_results['pass_3']
                                                model_ui['bits_3'] = ui_results['bits_3']
                                                model_ui['hack_time_3'] = ui_results['hack_time_3']
                                                model_ui['hack_unit_3'] = ui_results['hack_unit_3']
                                                model_run['modelRank'] = model_results['modelRank']
                                                model_run['modelProb'] = model_results['modelProb']
                                                model_run['prefixProb'] = model_results['prefixProb']
                                                model_run['baseProb'] = model_results['baseProb']
                                                model_run['suffixProb'] = model_results['suffixProb']
                                                model_run['l33tProb'] = model_results['l33tProb']
                                                model_run['upperProb'] = model_results['upperProb']
                                                model_run['finalPrefix_length'] = str(len(model_results['finalPrefix']))
                                                model_run['finalunL33tBaseWord_length'] = \
                                                    str(len(model_results['finalunL33tBaseWord']))
                                                model_run['finalSuffix_length'] = len(model_results['finalSuffix'])
                                                model_run['l33tList'] = model_results['l33tList']
                                                model_run['upperList'] = model_results['upperList']
                                                model_run['nonePrefixProbFlag'] = model_results['nonePrefixProbFlag']
                                                model_run['noneBaseProbFlag'] = model_results['noneBaseProbFlag']
                                                model_run['noneSuffixProbFlag'] = model_results['noneSuffixProbFlag']
                                                model_run['noneL33tProbFlag'] = model_results['noneL33tProbFlag']
                                                model_run['noneUpperProbFlag'] = model_results['noneUpperProbFlag']
                                                model_run['bits'] = model_results['bits']
                                                model_run['percentile'] = model_results['percentile']
                                                model_run['recommendation_1'] = model_results['1']
                                                model_run['recommendation_2'] = model_results['2']
                                                model_run['recommendation_3'] = model_results['3']
                                                model_run['recommendation_4'] = model_results['4']
                                                model_run['recommendation_5'] = model_results['5']
                                                model_run['recommendation_6'] = model_results['6']
                                                model_run['recommendation_7'] = model_results['7']
                                                item = {
                                                    "page": {'S': 'register1'},
                                                    "username": {'S': str(new_username)},
                                                    "hashed_password": {'S': str(hashed_password)},
                                                    "password_length": {'S': str(len(new_password))},
                                                    "password_count_numeric": {
                                                        'S': str(to_save['password_count_numeric'])},
                                                    "password_count_alpha": {'S': str(to_save['password_count_alpha'])},
                                                    "password_count_uppercase": {
                                                        'S': str(to_save['password_count_uppercase'])},
                                                    "password_count_symbols": {
                                                        'S': str(to_save['password_count_symbols'])},
                                                    "model_run_modelRank": {'S': str(model_run['modelRank'])},
                                                    "model_run_modelProb": {'S': str(model_run['modelProb'])},
                                                    "model_run_prefixProb": {'S': str(model_run['prefixProb'])},
                                                    "model_run_baseProb": {'S': str(model_run['baseProb'])},
                                                    "model_run_suffixProb": {'S': str(model_run['suffixProb'])},
                                                    "model_run_l33tProb": {'S': str(model_run['l33tProb'])},
                                                    "model_run_upperProb": {'S': str(model_run['upperProb'])},
                                                    "model_run_finalPrefix_length": {
                                                        'S': str(model_run['finalPrefix_length'])},
                                                    "model_run_finalunL33tBaseWord_length": {
                                                        'S': str(model_run['finalunL33tBaseWord_length'])},
                                                    "model_run_finalSuffix_length": {
                                                        'S': str(model_run['finalSuffix_length'])},
                                                    "model_run_l33tList": {'S': str(model_run['l33tList'])},
                                                    "model_run_upperList": {'S': str(model_run['upperList'])},
                                                    "model_run_nonePrefixProbFlag": {
                                                        'S': str(model_run['nonePrefixProbFlag'])},
                                                    "model_run_noneBaseProbFlag": {
                                                        'S': str(model_run['noneBaseProbFlag'])},
                                                    "model_run_noneSuffixProbFlag": {
                                                        'S': str(model_run['noneSuffixProbFlag'])},
                                                    "model_run_noneL33tProbFlag": {
                                                        'S': str(model_run['noneL33tProbFlag'])},
                                                    "model_run_noneUpperProbFlag": {
                                                        'S': str(model_run['noneUpperProbFlag'])},
                                                    "model_run_bits": {'S': str(model_run['bits'])},
                                                    "model_run_percentile": {'S': str(model_run['percentile'])},
                                                    "model_run_recommendation_1": {
                                                        'S': str(model_run['recommendation_1'])},
                                                    "model_run_recommendation_2": {
                                                        'S': str(model_run['recommendation_2'])},
                                                    "model_run_recommendation_3": {
                                                        'S': str(model_run['recommendation_3'])},
                                                    "model_run_recommendation_4": {
                                                        'S': str(model_run['recommendation_4'])},
                                                    "model_run_recommendation_5": {
                                                        'S': str(model_run['recommendation_5'])},
                                                    "model_run_recommendation_6": {
                                                        'S': str(model_run['recommendation_6'])},
                                                    "model_run_recommendation_7": {
                                                        'S': str(model_run['recommendation_7'])},
                                                    "model_ui_password_strength": {
                                                        'S': str(model_ui['password_strength'])},
                                                    "model_ui_password_percentile": {
                                                        'S': str(model_ui['password_percentile'])},
                                                    "model_ui_hack_time": {'S': str(model_ui['hack_time'])},
                                                    "model_ui_hack_unit": {'S': str(model_ui['hack_unit'])},
                                                    "model_ui_rec_lev_1": {'S': str(model_ui['rec_lev_1'])},
                                                    "model_ui_pass_1": {'S': str(model_ui['pass_1'])},
                                                    "model_ui_bits_1": {'S': str(model_ui['bits_1'])},
                                                    "model_ui_hack_time_1": {'S': str(model_ui['hack_time_1'])},
                                                    "model_ui_hack_unit_1": {'S': str(model_ui['hack_unit_1'])},
                                                    "model_ui_rec_lev_2": {'S': str(model_ui['rec_lev_2'])},
                                                    "model_ui_pass_2": {'S': str(model_ui['pass_2'])},
                                                    "model_ui_bits_2": {'S': str(model_ui['bits_2'])},
                                                    "model_ui_hack_time_2": {'S': str(model_ui['hack_time_2'])},
                                                    "model_ui_hack_unit_2": {'S': str(model_ui['hack_unit_2'])},
                                                    "model_ui_rec_lev_3": {'S': str(model_ui['rec_lev_3'])},
                                                    "model_ui_pass_3": {'S': str(model_ui['pass_3'])},
                                                    "model_ui_bits_3": {'S': str(model_ui['bits_3'])},
                                                    "model_ui_hack_time_3": {'S': str(model_ui['hack_time_3'])},
                                                    "model_ui_hack_unit_3": {'S': str(model_ui['hack_unit_3'])},
                                                    "registration1_start_time": {'S': str(st.session_state['page_start_time'])},
                                                    "model_ui_screen_1": {'S': str(ui_results['screen_1'])},
                                                    "model_ui_screen_2": {'S': str(ui_results['screen_2'])},
                                                    "model_ui_screen_3": {'S': str(ui_results['screen_3'])},
                                                    "experiment_group": {
                                                        'S': str(st.session_state['experiment_group'])},
                                                    "page_start_time": {'S': str(st.session_state['page_start_time'])},
                                                    "page_end_time": {'S': str(time.time())}
                                                }
                                                dynamoz = Dynamodb()
                                                dynamoz.data_upload("pesrank", item)
                                                placeholder.empty()
                                                if model_run['bits'] >= 54:
                                                    st.session_state['experiment_group'] = 5
                                                st.session_state['form_display'] = 'register2'
                                                return True
                                            except Exception as e:
                                                logging.error('Error at %s', 'division', exc_info=e)
                                                st.error("We apologize, there's an error")
                                                st.error('The Error is ' + str(e))

                                        else:
                                            st.error('Your password must contain at least 1 letter and at least 1 digit')
                                    else:
                                        not_ascii = []
                                        for char in new_password:
                                            if not str.isascii(char):
                                                not_ascii.append(char)
                                        not_ascii_to_print = ','.join(not_ascii)
                                        st.error('Please avoid using these characters: ' + str(not_ascii_to_print))
                                else:
                                    st.error('Your password must contain at least 8 characters')
                            else:
                                st.error('Username already taken, please choose a new username')
                        else:
                            st.error('Mismatch between entered passwords!')
                    else:
                        st.error('Please complete the registration form')

            with col2:
                st.markdown('''<br><br><br><p class="lead">Welcome to IWiT Lab registration form</p><br>''',
                            unsafe_allow_html=True)
                st.subheader("Your password must:")
                st.markdown("<br>", unsafe_allow_html=True)
                st.text("# Contain at least 8 characters")
                st.markdown("<br>", unsafe_allow_html=True)
                st.text("# Contain at least 1 letter and at least 1 digit")

    except Exception as e:
        st.error(e)
