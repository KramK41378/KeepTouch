class Broken:
    def __enter__(self):
        print(f'Запущено. Делю на 0: ')
        return self

    def div0(self):
        print(0 / 0)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f'Черт, так же нельзя. {exc_type=}, {exc_val=}, {exc_tb=}')
        return True

with Broken() as broken:
    broken.div0()
