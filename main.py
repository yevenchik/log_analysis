from collections import Counter
import re


class ErrorAnalyzer:
    @staticmethod
    def sandwich_checker(log, top, bottom, filling=None):
        top_counter = 0
        bottom_counter = 0
        with open(log, 'r') as log_file:
            log_as_list = log_file.readlines()
            top_index = 0
            bottom_index = 0
            for i in range(len(log_as_list)):
                top_counter, top_index = ErrorAnalyzer.handle_top(bottom_counter, i, log_as_list, top, top_counter,
                                                                  top_index)
                bottom_counter = ErrorAnalyzer.handle_bottom(bottom, bottom_counter, filling, i, log_as_list,
                                                             top_counter, top_index)
            if top_counter > bottom_counter:
                ErrorAnalyzer.log_summary(top + "\t->\t sandwich top with no bottom\n")
                if filling:
                    ErrorAnalyzer.handle_filling_check(len(log_as_list), filling, log_as_list, top_index)

    @staticmethod
    def handle_bottom(bottom, bottom_counter, filling, i, log_as_list, top_counter, top_index):
        if bottom in log_as_list[i]:
            bottom_counter += 1
            bottom_index = i
            if top_counter < bottom_counter:
                ErrorAnalyzer.log_summary(bottom + "\t->\t sandwich bottom with no top\n")
                bottom_counter -= 1
            elif filling:
                ErrorAnalyzer.handle_filling_check(bottom_index, filling, log_as_list, top_index)
        return bottom_counter

    @staticmethod
    def handle_top(bottom_counter, i, log_as_list, top, top_counter, top_index):
        if top in log_as_list[i]:
            top_counter += 1
            top_index = i
            if top_counter > bottom_counter + 1:
                ErrorAnalyzer.log_summary(top + "\t->\t sandwich top with no bottom\n")
                top_counter -= 1
        return top_counter, top_index

    @staticmethod
    def handle_filling_check(bottom_index, filling, log_as_list, top_index):
        does_have_filling = ErrorAnalyzer.filling_checker(log_as_list[top_index:bottom_index], filling)
        if does_have_filling:
            ErrorAnalyzer.log_summary(filling + "\t->\t filling found\n")
        else:  # YE TODO: decide if to check filling or not filling!!!
            ErrorAnalyzer.log_summary(filling + "\t->\t filling not found\n")

    @staticmethod
    def filling_checker(log_sandwich, filling):
        for log in log_sandwich:
            if filling in log:
                return True
        return False

    @staticmethod
    def amount_of_same_error(log):  # ye TODO: need to add filter for time and variables!!!
        with open(log, 'r') as lines:
            log_lines = lines.readlines()
            counter = dict(Counter(log_lines))
            with open('error_count.txt', 'w') as count_result:
                for key in counter.keys():
                    count_result.write("{} = {}\n".format(re.sub('\n', '', key), counter[key]))

    @staticmethod
    def merge_logs(logs, merged_log_name):
        merged_log = ''
        for log in logs:
            merged_log = ErrorAnalyzer.merge_single_log(log, merged_log)
        ErrorAnalyzer.final_log_merge(merged_log, merged_log_name)

    @staticmethod
    def final_log_merge(merged_log, merged_log_name):
        with open(merged_log_name, 'a') as merged:
            merged.write(merged_log)

    @staticmethod
    def merge_single_log(log, merged_log):
        with open(log, 'r') as f:
            log_n = f.read()
            merged_log += log_n
            merged_log += '\n'
        return merged_log

    def time_between_same_log_average(self, logs):
        pass

    def same_log_time_deviation_and_location(self, logs):
        pass

    def clean_up_logs(self, logs):
        pass
        # ye TODO: reuse writen code

    @staticmethod
    def log_summary(results):
        with open('result_summary.txt', 'a') as result:
            result.write(results)


def json_loader(json):
    pass
    # ye TODO: reuse XR code


if __name__ == '__main__':
    e = ErrorAnalyzer()
    e.merge_logs(['1.txt', '2.txt'], 'merged_log.txt')
    e.amount_of_same_error('merged_log.txt')
    e.sandwich_checker('merged_log.txt', '5', '7', '6')
    e.sandwich_checker('merged_log.txt', 'a', 'b')
    e.merge_logs(['result_summary.txt', 'error_count.txt'], 'final_result.txt')
