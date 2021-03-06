def event():
    print('start yield')
    # return next(task) and yield next(task.send('set_two'))
    one = yield 'get_one'
    assert(one == 'set_two')
    print(one)
    yield 'get_two'  # return next(task) and yield next(task.send('set_two'))
    print('exit yield')
    yield  # yield next() to exit or raise StopIteration


task = event()
run_one = next(task)  # need next(task) init and next(task) == task.send(None)
# so next(task) => yield 'get_one' => run_one = 'get_one'
assert(run_one == 'get_one')
run_two = task.send('set_two')
assert(run_two == 'get_two')
print('run : ', run_one, ' and ', run_two)

try:
    next(task)
    print('run end')
    next(task)  # will raise StopIteration
except Exception as e:
    print('yield StopIteration')

if __name__ == '__main__':

    def task():
        while True:
            print('hello')
            yield

    tmp = task()
    while True:
        next(tmp)

    while True:
        print('hello')
