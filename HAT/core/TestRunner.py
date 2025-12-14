import copy
import sys

import allure
import pytest
import requests
from tqdm import tqdm

from HAT.core.globalContext import g_context
from HAT.extend.api_keywords import Keywords
from HAT.parse.YamlCaseParser import readYaml, load_context_from_yaml
from HAT.utils.VarRender import refresh


class TestRunner:
    # 用例数据
    load_context_from_yaml(r'F:\request\HAT\examples\api-cases-yaml')
    data=readYaml(r'F:\request\HAT\examples\api-cases-yaml\login.yaml')
    print("yaml用例数据", data)

    @pytest.mark.parametrize("caseinfo", data)  # 列表数据
    def test_case_execute(self, caseinfo):
        keywords = Keywords(requests)
        base_info = caseinfo.get('基础配置', {})  # 测试报告后续用的
        print("数据类型",type(base_info))
        allure.dynamic.parameter("caseinfo", "")
        allure.dynamic.feature(base_info.get("一级模块", "默认模块"))
        allure.dynamic.story(base_info.get("二级模块", "默认模块"))
        allure.dynamic.title(base_info.get("用例标题", '默认用例标题'))

        steps = caseinfo.get('用例步骤', None)

        with tqdm(total=len(steps), desc="开始执行") as pbar:
            for step in steps:  # [{'发送登录接口'：{'操作类型': '发送请求POST', '请求地}}]
                step_name = list(step.keys())[0]  # '发送登录接口'
                step_value = list(step.values())[0]  # {'操作类型': '发送请求POST', '请求地址': 'httpxx
                pbar.set_description(f'{base_info.get("用例标题")}-当前步骤:{step_name}')
                pbar.update(1)
                with allure.step(step_name):
                    # print("没有渲染前的字典值数据", step_value)
                    context = copy.deepcopy(g_context().show_dict())  # 全局变量
                    step_value = eval(refresh(step_value, context))
                    # print("渲染后的字典值数据", step_value)
                    key = step_value['操作类型']  # 发送请求POST  发送请求GET
                    # print("操作类型",key)
                    try:
                        key_func = keywords.__getattribute__(key)  # 去Keywords关键字类中找对应的方法  反射

                    except Exception as e:
                        # print("在keywords类中没有找到对应的方法")
                        sys.path.append('./HAT/key_dir')  # 找目录文件
                        module = __import__(key)  # 导入模块 import 发送请求 POST
                        class_ = getattr(module, key)  # 获取模块中的方法
                        key_func = class_(requests).__getattribute__(key)
                    key_func(**step_value)  # 发送请求POST(接口信息)

