from jinja2 import Template  # 导入Jinja2模板引擎，用于解析{{}}占位符

def refresh(target,context):
    # 步骤1：把target（字典）转成字符串 → "{'name':'{{age}}', 'age':'18'}"
    # 步骤2：用Template封装这个字符串，识别其中的{{}}占位符
    # 步骤3：调用render(context)，用context里的键值对替换占位符
    return Template(str(target)).render(context)

if __name__ == '__main__':
    target = {'name':'{{age}}',"age":"18"}  # 包含Jinja2占位符的原始数据
    context = {"name":"张三","sex":"男","age":"18"}  # 用于替换占位符的数据源
    r = refresh(target,context)  # 执行替换
    print("新数据",r)  # 输出：新数据 {'name':'18', 'age':'18'}