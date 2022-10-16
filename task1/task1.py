import random
from datetime import datetime

def time_calc(time_list):
    def decorator(func):
        def wrapped(*args, **kwargs):
            start_time = datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.now()
            res_time = start_time - end_time
            time_list.append(res_time.microseconds)
            return result
        return wrapped
    return decorator


def fill_array(size=1000000, start=0, end=999):
    random_list = []
    for i in range(size):
        random_list.append(random.randint(start, end))
    return random_list


time_list = [] #microsec
@time_calc(time_list)
def calc_hist(some_list):
    hist = [0 for i in range(10)]
    for i in some_list:
        hist[i // 100] += 1
    return hist


def main():
    data_list = fill_array()
    for i in range(100):
        calc_hist(data_list)
    print('Minimum time: {:.3f} seconds'.format(min(time_list) / 1000000))
    print('Maximum time: {:.3f} seconds'.format(max(time_list) / 1000000))
    print('Average time: {:.3f} seconds'.format(sum(time_list) / len(time_list) / 1000000))


if __name__ == "__main__":
    main()
