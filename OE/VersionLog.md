###2018-08-3 更新日志
* 更新了使用了requests模块，可以自定义扩展成get,post,put,delete,head,options等方法，同时支持上传图片
* 更新脱离excel来管理测试用例，使用html生成xml接口文件后，给python来解析.

###201xxxxxx 更新日志
* 修复了支持指定测试接口测试id

###201xxxxxx 更新日志
* 优化在html线生成xml接口，只要填入接口名字，参数，方法，自定义函数就可以了


###201xxxxxx 更新日志
* 去掉自动化函数，节省大量代码，只需在接口xml生成器上指定预期结果就可以了

###201xxxxxx 更新日志
* 更新了预期结果偶尔无法检测成功的bug
* 更新了需要登陆后的id或者token联合使用接口

###201xxxxxx 更新日志
* 优化了检查点。如果实际结果包含了嵌套层，检查点只要检查实际结果中嵌套层的第一个对象。如:data[{"a":b},{"a":"c"}].只要检查{"a":"b"}
 * 一级检查点和二级检查点（嵌套层，只是检查key是否存在）
 * 二级检查主要用的是list set差集的方式 
* 更新了html接口生成器

* 生成器代码参考：https://github.com/284772894/SaveXML

### 201xxxxxx

* 代码简单优化了下
* 主要更新了对比规则,第一层对比code的状态，第二层全字段对比，之前想复杂了

```
def compare(exJson,factJson):
    if factJson["appStatus"]["errorCode"] == 0:
       return exJson==factJson
    else:
        print("接口请求失败")
        return False
```


### 201xxxxxx 更新日志
* 修改对比规则，如果有嵌套层，首页对比第一层的code,然后对比其他嵌套层的value，不进行其他嵌套层的全字段匹配

```
def compare(exJson,factJson,isList=0):
    isFlag = True
    if exJson.get("appStatus") == factJson.get("appStatus"):
        if isList== False: # 如果没有嵌套层
            return isFlag
        data2 = exJson.get("content")
        data3 = factJson.get("content")
        for item2 in data2:
            for item3 in data3:
                keys2 = item2.keys()
                keys3 = item3.keys()
                if keys2 == keys3: # 如果嵌套层的key完全相等
                     for key in keys2:
                        value2 = item2.get(key)
                        value3 = item3.get(key)
                        if type(value3)==type(value2):# 对比嵌套层的value的type值
                           pass
                        else:
                            isFlag = False
                            break
                else:
                    isFlag = False
                    break
    else:
        isFlag = False
    print(isFlag)
    return isFlag
```

### 201xxxxxx 更新日志

* 测试报告改用控制excel的显示方式 

![test_mark.png](test_mark.png "test_mark.png")

![test_detail.png](test_detail.png "test_detail.png")

### 201xxxxxx 更新日志

* 测试报告以发送邮件的方式通知