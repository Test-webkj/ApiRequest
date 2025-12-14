import jsonpath
import requests
from api参数 import *
session = requests.session()
url = 'http://shop-xo.hctestedu.com/index.php?s=/api/user/login&application=app&application_client_type=weixin'
res = session.post(url,json=data)
print('返回结果',res.json())
exmsg = '登录成功'
sjmsg = jsonpath.jsonpath(res.json(),'$.msg')
print('实际结果',sjmsg[0])
assert exmsg == sjmsg[0],'断言失败'
token = jsonpath.jsonpath(res.json(),'$.data.token')[0]
print('token',token)

#加入购物车
url = f'http://shop-xo.hctestedu.com/index.php?s=api/cart/save&application=app&application_client_type=weixin&token={token}'
data = {"goods_id":"2","stock":"1"}
res = session.post(url,json=data)
print('返回结果',res.json())
exmsg = '加入成功'
sjmsg = jsonpath.jsonpath(res.json(),'$.msg')
assert exmsg == sjmsg[0],'加入购物车断言失败'

#查看购物车
url = f'http://shop-xo.hctestedu.com/index.php?s=api/cart/index&application=app&application_client_type=weixin&token={token}'
res = session.get(url)
print('查看购物车：',res.json())
isd_id = jsonpath.jsonpath(res.json(),'$.data.data[0].id')[0]
print('购物车id',isd_id)

#查看地址
url = f'http://shop-xo.hctestedu.com/index.php?s=api/useraddress/index&application=app&application_client_type=weixin&token={token}'
res = session.post(url)
print('查看地址：',res.json())
dzid = jsonpath.jsonpath(res.json(),'$.data.data[0].id')[0]
print('地址id',dzid)

#新增订单
url = f'http://shop-xo.hctestedu.com/index.php?s=/api/buy/add&application=app&application_client_type=weixin&token={token}'
data = {
    "buy_type":"cart",
    "ids":isd_id,
    "stock":"1",
    "spec":[],
    "address_id":dzid,
    "payment_id":"3"
}
res = session.post(url,json=data)
print('新增订单返回结果：',res.json())
exmsg = "提交成功"
sjmsg = jsonpath.jsonpath(res.json(),'$.msg')
assert exmsg == sjmsg[0],'断言失败'
