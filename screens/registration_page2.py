from PIL import Image
import time
from PESrank import mainModel
import hashlib
import hydralit_components as hc
from contextlib import contextmanager
import streamlit as st
import streamlit.components.v1 as components
from st_click_detector import click_detector
import json
import boto3
from boto3.dynamodb.conditions import Key

hc.hydralit_experimental(True)


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


def register2():
    def is_open():
        return st.session_state.get('modal_is_open', False)

    def open_xd():
        st.session_state.modal_is_open = True
        st.experimental_rerun()

    def close():
        st.session_state.modal_is_open = False
        st.experimental_rerun()

    @contextmanager
    def container(title=None, padding=100):
        st.markdown(
            """
            <style>
            div[data-modal-container='true'] {
                position: fixed;
                z-index: 1001;
            }

            div[data-modal-container='true'] h1 a {
                display: none
            }

            div[data-modal-container='true']::before {
                    position: fixed;
                    content: ' ';
                    left: 0;
                    right: 0;
                    top: 0;
                    bottom: 0;
                    z-index: 1000;
                    background-color: rgba(0, 0, 0, 0.5);
                    vertical-align: center;
                    horizontal-align: center;
            }
            div[data-modal-container='true'] > div:first-child > div:first-child {
                width: unset !important;
                background-color: #ffff;     
                margin: auto;
                padding: 30px;
                margin-top: 30px;
                margin-left: 30px;
                margin-bottom: 30px;
                z-index: 1001;
                border-radius: 5px;
                vertical-align: middle;
            }
            div[data-modal-container='true'] > div > div:nth-child(2)  {
                z-index: 1003;
                position: absolute;
                vertical-align: middle;
            }
            div[data-modal-container='true'] > div > div:nth-child(2) > div {
                text-align: right;
                vertical-align: middle;
            }
            div[data-modal-container='true'] > div > div:nth-child(2) > div > button {
                width: 60px;
                background: #6c757d;
            }
            ::-webkit-scrollbar {
                background: transparent;
                color: transparent;
                border-radius: 200px;
                height: 100px;
                width: 250px;
            }
            # .modal {
            #     position: fixed;
            #     top: 100;
            #     right: 0;
            #     bottom: 100;
            #     left: 10;
            #     z-index: 1040;
            #     display: none;
            #     overflow: hidden;
            #     -webkit-overflow-scrolling: touch;
            #     outline: 0;
            # }
            # .modal-header {
            #     min-height: 16.43px;
            #     padding: 15px;
            #     border-bottom: 1px solid #e5e5e5;
            # }
            # .modal-footer {
            #     padding: 15px;
            #     text-align: right;
            #     border-top: 1px solid #e5e5e5;
            # }
            # .modal-backdrop.in {
            #     filter: alpha(opacity=50);
            #     opacity: .5;
            # }
            # .modal-backdrop.fade {
            #     filter: alpha(opacity=0);
            #     opacity: 0;
            # }
            # .modal-backdrop {
            #     position: fixed;
            #     top: 0;
            #     right: 0;
            #     bottom: 0;
            #     left: 0;
            #     background-color: #000;
            # }
            </style>
            """,
            unsafe_allow_html=True
        )
        with st.container():
            _container = st.container()
            if title:
                _container.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)

            # close_ = st.button('Cancel')
            # if close_:
            #     close()

        components.html(
            """
            <script>
            // MODAL
            const iframes = parent.document.body.getElementsByTagName('iframe');
            let container
            for(const iframe of iframes)
            {
              if (iframe.srcdoc.indexOf("MODAL") !== -1) {
                container = iframe.parentNode.previousSibling;
                container.setAttribute('data-modal-container', 'true');
              }
            }
            </script>
            """,
            height=0, width=0
        )

        with _container:
            yield _container

    try:
        placeholder2 = st.empty()
        st.session_state['page_start_time'] = time.time()
        with placeholder2.container():
            col1, col2, = st.columns(2)
            with col1:
                image = Image.open("static/images/bobo1.png")
                st.image(image)
                register_user_form1 = st.form('Registration Form 1')
                register_user_form1.subheader("Registration Form")
                new_username = register_user_form1.text_input('Username',
                                                              value=st.session_state['username_value']).lower()
                if st.session_state['password_flag']:
                    new_password = register_user_form1.text_input('Password', value=st.session_state['password_value'])
                else:
                    new_password = register_user_form1.text_input('Password', type='password',
                                                                  value=st.session_state['password_value'])
                new_password_repeat = register_user_form1.text_input('Repeat password', type='password',
                                                                     value=st.session_state['password2_value'])
                pressed = register_user_form1.form_submit_button('Register')
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
                                                cookies = {}
                                                to_save = {}
                                                known_passes = [st.session_state['register_1_password'],
                                                                st.session_state['ui_results']['pass_1'],
                                                                st.session_state['ui_results']['pass_2'],
                                                                st.session_state['ui_results']['pass_3']]
                                                if new_password in known_passes:
                                                    to_save['page'] = 'Register2'
                                                    to_save['username'] = new_username
                                                    to_save['password_length'] = len(new_password)
                                                    to_save['password_count_numeric'] = \
                                                        sum(1 for elem in new_password if elem.isnumeric())
                                                    to_save['password_count_alpha'] = \
                                                        sum(1 for elem in new_password if elem.isalpha())
                                                    to_save['password_count_uppercase'] = \
                                                        sum(1 for elem in new_password if elem.isupper())
                                                    to_save['password_count_symbols'] = \
                                                        len(new_password) - sum(
                                                            1 for elem in new_password if elem.isalnum())
                                                    if 'register_2_password' in st.session_state:
                                                        st.session_state['register_2_password'] = new_password
                                                    temp_dict = {}
                                                    new_password1 = new_password.encode('utf-8')
                                                    h = hashlib.sha256(new_password1)
                                                    temp_dict[new_username] = h.hexdigest()
                                                    st.session_state['users'].update(temp_dict)
                                                    with open('output/users.json', 'w') as f:
                                                        json.dump(st.session_state['users'], f)
                                                    item = {
                                                        "page": {'S': 'register2'},
                                                        "username": {'S': str(new_username)},
                                                        "hashed_password": {'S': str(h.hexdigest())},
                                                        "password_length": {'S': str(len(new_password))},
                                                        "password_count_numeric": {
                                                            'S': str(to_save['password_count_numeric'])},
                                                        "password_count_alpha": {'S': str(to_save['password_count_alpha'])},
                                                        "password_count_uppercase": {
                                                            'S': str(to_save['password_count_uppercase'])},
                                                        "password_count_symbols": {
                                                            'S': str(to_save['password_count_symbols'])},
                                                        "model_run_modelRank": {'S': str(st.session_state['model_results']['modelRank'])},
                                                        "model_run_modelProb": {'S': str(st.session_state['model_results']['modelProb'])},
                                                        "model_run_prefixProb": {'S': str(st.session_state['model_results']['prefixProb'])},
                                                        "model_run_baseProb": {'S': str(st.session_state['model_results']['baseProb'])},
                                                        "model_run_suffixProb": {'S': str(st.session_state['model_results']['suffixProb'])},
                                                        "model_run_l33tProb": {'S': str(st.session_state['model_results']['l33tProb'])},
                                                        "model_run_upperProb": {'S': str(st.session_state['model_results']['upperProb'])},
                                                        "model_run_finalPrefix_length": {'S': str(len(st.session_state['model_results']['finalPrefix']))},
                                                        "model_run_finalunL33tBaseWord_length": {'S': str(len(st.session_state['model_results']['finalunL33tBaseWord']))},
                                                        "model_run_finalSuffix_length": {'S': str(len(st.session_state['model_results']['finalSuffix']))},
                                                        "model_run_l33tList": {'S': str(st.session_state['model_results']['l33tList'])},
                                                        "model_run_upperList": {'S': str(st.session_state['model_results']['upperList'])},
                                                        "model_run_nonePrefixProbFlag": {'S': str(st.session_state['model_results']['nonePrefixProbFlag'])},
                                                        "model_run_noneBaseProbFlag": {'S': str(st.session_state['model_results']['noneBaseProbFlag'])},
                                                        "model_run_noneSuffixProbFlag": {'S': str(st.session_state['model_results']['noneSuffixProbFlag'])},
                                                        "model_run_noneL33tProbFlag": {'S': str(st.session_state['model_results']['noneL33tProbFlag'])},
                                                        "model_run_noneUpperProbFlag": {'S': str(st.session_state['model_results']['noneUpperProbFlag'])},
                                                        "model_run_bits": {'S': str(st.session_state['model_results']['bits'])},
                                                        "model_run_percentile": {'S': str(st.session_state['model_results']['percentile'])},
                                                        "model_run_recommendation_1": {'S': str(st.session_state['model_results']['1'])},
                                                        "model_run_recommendation_2": {'S': str(st.session_state['model_results']['2'])},
                                                        "model_run_recommendation_3": {'S': str(st.session_state['model_results']['3'])},
                                                        "model_run_recommendation_4": {'S': str(st.session_state['model_results']['4'])},
                                                        "model_run_recommendation_5": {'S': str(st.session_state['model_results']['5'])},
                                                        "model_run_recommendation_6": {'S': str(st.session_state['model_results']['6'])},
                                                        "model_run_recommendation_7": {'S': str(st.session_state['model_results']['7'])},
                                                        "model_ui_password_strength": {'S': str(st.session_state['ui_results']['password_strength'])},
                                                        "model_ui_password_percentile": {'S': str(st.session_state['ui_results']['password_percentile'])},
                                                        "model_ui_hack_time": {'S': str(st.session_state['ui_results']['hack_time'])},
                                                        "model_ui_hack_unit": {'S': str(st.session_state['ui_results']['hack_unit'])},
                                                        "model_ui_rec_lev_1": {'S': str(st.session_state['ui_results']['rec_lev_1'])},
                                                        "model_ui_pass_1": {'S': str(st.session_state['ui_results']['pass_1'])},
                                                        "model_ui_bits_1": {'S': str(st.session_state['ui_results']['bits_1'])},
                                                        "model_ui_hack_time_1": {'S': str(st.session_state['ui_results']['hack_time_1'])},
                                                        "model_ui_hack_unit_1": {'S': str(st.session_state['ui_results']['hack_unit_1'])},
                                                        "model_ui_rec_lev_2": {'S': str(st.session_state['ui_results']['rec_lev_2'])},
                                                        "model_ui_pass_2": {'S': str(st.session_state['ui_results']['pass_2'])},
                                                        "model_ui_bits_2": {'S': str(st.session_state['ui_results']['bits_2'])},
                                                        "model_ui_hack_time_2": {'S': str(st.session_state['ui_results']['hack_time_2'])},
                                                        "model_ui_hack_unit_2": {'S': str(st.session_state['ui_results']['hack_unit_2'])},
                                                        "model_ui_rec_lev_3": {'S': str(st.session_state['ui_results']['rec_lev_3'])},
                                                        "model_ui_pass_3": {'S': str(st.session_state['ui_results']['pass_3'])},
                                                        "model_ui_bits_3": {'S': str(st.session_state['ui_results']['bits_3'])},
                                                        "model_ui_hack_time_3": {'S': str(st.session_state['ui_results']['hack_time_3'])},
                                                        "model_ui_hack_unit_3": {'S': str(st.session_state['ui_results']['hack_unit_3'])},
                                                        "model_ui_screen_1": {'S': str(st.session_state['ui_results']['screen_1'])},
                                                        "model_ui_screen_2": {'S': str(st.session_state['ui_results']['screen_2'])},
                                                        "model_ui_screen_3": {'S': str(st.session_state['ui_results']['screen_3'])},
                                                        "experiment_group": {
                                                            'S': str(st.session_state['experiment_group'])},
                                                        "recommendation_button_1_pressed": {
                                                            'S': str(st.session_state[
                                                                         'recommendation_button_1_pressed'])},
                                                        "recommendation_button_2_pressed": {
                                                            'S': str(st.session_state[
                                                                         'recommendation_button_2_pressed'])},
                                                        "recommendation_button_3_pressed": {
                                                            'S': str(st.session_state[
                                                                         'recommendation_button_3_pressed'])},
                                                        "recommendation_1_injected": {
                                                            'S': str(
                                                                st.session_state['recommendation_1_injected'])},
                                                        "recommendation_2_injected": {
                                                            'S': str(
                                                                st.session_state['recommendation_2_injected'])},
                                                        "recommendation_3_injected": {
                                                            'S': str(
                                                                st.session_state['recommendation_3_injected'])},
                                                        "recommendation_1_canceled": {
                                                            'S': str(
                                                                st.session_state['recommendation_1_canceled'])},
                                                        "recommendation_2_canceled": {
                                                            'S': str(
                                                                st.session_state['recommendation_2_canceled'])},
                                                        "recommendation_3_canceled": {
                                                            'S': str(
                                                                st.session_state['recommendation_3_canceled'])},
                                                        "second_shown": {
                                                            'S': str(st.session_state['second_shown'])},
                                                        "registration1_start_time": {
                                                            'S': str(st.session_state['page_start_time'])},
                                                        "page_start_time": {'S': str(st.session_state['page_start_time'])},
                                                        "page_end_time": {'S': str(time.time())},

                                                    }

                                                    item2 = {
                                                        "username": {'S': str(new_username)},
                                                        "password": {'S': str(h.hexdigest())}
                                                    }
                                                    # print(st.session_state)
                                                    dynamoz = Dynamodb()
                                                    dynamoz.data_upload("pesrank", item)

                                                    dynamoz.data_upload("users", item2)

                                                    if 'form_display' in st.session_state:
                                                        st.session_state['form_display'] = 'post_registration'
                                                    placeholder2.empty()
                                                    return True
                                                else:
                                                    try:
                                                        to_save = {}
                                                        model_ui = {}
                                                        model_run = {}
                                                        with st.spinner('Processing your information...'):
                                                            ui_results, model_results = mainModel.main(new_username, new_password)
                                                        st.session_state['ui_results_2'] = ui_results
                                                        st.session_state['model_results_2'] = model_results
                                                        to_save['page'] = 'Register2'
                                                        to_save['username'] = new_username
                                                        to_save['password_length'] = len(new_password)
                                                        to_save['password_count_numeric'] = \
                                                            sum(1 for elem in new_password if elem.isnumeric())
                                                        to_save['password_count_alpha'] = \
                                                            sum(1 for elem in new_password if elem.isalpha())
                                                        to_save['password_count_uppercase'] = \
                                                            sum(1 for elem in new_password if elem.isupper())
                                                        to_save['password_count_symbols'] = \
                                                            len(new_password) - sum(
                                                                1 for elem in new_password if elem.isalnum())
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
                                                        model_run['finalPrefix_length'] = len(model_results['finalPrefix'])
                                                        model_run['finalunL33tBaseWord_length'] = \
                                                            len(model_results['finalunL33tBaseWord'])
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
                                                        if 'register_2_password' in st.session_state:
                                                            st.session_state['register_2_password'] = new_password
                                                        temp_dict = {}
                                                        new_password1 = new_password.encode('utf-8')
                                                        h = hashlib.sha256(new_password1)
                                                        temp_dict[new_username] = h.hexdigest()
                                                        st.session_state['users'].update(temp_dict)
                                                        with open('output/users.json', 'w') as f:
                                                            json.dump(st.session_state['users'], f)
                                                        item = {
                                                            "page": {'S': 'register2'},
                                                            "username": {'S': str(new_username)},
                                                            "hashed_password": {'S': str(h.hexdigest())},
                                                            "password_length": {'S': str(len(new_password))},
                                                            "password_count_numeric": {'S': str(to_save['password_count_numeric'])},
                                                            "password_count_alpha": {'S': str(to_save['password_count_alpha'])},
                                                            "password_count_uppercase": {'S': str(to_save['password_count_uppercase'])},
                                                            "password_count_symbols": {'S': str(to_save['password_count_symbols'])},
                                                            "model_run_modelRank": {'S': str(model_run['modelRank'])},
                                                            "model_run_modelProb": {'S': str(model_run['modelProb'])},
                                                            "model_run_prefixProb": {'S': str(model_run['prefixProb'])},
                                                            "model_run_baseProb": {'S': str(model_run['baseProb'])},
                                                            "model_run_suffixProb": {'S': str(model_run['suffixProb'])},
                                                            "model_run_l33tProb": {'S': str(model_run['l33tProb'])},
                                                            "model_run_upperProb": {'S': str(model_run['upperProb'])},
                                                            "model_run_finalPrefix_length": {'S': str(model_run['finalPrefix_length'])},
                                                            "model_run_finalunL33tBaseWord_length": {'S': str(model_run['finalunL33tBaseWord_length'])},
                                                            "model_run_finalSuffix_length": {'S': str(model_run['finalSuffix_length'])},
                                                            "model_run_l33tList": {'S': str(model_run['l33tList'])},
                                                            "model_run_upperList": {'S': str(model_run['upperList'])},
                                                            "model_run_nonePrefixProbFlag": {'S': str(model_run['nonePrefixProbFlag'])},
                                                            "model_run_noneBaseProbFlag": {'S': str(model_run['noneBaseProbFlag'])},
                                                            "model_run_noneSuffixProbFlag": {'S': str(model_run['noneSuffixProbFlag'])},
                                                            "model_run_noneL33tProbFlag": {'S': str(model_run['noneL33tProbFlag'])},
                                                            "model_run_noneUpperProbFlag": {'S': str(model_run['noneUpperProbFlag'])},
                                                            "model_run_bits": {'S': str(model_run['bits'])},
                                                            "model_run_percentile": {'S': str(model_run['percentile'])},
                                                            "model_run_recommendation_1": {'S': str(model_run['recommendation_1'])},
                                                            "model_run_recommendation_2": {'S': str(model_run['recommendation_2'])},
                                                            "model_run_recommendation_3": {'S': str(model_run['recommendation_3'])},
                                                            "model_run_recommendation_4": {'S': str(model_run['recommendation_4'])},
                                                            "model_run_recommendation_5": {'S': str(model_run['recommendation_5'])},
                                                            "model_run_recommendation_6": {'S': str(model_run['recommendation_6'])},
                                                            "model_run_recommendation_7": {'S': str(model_run['recommendation_7'])},
                                                            "model_ui_password_strength": {'S': str(model_ui['password_strength'])},
                                                            "model_ui_password_percentile": {'S': str(model_ui['password_percentile'])},
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
                                                            "model_ui_screen_1": {'S': str(st.session_state['ui_results']['screen_1'])},
                                                            "model_ui_screen_2": {'S': str(st.session_state['ui_results']['screen_2'])},
                                                            "model_ui_screen_3": {'S': str(st.session_state['ui_results']['screen_3'])},
                                                            "experiment_group": {'S': str(st.session_state['experiment_group'])},
                                                            "recommendation_button_1_pressed": {
                                                                'S': str(st.session_state['recommendation_button_1_pressed'])},
                                                            "recommendation_button_2_pressed": {
                                                                'S': str(st.session_state['recommendation_button_2_pressed'])},
                                                            "recommendation_button_3_pressed": {
                                                                'S': str(st.session_state['recommendation_button_3_pressed'])},
                                                            "recommendation_1_injected": {
                                                                'S': str(st.session_state['recommendation_1_injected'])},
                                                            "recommendation_2_injected": {
                                                                'S': str(st.session_state['recommendation_2_injected'])},
                                                            "recommendation_3_injected": {
                                                                'S': str(st.session_state['recommendation_3_injected'])},
                                                            "recommendation_1_canceled": {
                                                                'S': str(
                                                                    st.session_state['recommendation_1_canceled'])},
                                                            "recommendation_2_canceled": {
                                                                'S': str(
                                                                    st.session_state['recommendation_2_canceled'])},
                                                            "recommendation_3_canceled": {
                                                                'S': str(
                                                                    st.session_state['recommendation_3_canceled'])},
                                                            "second_shown": {'S': str(st.session_state['second_shown'])},
                                                            "registration1_start_time": {
                                                                'S': str(st.session_state['page_start_time'])},
                                                            "page_start_time": {'S': str(st.session_state['page_start_time'])},
                                                            "page_end_time": {'S': str(time.time())}
                                                        }
                                                        print(json.dumps(ui_results, indent=4))
                                                        item2 = {
                                                            "username": {'S': str(new_username)},
                                                            "password": {'S': str(h.hexdigest())}
                                                        }

                                                        dynamoz = Dynamodb()
                                                        dynamoz.data_upload("pesrank", item)
                                                        dynamoz.data_upload("users", item2)

                                                        if 'form_display' in st.session_state:
                                                            st.session_state['form_display'] = 'post_registration'
                                                        placeholder2.empty()
                                                        return True
                                                    except Exception as e:
                                                        st.error("We apologize, there's an error")
                                                        st.error('The Error is ' + str(e))
                                            except Exception as e:
                                                st.error("We apologize, there's an error")
                                                st.error('Error is ' + str(e))

                                        else:
                                            st.error('Your password must contain at least 1 letter and at least 1 digit')
                                    else:
                                        not_ascii = []
                                        for char in new_password:
                                            if not str.isascii(char):
                                                not_ascii.append(char)
                                        not_ascii_to_print = ','.join(not_ascii)
                                        st.error('Please avoid using these characters: ' + not_ascii_to_print)
                                else:
                                    st.error('Your password must contain at least 8 characters')
                            else:
                                st.error('Username already taken, please choose a new username')
                        else:
                            st.error('Mismatch between entered passwords!')
                    else:
                        st.error('Please complete the registration form')

            with col2:
                # st.session_state['experiment_group'] = 3
                if st.session_state['experiment_group'] == 1:
                    ui_results = st.session_state['ui_results']
                    st.markdown("<br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
                    if ui_results['hack_time'] == 'Instantly' or ui_results['hack_unit'] in ('seconds', 'minutes', 'hours', 'days'):
                        st.markdown("<--- Your password is risky", unsafe_allow_html=True)
                    if ui_results['hack_time'] == 'Instantly':
                        st.markdown("<p>Hackers may guess your password <FONT COLOR=red>instantly</FONT COLOR=red></p>", unsafe_allow_html=True)
                    elif ui_results['hack_unit'] == 'seconds':
                        text = "<p>Hackers may guess your password within <FONT COLOR=red>" + str(ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=red></p>")
                        st.markdown(text, unsafe_allow_html=True)
                    elif ui_results['hack_unit'] == 'minutes':
                        text = "<p>Hackers may guess your password within <FONT COLOR=red>" + str(
                            ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=red></p>")
                        st.markdown(text, unsafe_allow_html=True)
                    elif ui_results['hack_unit'] == 'hours':
                        text = "<p>Hackers may guess your password within <FONT COLOR=orange>" + str(
                            ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=orange></p>")
                        st.markdown(text, unsafe_allow_html=True)
                    elif ui_results['hack_unit'] == 'days':
                        text = "<p>Hackers may guess your password within <FONT COLOR=orange>" + str(
                            ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=orange></p>")
                        st.markdown(text, unsafe_allow_html=True)
                    else:
                        text = "<p>Hackers may guess your password within <FONT COLOR=green>" + str(
                            ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=green></p>")
                        st.markdown(text, unsafe_allow_html=True)

                    st.markdown("<p>Please try our recommendations to improve your password:</p>", unsafe_allow_html=True)
                    if ui_results["pass_1"] == '':
                        st.markdown("<br>", unsafe_allow_html=True)
                    else:
                        open_modal1 = st.button(ui_results["screen_1"])
                        if open_modal1:
                            if 'recommendation_button_pressed' in st.session_state:
                                st.session_state['recommendation_button_pressed'] = 1
                            if 'recommendation_button_1_pressed' in st.session_state:
                                st.session_state['recommendation_button_1_pressed'] = 1
                            open_xd()

                    if ui_results["pass_2"] == '':
                        st.markdown("<br>", unsafe_allow_html=True)
                    else:
                        open_modal2 = st.button(ui_results["screen_2"])
                        if open_modal2:
                            if 'recommendation_button_pressed' in st.session_state:
                                st.session_state['recommendation_button_pressed'] = 2
                            if 'recommendation_button_2_pressed' in st.session_state:
                                st.session_state['recommendation_button_2_pressed'] = 1
                            open_xd()

                    if ui_results["pass_3"] == '':
                        st.markdown("<br>", unsafe_allow_html=True)
                    else:
                        open_modal3 = st.button(ui_results["screen_3"])
                        if open_modal3:
                            if 'recommendation_button_pressed' in st.session_state:
                                st.session_state['recommendation_button_pressed'] = 3
                            if 'recommendation_button_3_pressed' in st.session_state:
                                st.session_state['recommendation_button_3_pressed'] = 1
                            open_xd()

                    if is_open():
                        with container():
                            if st.session_state['recommendation_button_pressed'] == 1:
                                if 'watched_recom_1' in st.session_state:
                                    st.session_state['watched_recom_1'] = True
                                if ui_results['rec_lev_1'] == '1':
                                    text1 = "Try the following change:"
                                else:
                                    text1 = "Try the following changes:"
                                text2 = ui_results["pass_1"]
                                if ui_results['hack_time_1'] == 'Instantly':
                                    text3 = "Hackers may guess the new password instantly"
                                else:
                                    text3 = "It will take hackers " + str(ui_results['hack_time_1']) + ' ' \
                                            + str(ui_results['hack_unit_1'] + " to guess the new password")
                                password_valuez = ui_results["pass_1"]
                                chosen_recommendation = 1

                            if st.session_state['recommendation_button_pressed'] == 2:
                                if 'watched_recom_2' in st.session_state:
                                    st.session_state['watched_recom_2'] = True
                                if ui_results['rec_lev_2'] == '1':
                                    text1 = "Try the following change:"
                                else:
                                    text1 = "Try the following changes:"
                                text2 = ui_results["pass_2"]
                                if ui_results['hack_time_2'] == 'Instantly':
                                    text3 = "Hackers may guess the new password instantly"
                                else:
                                    text3 = "It will take hackers " + str(ui_results['hack_time_2']) + ' ' \
                                            + str(ui_results['hack_unit_2'] + " to guess the new password")
                                password_valuez = ui_results["pass_2"]
                                chosen_recommendation = 2

                            if st.session_state['recommendation_button_pressed'] == 3:
                                if 'watched_recom_3' in st.session_state:
                                    st.session_state['watched_recom_3'] = True
                                if ui_results['rec_lev_3'] == '1':
                                    text1 = "Try the following change:"
                                else:
                                    text1 = "Try the following changes:"
                                text2 = ui_results["pass_3"]
                                if ui_results['hack_time_3'] == 'Instantly':
                                    text3 = "Hackers may guess the new password instantly"
                                else:
                                    text3 = "It will take hackers " + str(
                                        ui_results['hack_time_3']) + ' ' \
                                            + str(ui_results['hack_unit_3'] + " to guess the new password")
                                password_valuez = ui_results["pass_3"]
                                chosen_recommendation = 3

                            st.subheader("Password recommendation")
                            st.markdown(text1)
                            st.subheader(text2)
                            st.markdown(text3)

                            content = """
                                <p><a href='#' id='Link 1'></a></p>
                                <p><a href='#' id='Link 2'></a></p>
                                <a href='#' id='Use'><button 
                                    style="
                                    color: white;
                                    background-color: rgb(255, 255, 255);
                                    border-radius: 7px;
                                    border: 1px #015E92;
                                    background-image: linear-gradient(to bottom, #579add, #2773bd);
                                    "                                 
                                    type="button">Use this password</button></a>
                                <a href='#' id='Cancel'><button 
                                    style="
                                    background-color: rgb(255, 255, 255);
                                    border-radius: 7px;
                                    border: 1px #015E92;
                                    background-image: linear-gradient(to bottom, #f8f9fa, #6c757d);
                                    width: 60px;
                                    " 
                                    type="button">Cancel</button></a>
                                """

                            clicked = click_detector(content)
                            if clicked == 'Cancel':
                                if chosen_recommendation == 1:
                                    if 'recommendation_1_canceled' in st.session_state:
                                        st.session_state['recommendation_1_canceled'] = 1
                                elif chosen_recommendation == 2:
                                    if 'recommendation_2_canceled' in st.session_state:
                                        st.session_state['recommendation_2_canceled'] = 1
                                elif chosen_recommendation == 3:
                                    if 'recommendation_3_canceled' in st.session_state:
                                        st.session_state['recommendation_3_canceled'] = 1
                                close()
                            if clicked == 'Use':
                                if st.session_state['form_inject'] == 1:
                                    if 'password_value' in st.session_state:
                                        st.session_state['password_value'] = password_valuez
                                    if 'password2_value' in st.session_state:
                                        st.session_state['password2_value'] = password_valuez
                                    if 'second_shown' in st.session_state:
                                        st.session_state['second_shown'] = 1
                                    if 'password_flag' in st.session_state:
                                        st.session_state['password_flag'] = False
                                    if 'chosen_recommendation' in st.session_state:
                                        st.session_state['chosen_recommendation'] = chosen_recommendation
                                    if chosen_recommendation == 1:
                                        if 'recommendation_1_injected' in st.session_state:
                                            st.session_state['recommendation_1_injected'] = 1
                                    elif chosen_recommendation == 2:
                                        if 'recommendation_2_injected' in st.session_state:
                                            st.session_state['recommendation_2_injected'] = 1
                                    elif chosen_recommendation == 3:
                                        if 'recommendation_3_injected' in st.session_state:
                                            st.session_state['recommendation_3_injected'] = 1
                                    close()
                                else:
                                    if 'password_value' in st.session_state:
                                        st.session_state['password_value'] = password_valuez
                                    if 'password2_value' in st.session_state:
                                        st.session_state['password2_value'] = ''
                                    if 'password_flag' in st.session_state:
                                        st.session_state['password_flag'] = False
                                    if 'chosen_recommendation' in st.session_state:
                                        st.session_state['chosen_recommendation'] = chosen_recommendation
                                    if chosen_recommendation == 1:
                                        if 'recommendation_1_injected' in st.session_state:
                                            st.session_state['recommendation_1_injected'] = 1
                                    elif chosen_recommendation == 2:
                                        if 'recommendation_2_injected' in st.session_state:
                                            st.session_state['recommendation_2_injected'] = 1
                                    elif chosen_recommendation == 3:
                                        if 'recommendation_3_injected' in st.session_state:
                                            st.session_state['recommendation_3_injected'] = 1
                                close()



                elif st.session_state['experiment_group'] == 2:
                    ui_results = st.session_state['ui_results']
                    st.markdown("<br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
                    if ui_results['hack_time'] == 'Instantly' or ui_results['hack_unit'] in ('seconds', 'minutes', 'hours', 'days'):
                        st.markdown("<--- Your password is risky", unsafe_allow_html=True)
                    if ui_results['hack_time'] == 'Instantly':
                        st.markdown("<p>Hackers may guess your password <FONT COLOR=red>instantly</FONT COLOR=red></p>", unsafe_allow_html=True)
                    elif ui_results['hack_unit'] == 'seconds':
                        text = "<p>Hackers may guess your password within <FONT COLOR=red>" + str(ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=red></p>")
                        st.markdown(text, unsafe_allow_html=True)
                    elif ui_results['hack_unit'] == 'minutes':
                        text = "<p>Hackers may guess your password within <FONT COLOR=red>" + str(
                            ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=red></p>")
                        st.markdown(text, unsafe_allow_html=True)
                    elif ui_results['hack_unit'] == 'hours':
                        text = "<p>Hackers may guess your password within <FONT COLOR=orange>" + str(
                            ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=orange></p>")
                        st.markdown(text, unsafe_allow_html=True)
                    elif ui_results['hack_unit'] == 'days':
                        text = "<p>Hackers may guess your password within <FONT COLOR=orange>" + str(
                            ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=orange></p>")
                        st.markdown(text, unsafe_allow_html=True)
                    else:
                        text = "<p>Hackers may guess your password within <FONT COLOR=green>" + str(
                            ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=green></p>")
                        st.markdown(text, unsafe_allow_html=True)

                    st.markdown("<p>Please try our recommendations to improve your password:</p>",
                                unsafe_allow_html=True)
                    st.markdown("<p>On each button you can see the new estimated hack time of the recommended password</p>",
                                unsafe_allow_html=True)
                    if ui_results["pass_1"] == '':
                        st.markdown("<br>", unsafe_allow_html=True)
                    else:
                        hack_time_temp = str(ui_results['hack_time_1']) + ' ' + str(ui_results['hack_unit_1'])
                        open_modal1 = st.button(hack_time_temp)
                        if open_modal1:
                            if 'recommendation_button_pressed' in st.session_state:
                                st.session_state['recommendation_button_pressed'] = 1
                            if 'recommendation_button_1_pressed' in st.session_state:
                                st.session_state['recommendation_button_1_pressed'] = 1
                            open_xd()

                    if ui_results["pass_2"] == '':
                        st.markdown("<br>", unsafe_allow_html=True)
                    else:
                        hack_time_temp = str(ui_results['hack_time_2']) + ' ' + str(ui_results['hack_unit_2'])
                        open_modal2 = st.button(hack_time_temp)
                        if open_modal2:
                            if 'recommendation_button_pressed' in st.session_state:
                                st.session_state['recommendation_button_pressed'] = 2
                            if 'recommendation_button_2_pressed' in st.session_state:
                                st.session_state['recommendation_button_2_pressed'] = 1
                            open_xd()

                    if ui_results["pass_3"] == '':
                        st.markdown("<br>", unsafe_allow_html=True)
                    else:
                        hack_time_temp = str(ui_results['hack_time_3']) + ' ' + str(ui_results['hack_unit_3'])
                        open_modal3 = st.button(hack_time_temp)
                        if open_modal3:
                            if 'recommendation_button_pressed' in st.session_state:
                                st.session_state['recommendation_button_pressed'] = 3
                            if 'recommendation_button_3_pressed' in st.session_state:
                                st.session_state['recommendation_button_3_pressed'] = 1
                            open_xd()

                    if is_open():
                        with container():

                            if st.session_state['recommendation_button_pressed'] == 1:
                                if 'watched_recom_1' in st.session_state:
                                    st.session_state['watched_recom_1'] = True
                                if ui_results['rec_lev_1'] == '1':
                                    text1 = "Try the following change:"
                                else:
                                    text1 = "Try the following changes:"
                                text2 = ui_results["pass_1"]
                                if ui_results['hack_time_1'] == 'Instantly':
                                    text3 = "Hackers may guess the new password instantly"
                                else:
                                    text3 = "Hackers may guess the new password within " + str(
                                        ui_results['hack_time_1']) + ' ' \
                                            + str(ui_results['hack_unit_1'])
                                password_valuez = ui_results["pass_1"]
                                chosen_recommendation = 1

                            if st.session_state['recommendation_button_pressed'] == 2:
                                if 'watched_recom_2' in st.session_state:
                                    st.session_state['watched_recom_2'] = True
                                if ui_results['rec_lev_2'] == '1':
                                    text1 = "Try the following change:"
                                else:
                                    text1 = "Try the following changes:"
                                text2 = ui_results["pass_2"]
                                if ui_results['hack_time_2'] == 'Instantly':
                                    text3 = "Hackers may guess the new password instantly"
                                else:
                                    text3 = "Hackers may guess the new password within " + str(
                                        ui_results['hack_time_2']) + ' ' \
                                            + str(ui_results['hack_unit_2'])
                                password_valuez = ui_results["pass_2"]
                                chosen_recommendation = 2

                            if st.session_state['recommendation_button_pressed'] == 3:
                                if 'watched_recom_3' in st.session_state:
                                    st.session_state['watched_recom_3'] = True
                                if ui_results['rec_lev_3'] == '1':
                                    text1 = "Try the following change:"
                                else:
                                    text1 = "Try the following changes:"
                                text2 = ui_results["pass_3"]
                                if ui_results['hack_time_3'] == 'Instantly':
                                    text3 = "Hackers may guess the new password instantly"
                                else:
                                    text3 = "Hackers may guess the new password within " + str(
                                        ui_results['hack_time_3']) + ' ' \
                                            + str(ui_results['hack_unit_3'])
                                password_valuez = ui_results["pass_3"]
                                chosen_recommendation = 3

                            st.subheader("Password recommendation")
                            st.markdown(text1)
                            st.subheader(text2)
                            st.markdown(text3)
                            content = """
                                <p><a href='#' id='Link 1'></a></p>
                                <p><a href='#' id='Link 2'></a></p>
                                <a href='#' id='Use'><button 
                                    style="
                                    color: white;
                                    background-color: rgb(255, 255, 255);
                                    border-radius: 7px;
                                    border: 1px #015E92;
                                    background-image: linear-gradient(to bottom, #579add, #2773bd);
                                    "                                 
                                    type="button">Use this password</button></a>
                                <a href='#' id='Cancel'><button 
                                    style="
                                    background-color: rgb(255, 255, 255);
                                    border-radius: 7px;
                                    border: 1px #015E92;
                                    background-image: linear-gradient(to bottom, #f8f9fa, #6c757d);
                                    width: 60px;
                                    " 
                                    type="button">Cancel</button></a>
                                """

                            clicked = click_detector(content)
                            if clicked == 'Cancel':
                                if chosen_recommendation == 1:
                                    if 'recommendation_1_canceled' in st.session_state:
                                        st.session_state['recommendation_1_canceled'] = 1
                                elif chosen_recommendation == 2:
                                    if 'recommendation_2_canceled' in st.session_state:
                                        st.session_state['recommendation_2_canceled'] = 1
                                elif chosen_recommendation == 3:
                                    if 'recommendation_3_canceled' in st.session_state:
                                        st.session_state['recommendation_3_canceled'] = 1
                                close()
                            if clicked == 'Use':
                                if st.session_state['form_inject'] == 1:
                                    if 'password_value' in st.session_state:
                                        st.session_state['password_value'] = password_valuez
                                    if 'password2_value' in st.session_state:
                                        st.session_state['password2_value'] = password_valuez
                                    if 'second_shown' in st.session_state:
                                        st.session_state['second_shown'] = 1
                                    if 'password_flag' in st.session_state:
                                        st.session_state['password_flag'] = False
                                    if 'chosen_recommendation' in st.session_state:
                                        st.session_state['chosen_recommendation'] = chosen_recommendation
                                    if chosen_recommendation == 1:
                                        if 'recommendation_1_injected' in st.session_state:
                                            st.session_state['recommendation_1_injected'] = 1
                                    elif chosen_recommendation == 2:
                                        if 'recommendation_2_injected' in st.session_state:
                                            st.session_state['recommendation_2_injected'] = 1
                                    elif chosen_recommendation == 3:
                                        if 'recommendation_3_injected' in st.session_state:
                                            st.session_state['recommendation_3_injected'] = 1
                                    close()
                                else:
                                    if 'password_value' in st.session_state:
                                        st.session_state['password_value'] = password_valuez
                                    if 'password2_value' in st.session_state:
                                        st.session_state['password2_value'] = ''
                                    if 'password_flag' in st.session_state:
                                        st.session_state['password_flag'] = False
                                    if 'chosen_recommendation' in st.session_state:
                                        st.session_state['chosen_recommendation'] = chosen_recommendation
                                    if chosen_recommendation == 1:
                                        if 'recommendation_1_injected' in st.session_state:
                                            st.session_state['recommendation_1_injected'] = 1
                                    elif chosen_recommendation == 2:
                                        if 'recommendation_2_injected' in st.session_state:
                                            st.session_state['recommendation_2_injected'] = 1
                                    elif chosen_recommendation == 3:
                                        if 'recommendation_3_injected' in st.session_state:
                                            st.session_state['recommendation_3_injected'] = 1
                                close()


                elif st.session_state['experiment_group'] == 3:
                    ui_results = st.session_state['ui_results']
                    st.markdown("<br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
                    if ui_results['hack_time'] == 'Instantly' or ui_results['hack_unit'] in ('seconds', 'minutes', 'hours', 'days'):
                        st.markdown("<--- Your password is risky", unsafe_allow_html=True)
                    if ui_results['hack_time'] == 'Instantly':
                        st.markdown("<p>Hackers may guess your password <FONT COLOR=red>instantly</FONT COLOR=red></p>", unsafe_allow_html=True)
                    elif ui_results['hack_unit'] == 'seconds':
                        text = "<p>Hackers may guess your password within <FONT COLOR=red>" + str(ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=red></p>")
                        st.markdown(text, unsafe_allow_html=True)
                    elif ui_results['hack_unit'] == 'minutes':
                        text = "<p>Hackers may guess your password within <FONT COLOR=red>" + str(
                            ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=red></p>")
                        st.markdown(text, unsafe_allow_html=True)
                    elif ui_results['hack_unit'] == 'hours':
                        text = "<p>Hackers may guess your password within <FONT COLOR=orange>" + str(
                            ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=orange></p>")
                        st.markdown(text, unsafe_allow_html=True)
                    elif ui_results['hack_unit'] == 'days':
                        text = "<p>Hackers may guess your password within <FONT COLOR=orange>" + str(
                            ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=orange></p>")
                        st.markdown(text, unsafe_allow_html=True)
                    else:
                        text = "<p>Hackers may guess your password within <FONT COLOR=green>" + str(
                            ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=green></p>")
                        st.markdown(text, unsafe_allow_html=True)

                    st.markdown("<p>Please try our recommendations to improve your password:</p>",
                                unsafe_allow_html=True)
                    st.markdown("<p>On each button you can see the number of changes in the original password</p>",
                                unsafe_allow_html=True)
                    if ui_results["pass_1"] == '':
                        st.markdown("<br>", unsafe_allow_html=True)
                    else:
                        if ui_results['rec_lev_1'] == 1:
                            changes_temp = "1 change"
                        else:
                            changes_temp = str(ui_results['rec_lev_1']) + ' changes'
                        open_modal1 = st.button(changes_temp)
                        if open_modal1:
                            if 'recommendation_button_pressed' in st.session_state:
                                st.session_state['recommendation_button_pressed'] = 1
                            if 'recommendation_button_1_pressed' in st.session_state:
                                st.session_state['recommendation_button_1_pressed'] = 1
                            open_xd()

                    if ui_results["pass_2"] == '':
                        st.markdown("<br>", unsafe_allow_html=True)
                    else:
                        if ui_results['rec_lev_2'] == 1:
                            changes_temp = "1 change"
                        else:
                            changes_temp = str(ui_results['rec_lev_2']) + ' changes'
                        open_modal2 = st.button(changes_temp)
                        if open_modal2:
                            if 'recommendation_button_pressed' in st.session_state:
                                st.session_state['recommendation_button_pressed'] = 2
                            if 'recommendation_button_2_pressed' in st.session_state:
                                st.session_state['recommendation_button_2_pressed'] = 1
                            open_xd()

                    if ui_results["pass_3"] == '':
                        st.markdown("<br>", unsafe_allow_html=True)
                    else:
                        if ui_results['rec_lev_3'] == 1:
                            changes_temp = "1 change"
                        else:
                            changes_temp = str(ui_results['rec_lev_3']) + ' changes'
                        open_modal3 = st.button(changes_temp)
                        if open_modal3:
                            if 'recommendation_button_pressed' in st.session_state:
                                st.session_state['recommendation_button_pressed'] = 3
                            if 'recommendation_button_3_pressed' in st.session_state:
                                st.session_state['recommendation_button_3_pressed'] = 1
                            open_xd()

                    if is_open():
                        with container():
                            if st.session_state['recommendation_button_pressed'] == 1:
                                if 'watched_recom_1' in st.session_state:
                                    st.session_state['watched_recom_1'] = True
                                if ui_results['rec_lev_1'] == '1':
                                    text1 = "Try the following change:"
                                else:
                                    text1 = "Try the following changes:"
                                text2 = ui_results["pass_1"]
                                if ui_results['hack_time_1'] == 'Instantly':
                                    text3 = "Hackers may guess the new password instantly"
                                else:
                                    text3 = "It will take hackers " + str(ui_results['hack_time_1']) + ' ' \
                                            + str(ui_results['hack_unit_1'] + " to guess the new password")
                                password_valuez = ui_results["pass_1"]
                                chosen_recommendation = 1

                            if st.session_state['recommendation_button_pressed'] == 2:
                                if 'watched_recom_2' in st.session_state:
                                    st.session_state['watched_recom_2'] = True
                                if ui_results['rec_lev_2'] == '1':
                                    text1 = "Try the following change:"
                                else:
                                    text1 = "Try the following changes:"
                                text2 = ui_results["pass_2"]
                                if ui_results['hack_time_2'] == 'Instantly':
                                    text3 = "Hackers may guess the new password instantly"
                                else:
                                    text3 = "It will take hackers " + str(ui_results['hack_time_2']) + ' ' \
                                            + str(ui_results['hack_unit_2'] + " to guess the new password")
                                password_valuez = ui_results["pass_2"]
                                chosen_recommendation = 2

                            if st.session_state['recommendation_button_pressed'] == 3:
                                if 'watched_recom_3' in st.session_state:
                                    st.session_state['watched_recom_3'] = True
                                if ui_results['rec_lev_3'] == '1':
                                    text1 = "Try the following change:"
                                else:
                                    text1 = "Try the following changes:"
                                text2 = ui_results["pass_3"]
                                if ui_results['hack_time_3'] == 'Instantly':
                                    text3 = "Hackers may guess the new password instantly"
                                else:
                                    text3 = "It will take hackers " + str(ui_results['hack_time_3']) + ' ' \
                                            + str(ui_results['hack_unit_3'] + " to guess the new password")
                                password_valuez = ui_results["pass_3"]
                                chosen_recommendation = 3

                            st.subheader("Password recommendation")
                            st.markdown(text1)
                            st.subheader(text2)
                            st.markdown(text3)

                            content = """
                                <p><a href='#' id='Link 1'></a></p>
                                <p><a href='#' id='Link 2'></a></p>
                                <a href='#' id='Use'><button 
                                    style="
                                    color: white;
                                    background-color: rgb(255, 255, 255);
                                    border-radius: 7px;
                                    border: 1px #015E92;
                                    background-image: linear-gradient(to bottom, #579add, #2773bd);
                                    "                                 
                                    type="button">Use this password</button></a>
                                <a href='#' id='Cancel'><button 
                                    style="
                                    background-color: rgb(255, 255, 255);
                                    border-radius: 7px;
                                    border: 1px #015E92;
                                    background-image: linear-gradient(to bottom, #f8f9fa, #6c757d);
                                    width: 60px;
                                    " 
                                    type="button">Cancel</button></a>
                                """

                            clicked = click_detector(content)
                            if clicked == 'Cancel':
                                if chosen_recommendation == 1:
                                    if 'recommendation_1_canceled' in st.session_state:
                                        st.session_state['recommendation_1_canceled'] = 1
                                elif chosen_recommendation == 2:
                                    if 'recommendation_2_canceled' in st.session_state:
                                        st.session_state['recommendation_2_canceled'] = 1
                                elif chosen_recommendation == 3:
                                    if 'recommendation_3_canceled' in st.session_state:
                                        st.session_state['recommendation_3_canceled'] = 1
                                close()
                            if clicked == 'Use':
                                if st.session_state['form_inject'] == 1:
                                    if 'password_value' in st.session_state:
                                        st.session_state['password_value'] = password_valuez
                                    if 'password2_value' in st.session_state:
                                        st.session_state['password2_value'] = password_valuez
                                    if 'second_shown' in st.session_state:
                                        st.session_state['second_shown'] = 1
                                    if 'password_flag' in st.session_state:
                                        st.session_state['password_flag'] = False
                                    if 'chosen_recommendation' in st.session_state:
                                        st.session_state['chosen_recommendation'] = chosen_recommendation
                                    if chosen_recommendation == 1:
                                        if 'recommendation_1_injected' in st.session_state:
                                            st.session_state['recommendation_1_injected'] = 1
                                    elif chosen_recommendation == 2:
                                        if 'recommendation_2_injected' in st.session_state:
                                            st.session_state['recommendation_2_injected'] = 1
                                    elif chosen_recommendation == 3:
                                        if 'recommendation_3_injected' in st.session_state:
                                            st.session_state['recommendation_3_injected'] = 1
                                    close()
                                else:
                                    if 'password_value' in st.session_state:
                                        st.session_state['password_value'] = password_valuez
                                    if 'password2_value' in st.session_state:
                                        st.session_state['password2_value'] = ''
                                    if 'password_flag' in st.session_state:
                                        st.session_state['password_flag'] = False
                                    if 'chosen_recommendation' in st.session_state:
                                        st.session_state['chosen_recommendation'] = chosen_recommendation
                                    if chosen_recommendation == 1:
                                        if 'recommendation_1_injected' in st.session_state:
                                            st.session_state['recommendation_1_injected'] = 1
                                    elif chosen_recommendation == 2:
                                        if 'recommendation_2_injected' in st.session_state:
                                            st.session_state['recommendation_2_injected'] = 1
                                    elif chosen_recommendation == 3:
                                        if 'recommendation_3_injected' in st.session_state:
                                            st.session_state['recommendation_3_injected'] = 1
                                close()

                else:
                    ui_results = st.session_state['ui_results']
                    st.markdown("<br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
                    if ui_results['hack_time'] == 'Instantly' or ui_results['hack_unit'] in ('seconds', 'minutes', 'hours', 'days'):
                        st.markdown("<--- Your password is risky", unsafe_allow_html=True)
                    if ui_results['hack_time'] == 'Instantly':
                        st.markdown("<p>Hackers may guess your password <FONT COLOR=red>instantly</FONT COLOR=red></p>", unsafe_allow_html=True)
                    elif ui_results['hack_unit'] == 'seconds':
                        text = "<p>Hackers may guess your password within <FONT COLOR=red>" + str(ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=red></p>")
                        st.markdown(text, unsafe_allow_html=True)
                    elif ui_results['hack_unit'] == 'minutes':
                        text = "<p>Hackers may guess your password within <FONT COLOR=red>" + str(
                            ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=red></p>")
                        st.markdown(text, unsafe_allow_html=True)
                    elif ui_results['hack_unit'] == 'hours':
                        text = "<p>Hackers may guess your password within <FONT COLOR=orange>" + str(
                            ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=orange></p>")
                        st.markdown(text, unsafe_allow_html=True)
                    elif ui_results['hack_unit'] == 'days':
                        text = "<p>Hackers may guess your password within <FONT COLOR=orange>" + str(
                            ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=orange></p>")
                        st.markdown(text, unsafe_allow_html=True)
                    else:
                        text = "<p>Hackers may guess your password within <FONT COLOR=green>" + str(
                            ui_results['hack_time']) + ' ' \
                               + str(ui_results['hack_unit'] + "</FONT COLOR=green></p>")
                        st.markdown(text, unsafe_allow_html=True)

    except Exception as e:
        st.error(e)


