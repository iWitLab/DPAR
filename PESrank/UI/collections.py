import json
import os
import math
import sys
import yaml as yml
import logging
import json


log = logging.getLogger(__name__)
ymlz = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'collections.yaml')


class Collections:
    def __init__(self, model_results):
        self.name = 'UI_Data'
        self.password = model_results['rawPassword']
        self.modelRank = model_results['modelRank']
        self.finalPrefix = model_results['finalPrefix']
        self.finalunL33tBaseWord = model_results['finalunL33tBaseWord']
        self.unShiftBaseWord = model_results['unShiftBaseWord']
        self.finalSuffix = model_results['finalSuffix']
        self.upperList = (model_results['upperList'].replace('(', '').replace(')', '').split(','))
        self.l33tList = (model_results['l33tList'].replace('(', '').replace(')', '').split(','))
        self.bits = model_results['bits']
        self.prefix_q = model_results['prefix_q']
        self.base_q = model_results['base_q']
        self.suffix_q = model_results['suffix_q']
        self.l33t_q = model_results['l33t_q']
        self.upper_q = model_results['upper_q']
        self.nonePrefixProbFlag = model_results['nonePrefixProbFlag']
        self.noneBaseProbFlag = model_results['noneBaseProbFlag']
        self.noneSuffixProbFlag = model_results['noneSuffixProbFlag']
        self.noneL33tProbFlag = model_results['noneL33tProbFlag']
        self.noneUpperProbFlag = model_results['noneUpperProbFlag']
        self.CONF = self.load_yml()
        self.prefixLEN = len(self.finalPrefix)
        self.baseLEN = len(self.finalunL33tBaseWord)
        self.suffixLEN = len(self.finalSuffix)
        self.l33tLEN = len(self.l33tList)
        self.capitalization_len = len(self.upperList)
        self.passwordLEN = len(self.password)
        self.L33tDictionary = {
            "1": ['0', 'o'],
            "12": ['1', 'i'],
            "13": ['!', 'i'],
            "2": ['@', 'a'],
            "3": ['4', 'a'],
            "6": ['3', 'e'],
            "4": ['$', 's'],
            "5": ['5', 's'],
            "11": ['2', 'z'],
            "14": ['%', 'x'],
            "10": ['7', 't'],
            "9": ['+', 't'],
            "8": ['9', 'g'],
            "7": ['6', 'g']
        }
        self.percentile_list = [
            13.24859472, 14.42324725, 15.2374284575, 15.755646788, 16.15404673, 16.63784183, 17.06499005, 17.34642283,
            17.7739242615, 18.182770165, 18.42983578, 18.78947156, 19.0926284175, 19.35078814, 19.8629415, 20.106741322,
            20.50156267, 20.812093537, 21.13520325, 21.45168226, 21.814673148, 22.11742918, 22.44605648, 22.839035824,
            23.10084421, 23.42630238, 23.68773699, 23.98472949, 24.30267793, 24.67071828, 24.9384517, 24.941169904,
            25.47450467, 25.47774298, 25.6474491475, 26.38903894, 26.38903894, 26.551261364, 26.68920037, 28.00932085,
            28.00932085, 28.00932085, 28.00932085, 28.00932085, 28.0117389275, 28.15824243, 28.16699803, 28.30598698,
            28.5699445715, 28.72491908, 28.99422883, 29.280241468, 29.751278853, 30.018638464, 30.41850239, 30.63241893,
            31.14530246, 31.48809705, 31.9353144625, 32.29923727, 32.6540543995, 33.12542087, 33.62225115, 33.98102749,
            34.50686336, 35.0076034, 35.55838062, 35.9731108, 36.49199365, 36.94355704, 36.94355704, 36.94355704,
            36.94355704, 36.94355704, 36.94355704, 36.94355704, 36.94355704, 36.94355704, 36.94355704, 36.94355704,
            37.17040478, 37.638063613, 38.238989061, 39.229159418, 39.8424821025, 40.93851966, 41.81565807,
            42.858404738, 43.5212397, 44.375470485, 45.2446347675, 46.31762342, 47.7464271855, 49.026142429,
            50.557006295, 52.860584706, 55.3829779965, 58.527121049, 62.8413292, 100.8216949
        ]
        self.fallback_percentile = model_results['percentile']
        self.percentile = self.find_precentile()
        self.guesses_per_second = 3600000 #100000000
        self.recommendations = {
            "1": model_results['1'],
            "2": model_results['2'],
            "3": model_results['3'],
            "4": model_results['4'],
            "5": model_results['5'],
            "6": model_results['6'],
            "7": model_results['7']
        }

    def hack_time(self, user_bits):
        hack_calc = float((math.pow(2, (float(user_bits)))) / (self.guesses_per_second))
        if hack_calc / 29030400000 > 1:
            hack_calc = round(hack_calc/29030400000, 2)
            hack_unit = 'millennia'
        elif hack_calc / 2903040000 > 1:
            hack_calc = round(hack_calc/2903040000, 2)
            hack_unit = 'centuries'
        elif hack_calc / 29030400 > 1:
            hack_calc = round(hack_calc/29030400, 2)
            hack_unit = 'years'
        elif hack_calc / 2419200 > 1:
            hack_calc = round(hack_calc/2419200, 2)
            hack_unit = 'months'
        elif hack_calc / 604800 > 1:
            hack_calc = round(hack_calc/604800, 2)
            hack_unit = 'weeks'
        elif hack_calc / 86400 > 1:
            hack_calc = round(hack_calc/86400, 2)
            hack_unit = 'days'
        elif hack_calc / 3600 > 1:
            hack_calc = round(hack_calc/3600, 2)
            hack_unit = 'hours'
        elif hack_calc / 60 > 1:
            hack_calc = round(hack_calc/60, 2)
            hack_unit = 'minutes'
        elif hack_calc > 1:
            hack_calc = round(hack_calc, 2)
            hack_unit = 'seconds'
        else:
            hack_calc = 'Instantly'
            hack_unit = ''
        return hack_calc, hack_unit

    def count_symbols(self, test):
        chars = ['[', ']', '=', '±', '§', '@', '_', '!', '#', '$', '%', '-', '^', '&', '*', '(', ')', '<', '>', '?', '/', "'", '"', '|', '+', '{', '}', '~', '`', ':', ';', '\\']
        counter = 0
        for item in test:
            if item in chars:
                counter += 1

        return counter

    def count_digits(self, test):
        chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        counter = 0
        for item in test:
            if str(item) in chars:
                counter += 1

        return counter

    def count_upper(self, test):
        counter = 0
        for item in test:
            if item.isupper():
                counter += 1

        return counter

    def policy_based_feedback(self):
        print("This is the raw", self.password)
        feedback = []
        lengthz = len(self.password)
        if lengthz == 8:
            feedback.append(self.CONF['length_8'])
        elif lengthz == 9:
            feedback.append(self.CONF['length_9'])
        elif lengthz == 10:
            feedback.append(self.CONF['length_10'])
        elif lengthz == 11:
            feedback.append(self.CONF['length_11'])
        elif lengthz == 12:
            feedback.append(self.CONF['length_12'])

        if self.count_symbols(self.password) == 0:
            feedback.append(self.CONF['no_symbols'])
        elif self.count_symbols(self.password) == 1:
            feedback.append(self.CONF['one_symbols'])

        if self.count_digits(self.password) == 0:
            feedback.append(self.CONF['no_digits'])
        elif self.count_digits(self.password) == 1:
            feedback.append(self.CONF['one_digits'])

        if self.count_upper(self.password) == 0:
            feedback.append(self.CONF['no_capital'])
        elif self.count_upper(self.password) == 1:
            feedback.append(self.CONF['one_capital'])

        if self.password.isdigit():
            feedback.append(self.CONF['no_letters'])

        return feedback


    def find_precentile(self):
        for i in range(len(self.percentile_list)):
            if i == 0:
                if float(self.bits) <= float(self.percentile_list[i]):
                    return i + 1
            elif i == 99:
                if float(self.bits) >= float(self.percentile_list[i]):
                    return i + 1
            else:
                if float(self.percentile_list[i]) <= float(self.bits) < float(self.percentile_list[i+1]):
                    return i + 1
        return self.fallback_percentile

    def load_yml(self):
        with open(ymlz) as file:
            return yml.load(file, Loader=yml.FullLoader)

    def mask_password(self, lenz, mask):
        return "".join(map(lambda x: x * lenz, mask))

    def password_l33ts(self, base_text):
        if self.l33tList[0] == '':
            return base_text
        else:
            letters = []
            tempo = []
            j = 0
            try:
                l33t_list = self.l33tList
                fixed_l33t = []
                for item in l33t_list:
                    item = item.replace(' ','')
                    fixed_l33t.append(item)
                for i in fixed_l33t:
                    if not i == '':
                        l33t_val = self.L33tDictionary[str(i)]
                        l33t_letter = str(l33t_val[0])
                        letters.append(l33t_letter)
                for letter in self.unShiftBaseWord:
                    if letter in letters:
                        letter = "S"
                        tempo.append(str(letter))
                        j += 1
                    else:
                        letter = base_text[j]
                        tempo.append(str(letter))
                        j += 1
                base_text = "".join(tempo)
            except Exception as e:
                log.critical("{} error: {}".format(self.name, e))
        return base_text

    def password_uppers(self, base_text):
        if self.upperList[0] == '':
            return base_text
        else:
            try:
                for i in self.upperList:
                    if not i == '':
                        if int(i) < 0:
                            i = int(i)
                            i = self.baseLEN + i
                            temp = list(base_text)
                            temp[int(i)] = "C"
                            base_text = "".join(temp)
                        else:
                            temp = list(base_text)
                            temp[int(i)] = "C"
                            base_text = "".join(temp)
                return base_text
            except Exception as e:
                log.critical("{} error: {}".format(self.name, e))

    def build_password(self):
        if self.prefixLEN == 0:
            prefix_text = self.mask_password(4, '_')
        else:
            prefix_text = self.mask_password(self.prefixLEN, 'x')

        if self.baseLEN == 0:
            base_text = self.mask_password(6, '_')
        else:
            base_text = self.mask_password(self.baseLEN, 'x')
            base_text = self.password_uppers(base_text)
            base_text = self.password_l33ts(base_text)

        if self.suffixLEN == 0:
            suffix_text = self.mask_password(4, '_')
        else:
            suffix_text = self.mask_password(self.suffixLEN, 'x')
        return prefix_text + " | " + base_text + " | " + suffix_text

    def collect_general(self):
        strength = ''
        if self.bits < self.CONF['Lowest']:
            strength = str(self.CONF['Very_weak'])
        elif self.bits < self.CONF['Medium']:
            strength = str(self.CONF['Weak'])
        elif self.bits < self.CONF['Highest']:
            strength = str(self.CONF['Fair'])
        elif self.bits >= self.CONF['Highest']:
            strength = str(self.CONF['Strong'])
        return strength, str(100 - round(self.percentile)) + '%'

    def collect_base(self):
        if self.noneBaseProbFlag is True:
            base_message = self.CONF['base_message_not_in_dict1']
            base_advise = self.CONF['base_message_not_in_dict2']
            return base_message, base_advise
        else:
            if self.baseLEN == 0:
                base_message = self.CONF['base_message_null1']
                base_advise = self.CONF['base_message_null2']
            elif self.base_q <= self.CONF['base_lowest']:
                base_message = self.CONF['base_message_low1']
                base_advise = self.CONF['base_message_low2']
            elif self.base_q <= self.CONF['base_medium']:
                base_message = self.CONF['base_message_medium1']
                base_advise = self.CONF['base_message_medium2']
            elif self.base_q <= self.CONF['base_highest']:
                base_message = self.CONF['base_message_ok1']
                base_advise = self.CONF['base_message_ok2']
            elif self.base_q > self.CONF['base_highest']:
                base_message = self.CONF['base_message_highest1']
                base_advise = self.CONF['base_message_highest2']
            else:
                base_message = ''
                base_advise = ''
            return base_message, base_advise

    def collect_prefix(self):
        if self.prefixLEN == 0:
            prefix_message = self.CONF['prefix_message_null1']
            prefix_advise = self.CONF['prefix_message_null2']
        else:
            if self.nonePrefixProbFlag:
                prefix_message = self.CONF['prefix_message_not_in_dict1']
                prefix_advise = self.CONF['prefix_message_not_in_dict2']
            elif self.prefix_q <= self.CONF['prefix_highest']:
                prefix_message = self.CONF['prefix_message_low1']
                prefix_advise = self.CONF['prefix_message_low2']
            else:
                prefix_message = self.CONF['prefix_message_high1']
                prefix_advise = self.CONF['prefix_message_high2']
        return prefix_message, prefix_advise

    def collect_suffix(self):
        if self.suffixLEN == 0:
            suffix_message = self.CONF['suffix_message_null1']
            suffix_advise = self.CONF['suffix_message_null2']
        else:
            if self.noneSuffixProbFlag is True:
                suffix_message = self.CONF['suffix_message_not_in_dict1']
                suffix_advise = self.CONF['suffix_message_not_in_dict2']
            elif self.suffix_q <= self.CONF['suffix_highest']:
                suffix_message = self.CONF['suffix_message_low1']
                suffix_advise = self.CONF['suffix_message_low2']
            else:
                suffix_message = self.CONF['suffix_message_high1']
                suffix_advise = self.CONF['suffix_message_high2']
        return suffix_message, suffix_advise

    def collect_l33t(self):
        if self.l33tLEN == 0:
            l33t_message = self.CONF['l33t_message_null1']
            l33t_advise = self.CONF['l33t_message_null2']
        else:
            if self.noneL33tProbFlag:
                l33t_message = self.CONF['l33t_message_not_in_dict1']
                l33t_advise = self.CONF['l33t_message_not_in_dict2']
            elif self.l33t_q <= self.CONF['l33t_highest']:
                l33t_message = self.CONF['l33t_message_low1']
                l33t_advise = self.CONF['l33t_message_low2']
            else:
                l33t_message = self.CONF['l33t_message_high1']
                l33t_advise = self.CONF['l33t_message_high2']
        return l33t_message, l33t_advise

    def collect_capitalization(self):
        if self.capitalization_len == 0:
            capital_message = self.CONF['capitalization_message_null1']
            capital_advise = self.CONF['capitalization_message_null2']
        else:
            if self.noneL33tProbFlag:
                capital_message = self.CONF['capitalization_message_not_in_dict1']
                capital_advise = self.CONF['capitalization_message_not_in_dict2']
            elif self.upper_q <= self.CONF['caps_highest']:
                capital_message = self.CONF['capitalization_message_low1']
                capital_advise = self.CONF['capitalization_message_low2']
            else:
                capital_message = self.CONF['capitalization_message_high1']
                capital_advise = self.CONF['capitalization_message_high1']
        return capital_message, capital_advise

    def should_hide_advise(self):
        return str(self.bits > self.CONF['Highest'])

    def is_unique_base(self):
        return self.noneBaseProbFlag

