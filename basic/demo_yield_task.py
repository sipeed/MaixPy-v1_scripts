class Task:

    def __init__(self, event=(lambda: print('task running'))):
        self.event = event
        self.cb = self.pre()
        next(self.cb)
        print('task init')

    def pre(self):
        print('task start')
        flag = True
        while flag is True:
            flag = yield flag
            self.event()
        print('task exit')

    def run(self, flag=True):
        try:
            res = self.cb.send(flag)
            return res
        except StopIteration as e:
            return False


if __name__ == "__main__":
    tmp = Task()

    assert(tmp.run())
    assert(tmp.run())
    assert(False == tmp.run(False))

    print(tmp.run())
    print(tmp.run(False))

    class music:

        def __init__(self):
            self.task = Task(self.pre)
            self.args = None
            print('music init')

        def pre(self):
            print('pre ', self.args)

        def play(self, size=10):
            self.args = list(range(size))
            print(self.task.run())

        def stop(self):
            print(self.task.run(False))
            self.__init__()

        def loop(self):
            self.alive = False
            while self.alive:
                self.play()
            stop()

    tmp = music()
    tmp.play()
    tmp.stop()
    tmp.play()
