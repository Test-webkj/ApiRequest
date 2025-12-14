# test_yaml.py
import yaml

yaml_path = r'F:\request\HAT\examples\api-cases-yaml\login.yaml'
try:
    with open(yaml_path, encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    print("✅ 解析成功！")
    print("数据类型：", type(data))  # 必须是list
    print("用例数：", len(data))     # 输出1
except Exception as e:
    print("❌ 解析失败：", e)