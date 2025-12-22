import allure
import jsonpath
from PIL.ImageChops import screen
from deepdiff import DeepDiff

from HAT.core.globalContext import g_context

# 接口请求进行二次封装
class Keywords:

    def __init__(self,request):
        self.request=request

    @allure.step("发送请求POST")
    def 发送请求POST(self,**kwargs):
        url=kwargs.get('请求地址',None)
        params=kwargs.get('URL参数',None)
        headers=kwargs.get('请求头',None)
        data=kwargs.get('请求数据',None)
        files=kwargs.get('文件列表',[])
        data_type=kwargs.get('请求类型',"data").lower()#默认请求类型
        request_data={
            "url":url,
            "params":params,
            "headers":headers,
            "files":files,
        }
        # 如果json   request_data['json']= data
        if data_type=="json":
            request_data["json"]=data
        elif data_type=="data":  #request_data['json']= data
            request_data["data"]=data
        else:
            raise Exception("请求类型错误")
        try:
            # self.request  必须是什么值才能发请求？  requests.request()
            response=self.request.request("post",**request_data)
            print("登陆响应数据",response.json())
            g_context().set_dict("响应结果",response)
            # 保存数据的逻辑  xxx
        except Exception as e:
            print("请求错误",e)
        return response

    @allure.step("发送请求GET")
    def 发送请求GET(self,**kwargs):
        url = kwargs.get('请求地址', None)
        params = kwargs.get('URL参数', None)
        headers = kwargs.get('请求头', None)
        data = kwargs.get('请求数据', None)
        files = kwargs.get('文件列表', [])
        request_data = {
            "url": url,
            "params": params,
            "headers": headers,
            "files": files,
        }
        response = self.request.request("get", **request_data)
        return response

    @allure.step("提取数据JSON")
    def 提取数据JSON(self,**kwargs):
        # 获取jsonpath表达式  $..msg  $..token
        EXPRESSION=kwargs.get("表达式",None)
        # 获取下标 不填下标就给你0  默认取第一个数据
        INDEX=kwargs.get("下标",None)
        if INDEX is None:
            INDEX=0

        response=g_context().get_dict("响应结果").json()
        result=jsonpath.jsonpath(response,EXPRESSION)
        if not result:
            raise Exception(f"没有找到对应的数据:{EXPRESSION}")
        ex_data=result[INDEX]
        # 设置到全局变量中去  {"msg_token": '1a8080e503afb6a24e23396aa654cccb'}
        g_context().set_dict(kwargs["变量名"],ex_data)
        print("全局变量",g_context().show_dict())


    # assert 期望结果==实际结果，"错误时显示信息"
    def 断言文本(self,**kwargs):
        #比较器  预期结果和实际结果真实对比的地方
        comparators={
            "==":lambda a,b:a==b,
            ">=":lambda a,b:a>=b,
            "<=":lambda a,b:a<=b,
            "!=":lambda a,b:a!=b,
            ">":lambda a,b:a>b,
            "<":lambda a,b:a<b,
            "in":lambda a,b:a in b,
        }

        message=kwargs.get("错误信息",None) #用例中有没有传错误信息
        operators=kwargs.get("比较符","==")#用例中有没有传比较符 没有就默认==   <>
        compare_type=kwargs.get("断言类型","文本")#用例中有没有传断言类型 没有就默认文本

        # 如果传过来的比较符不在比较器里面，就报错
        if operators not in comparators:
            raise Exception(f"没有对应的比较符:{operators}")

        # 对于期望结果，如果是数字，就转换成数字类型，否则就转换成字符串类型
        if compare_type=="数字":
            kwargs["期望结果"]=float(kwargs["期望结果"])
        else:
            kwargs["期望结果"]=str(kwargs["期望结果"])

        # == sj_msg,登陆成功   sj_msg==登陆成功 相等 True  不相等 False
        # if not True: ==if false 不执行下面的内容,，没有提示
        # if not False: ==if true 执行下面的内容
        if not comparators[operators](kwargs["实际结果"],kwargs["期望结果"]):
            if message:#如果有传错误信息 就用自定义错误信息
                raise Exception(message)
            else:#没有传错误信息 就用默认错误信息
                raise AssertionError(f"{kwargs['实际结果']} {operators} {kwargs['期望结果']}")

    def 断言文本相等(self,**kwargs):
        kwargs.update({"比较符":"=="})
        self.断言文本(**kwargs)

    def 断言文本包含(self, **kwargs):
        kwargs.update({"比较符": "in"})
        self.断言文本(**kwargs)

    def 断言文本不相等(self, **kwargs):
        kwargs.update({"比较符": "!="})
        self.断言文本(**kwargs)

    def 断言数字大于等于(self, **kwargs):
        kwargs.update({"比较符": ">=", "断言类型": "数字"})
        self.断言文本(**kwargs)

    def 断言数字小于等于(self, **kwargs):
        kwargs.update({"比较符": "<=", "断言类型": "数字"})
        self.断言文本(**kwargs)

    def 断言数字小于(self, **kwargs):
        kwargs.update({"比较符": "<", "断言类型": "数字"})
        self.断言文本(**kwargs)

    def 断言数字大于(self, **kwargs):
        kwargs.update({"比较符": ">", "断言类型": "数字"})
        self.断言文本(**kwargs)

    def 断言数字不等于(self, **kwargs):
        kwargs.update({"比较符": "!=", "断言类型": "数字"})
        self.断言文本(**kwargs)


    def 批量断言(self,**kwargs):
        try:
            sjmsg=g_context().get_dict("响应结果").json()#实际结果
            exmsg=kwargs["期望结果"]#预期结果

            exclude_paths=kwargs.get("过滤字段",[])
            ignore_order=kwargs.get("忽略顺序",True)
            ignore_string_case=kwargs.get("忽略大小写",True)

            screen_data={
                "exclude_paths":exclude_paths,
                "ignore_order":ignore_order,
                "ignore_string_case":ignore_string_case
            }
            diff=DeepDiff(sjmsg,exmsg,**screen_data)
        except Exception as e:
            assert False,f"批量断言失败:{e}"
        assert not diff,f"批量断言失败:{diff.pretty()}"