def even_nums():
    num = 0
    while True:
        yield num
        num += 2

### OR ###
def even_range(stop, start=0):
    it = start
    while it < stop:
        yield it
        it += 2
### or lazy 
#    for i in range(start, stop, step=2):
#        yield i
