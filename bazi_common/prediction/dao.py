class Dao:
    """
    道
    什么是道？就是日月天地与自身的作用规律和关系
    道对象用于Stage、Step和Rule中。
    道对象有基本的属性，这些属性将在运算中进行传递。

    道就是一个可运算对象。
    这个对象的运算规则，在stage中，stage有多个step，step有
    一个或者多个rule，rule包括对象、作用关系、关系的运算结果。

    rule，就是动的跟静的作用。
    step，就是在某个范围内，寻找动与静。
    stage，就是几个不同的阶段、不同断命的方法，由step组成。
    但是道dao，只能与rule作用，每次计算，都只计算一个rule。

    当前需要解决几个问题，我做了这套程序，那么要尽可能让其他编写算法的人，能够基于我这套程序进行算法的编写，而不是只能我用来写程序，其他人不能使用。
    如果程序本身，不能够实现手工制定断法，那么就等于没有办法实现易学各类计算。

    """

    def __init__(self,
                 basic_info,
                 result_class):
        self.basic_info = basic_info
        self.result_class = result_class

    def rule(self):
        pass

    def step(self):
        pass

    def stage(self):
        pass
