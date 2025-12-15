import os.path
import yaml
from HAT.core.globalContext import g_context


def readYaml(file_path):
    case_info=[]
    with open(file_path,'r',encoding='utf-8') as f:
        # yaml.load读取   Loader=yaml.FullLoader 安全读取
        data=yaml.load(f,Loader=yaml.FullLoader)
    case_info.append(data)
    return case_info


# 专门读取context.yaml文件数据
def load_context_from_yaml(file_path):
    """
    :param file_path: 目录文件夹
    :return:
    """
    yaml_file_path=os.path.join(file_path, 'context.yaml')
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        if data:g_context().set_by_dict(data)
        print("全局变量", g_context().show_dict())

# 读取文件夹下的yaml文件
def load_yaml_files(file_path):
    yaml_caseInfos=[]
    # 扫描用例文件夹
    suite_folder=os.path.join(file_path)
    # context.yaml放到全局变量中，后续用例可能用到全局变量的值
    load_context_from_yaml(suite_folder)
    file_names= [(int(f.split("_")[0]), f) for f in os.listdir(suite_folder)
                 if f.endswith('.yaml') and f.split("_")[0].isdigit()]
    # print("符合规则的文件读取出来",file_names)
    file_names.sort()#排序
    file_names=[f[-1] for f in file_names]
    print("排序后的文件列表",file_names)
    # 读取符合规则的文件数据
    for file_name in file_names:
        file_path=os.path.join(suite_folder, file_name)
        with open(file_path, 'r', encoding='utf-8')as file:
            caseinfo=yaml.full_load(file)
            yaml_caseInfos.append(caseinfo)
    return yaml_caseInfos



if __name__ == '__main__':
    # ./当前目录  ../上一级目录  ../../上上级目录  /n /t  r防止转义
    # data=readYaml(r'../../examples/api-cases-yaml/1_login.yaml')
    # print('返回结果',data)
    #
    # load_context_from_yaml(r'/examples\api-cases-yaml')
    c = load_yaml_files(r'F:\request\examples\api-cases-yaml')
    print("符合规则的yaml数据",c)

