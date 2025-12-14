#全局变量类
class g_context:
    _dic = {} #设置一个类变量

    #g_context().set_dict("name", "张三")  _dic = {"name": "张三"}
    # 添加字典值
    def set_dict(self, key, value):
        self._dic[key] = value

    # dic 完整的字典 g_context().set_by_dict（"age":"18"） _dic = {"name": "张三", "age": "18"}
    def set_by_dict(self, dic):
        self._dic.update(dic)

    # 得到字典值 g_context().get_dict("name")
    def get_dict(self, key):
        return self._dic.get(key, None)

    # _dic = {"name": "张三", "age": "18"}
    def show_dict(self):
        return self._dic