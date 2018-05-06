class MySQL:
    def __init__(self,host,port):
        self.host=host
        self.port=port

    @staticmethod
    def from_conf():
        return MySQL('192.168.1.1', '8080')

    # @classmethod #哪个类来调用,就将哪个类当做第一个参数传入
    # def from_conf(cls):
    #     return cls('192.168.1.1', '8080')

    def __str__(self):
        return '就不告诉你'

class Mariadb(MySQL):   # 继承MySQL类
    def __str__(self):
        return '<%s:%s>' %(self.host,self.port)

 # 调用staticmethod时，获得是MySQL类的对象，所以打印的是MySQL类中的__str__内置方法，结果为'就不告诉你'，
 # 调用classmethod时，获得的是Mariadb的对象，所以打印的是Mariadb类中的__str__内置方法
m=Mariadb.from_conf()
print(m) #我们的意图是想触发Mariadb.__str__,但是结果触发了MySQL.__str__