import os
import pytest


pytest_args=['-v','-s','--capture=sys',
             '--clean-alluredir',
             '--alluredir=allure-results',
             'HAT/core/TestRunner.py'
             ]
# 执行用例
pytest.main(pytest_args)
# 生成测试报告
os.system("allure generate allure-results -o allure-report --clean")
