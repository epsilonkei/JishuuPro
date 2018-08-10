from multiprocessing import Pool

class Test:
    def fuga(self, x):
        return x*x

    def hoge(self):
        p = Pool(8)
        print p.map(self.fuga, range(10))

if __name__ == "__main__":
    test = Test()
    test.hoge()
