import numpy as np

def triangle(a):
    side = 2 * a + 1
    height = a + 1
    for i in range(height):
        row = ''
        for i in range(a):
            row += ' '
        for i in range(side - 2 * a):
            row += '*'
        for i in range(a):
            row += ' '
        a -=  1
        print(row)

def hist_distance(hist1, hist2):
    #return np.linalg.norm(hist1 - hist2) 
    if len(hist1) != len(hist2):
        raise Exception("histogramm lens must be equal")
    square_distance = 0
    for i in range(len(hist1)):
        square_distance += (hist1[i] - hist2[i]) ** 2
    
    return square_distance ** 0.5


def read_hist(filename):
    with open(filename, 'r') as f:
        return np.array([int(x) for x in f.read().split()])


def write_hist(hist, filename='./files/res_hist.txt'):
    with open(filename, 'w') as f:
        f.write(' '.join([str(i) for i in hist]))


if __name__ == '__main__':
    triangle(3)
    hist1 = np.array((1, 2, 3, 4))
    hist2 = np.array((4, 5, 6, 8))
    print(hist_distance(hist1, hist2))
    print(read_hist('./files/hist.txt')) 
    write_hist(hist1)
