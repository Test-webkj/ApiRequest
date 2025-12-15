import allure
import jsonpath

from HAT.core.globalContext import g_context


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