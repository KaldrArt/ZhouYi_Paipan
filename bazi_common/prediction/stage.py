

class Stage:
    """
    阶段
    一个阶段由多个step组成

    每个阶段，接受到的结果，都是上一个阶段的结果。如果当前阶段是第一个阶段，则没有上一个结果。

    """

    def __init__(self,
                 stage_name: str,
                 stage_ob: object,
                 steps=[]
                 ):
        pass

    def next_step(self):
        pass
