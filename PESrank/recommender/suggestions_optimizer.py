import logging

log = logging.getLogger(__name__)


class Optimized():
    def __init__(self, optimization_vector, returns=3):
        self.name = "Optimizer_module"
        self.authors = ["anonymized"]
        self.optimization_vector = optimization_vector
        self.max_lev = len(self.optimization_vector[0]) * 2
        self.min_lev = 0
        self.max_bits = 150
        self.min_bits = 0
        self.to_return = returns
        self.struct = {
            "1": ("", 0),
            "2": ("", 0),
            "3": ("", 0),
            "4": ("", 0),
            "5": ("", 0),
            "6": ("", 0),
            "7": ("", 0)
        }

    def clean_opt_vector(self):
        new_vector = []
        optimizer_vector = self.optimization_vector
        for items in optimizer_vector:
            new_vector.append((items[0], items[1], items[2]))
        return new_vector

    def basic_optimization(self):
        new_vector = []
        cleaned_optimizer_vector = self.clean_opt_vector()
        for item in cleaned_optimizer_vector:
            try:
                normalized_bits = round((float(item[1]) / (float(self.max_bits) - float(self.min_bits))), 3)
                normalized_lev = round((1 - (item[2] / (self.max_lev - self.min_lev))), 3)
                suggestion_score = round(((normalized_lev + normalized_bits) / 2), 3)
                new_vector.append((item[0].replace('\\\\', '\\'), item[1], item[2], normalized_bits, normalized_lev,
                                   suggestion_score, len(item[0].replace('\\\\', '\\'))))
            except:
                continue
        new_vector = sorted(set(new_vector), key=lambda tup: tup[5], reverse=True)[0:self.to_return]
        return new_vector

    def max_list(self):
        cleaned_optimizer_vector = self.clean_opt_vector()
        for item in cleaned_optimizer_vector:
            temp_index = str(item[2])
            if temp_index in self.struct:
                if item[1] > self.struct[temp_index][1]:
                    self.struct[temp_index] = (item[0].replace('\\\\', '\\'), item[1])
        return self.struct