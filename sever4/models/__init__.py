import json


def save(data, path):
    """
    本函数把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    # json 是一个序列化/反序列化 list/dict 的库
    # indent 是缩进
    # ensure_ascii=False 用于保存中文
    #json.dumps 序列化得到json格式字符串
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    """
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        #字符串转字典
        return json.loads(s)


# Model 是用于存储数据的基类
class Model(object):
    # @classmethod 说明这是一个 类方法
    # 类方法的调用方式是  类名.类方法()
    @classmethod
    def db_path(cls):
        # classmethod 有一个参数是 class
        # 所以我们可以得到 class 的名字
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        # 下面一句相当于 User(form) 或者 Msg(form)
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        """
        得到一个类的所有存储的实例 在序列中
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    def save(self):
        """
        save 函数用于把一个 Model 的实例保存到文件中
        """
        models = self.all()
        log('models', models)
        models.append(self)
        # __dict__ 是包含了对象所有属性和值的字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def __repr__(self):
        """
        这是一个 魔法函数 返回 string representation of a object
        当调用 str(oject) 的时候
        若没有 __str__
        就调用 __repr__
        """
        #类名
        classname = self.__class__.__name__
        #所有的属性和值
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)

