from . import collections
import logging
import random
log = logging.getLogger(__name__)


def hidder(password, newword):
    first_set = set(password)
    second_set = set(newword)
    difference = first_set.symmetric_difference(second_set)
    hidden = []
    for char in newword:
        if char in difference:
            hidden.append(char)
        else:
            hidden.append('*')
    hidden_pass = ''.join(hidden)
    return hidden_pass


def main(model_results):
    data_struct = {}
    try:
        uis = collections.Collections(model_results)

        # High-level overview of password strength (verbal and percentile).
        strength, percentile = uis.collect_general()
        data_struct['password_strength'] = strength.strip().lower()
        data_struct['password_percentile'] = percentile

        # Scrubbed description of the password.
        password_text = uis.build_password()
        data_struct['password'] = password_text

        # Breakdown of the password structure (fixed strings).
        data_struct['structure'] = 'Prefix | Base Word | Suffix'
        data_struct['structure1'] = 'C = Capital letters, S = Symbols or Digits'

        # Advise and status of the prefix and suffix.
        data_struct['prefix_message'], data_struct['prefix_advise'] = uis.collect_prefix()
        data_struct['suffix_message'], data_struct['suffix_advise'] = uis.collect_suffix()

        # Advise and status of the base message.
        base_message, base_advise = uis.collect_base()
        data_struct['base_message'] = base_message

        # If the base is not unique, accumulate more words of advise using more aspects.
        base_advises = [base_advise]
        if not uis.is_unique_base():
            l33t_message, l33t_advise = uis.collect_l33t()
            capitalization_message, capitalization_advise = uis.collect_capitalization()
            # For the above only the message field is populated currently - the advise
            # field is empty and so we use the message.
            base_advises.extend([l33t_message, capitalization_message])
        # Only keep non-empty advises
        data_struct['base_advises'] = [advice for advice in base_advises if advice]

        # An indicator whether is password is strong enough to justify hiding all advise
        data_struct['hide_advise'] = uis.should_hide_advise()
        temp_hack_time, temp_unit = uis.hack_time(model_results['bits'])
        data_struct['hack_time'] = temp_hack_time
        data_struct['hack_unit'] = temp_unit
        suggest_1 = str(random.randint(1, 2))
        suggest_2 = str(random.randint(3, 4))
        suggest_3 = str(random.randint(5, 6))

        data_struct['rec_lev_1'] = suggest_1
        data_struct['pass_1'] = model_results[suggest_1][0]
        data_struct['bits_1'] = model_results[suggest_1][1]
        # print(model_results['rawPassword'])
        data_struct['screen_1'] = hidder(model_results['rawPassword'], model_results[suggest_1][0])
        # print(hidder(model_results['rawPassword'], model_results[suggest_1][0]))
        temp_hack_time, temp_unit = uis.hack_time(model_results[suggest_1][1])
        data_struct['hack_time_1'] = temp_hack_time
        data_struct['hack_unit_1'] = temp_unit

        data_struct['rec_lev_2'] = suggest_2
        data_struct['pass_2'] = model_results[suggest_2][0]
        data_struct['bits_2'] = model_results[suggest_2][1]
        data_struct['screen_2'] = hidder(model_results['rawPassword'], model_results[suggest_2][0])
        # print(hidder(model_results['rawPassword'], model_results[suggest_2][0]))
        temp_hack_time, temp_unit = uis.hack_time(model_results[suggest_2][1])
        data_struct['hack_time_2'] = temp_hack_time
        data_struct['hack_unit_2'] = temp_unit

        data_struct['rec_lev_3'] = suggest_3
        data_struct['pass_3'] = model_results[suggest_3][0]
        data_struct['bits_3'] = model_results[suggest_3][1]
        data_struct['screen_3'] = hidder(model_results['rawPassword'], model_results[suggest_3][0])
        # print(hidder(model_results['rawPassword'], model_results[suggest_3][0]))
        temp_hack_time, temp_unit = uis.hack_time(model_results[suggest_3][1])
        data_struct['hack_time_3'] = temp_hack_time
        data_struct['hack_unit_3'] = temp_unit

        # data_struct['pass_4'] = model_results['4'][0]
        # data_struct['bits_4'] = model_results['4'][1]
        # temp_hack_time, temp_unit = uis.hack_time(model_results['4'][1])
        # data_struct['hack_time_4'] = temp_hack_time
        # data_struct['hack_unit_4'] = temp_unit

        # data_struct['pass_5'] = model_results['5'][0]
        # data_struct['bits_5'] = model_results['5'][1]
        # temp_hack_time, temp_unit = uis.hack_time(model_results['5'][1])
        # data_struct['hack_time_5'] = temp_hack_time
        # data_struct['hack_unit_5'] = temp_unit

        # data_struct['pass_6'] = model_results['6'][0]
        # data_struct['bits_6'] = model_results['6'][1]
        # temp_hack_time, temp_unit = uis.hack_time(model_results['6'][1])
        # data_struct['hack_time_6'] = temp_hack_time
        # data_struct['hack_unit_6'] = temp_unit
        #
        # data_struct['pass_7'] = model_results['7'][0]
        # data_struct['bits_7'] = model_results['7'][1]
        # temp_hack_time, temp_unit = uis.hack_time(model_results['7'][1])
        # data_struct['hack_time_7'] = temp_hack_time
        # data_struct['hack_unit_7'] = temp_unit

        data_struct['policy_based'] = uis.policy_based_feedback()
        #(model_results['1'][0], model_results['1'][1],
        # data_struct['2'] = (model_results['2'][0], model_results['2'][1], uis.hack_time(model_results['2'][1]))
        # data_struct['3'] = (model_results['3'][0], model_results['3'][1], uis.hack_time(model_results['3'][1]))
        # data_struct['4'] = (model_results['4'][0], model_results['4'][1], uis.hack_time(model_results['4'][1]))
        # data_struct['5'] = (model_results['5'][0], model_results['5'][1], uis.hack_time(model_results['5'][1]))
        # data_struct['6'] = (model_results['6'][0], model_results['6'][1], uis.hack_time(model_results['6'][1]))
        # data_struct['7'] = (model_results['7'][0], model_results['7'][1], uis.hack_time(model_results['7'][1]))

        return data_struct
    except Exception as e:
        log.exception("UI_Collections error")



