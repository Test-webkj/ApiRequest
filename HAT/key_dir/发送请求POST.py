import allure


class 发送请求POST:
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
            # 保存数据的逻辑  xxx
        except Exception as e:
            print("请求错误",e)
        return response