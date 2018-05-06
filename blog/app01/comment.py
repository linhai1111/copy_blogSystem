
# # 列表的特性：引用数据类型，共用内存地址，
# data = [
#     [11,33,44],
#     [77,88,99]
# ]
# data[0].append(data[1]) # 将data[1]的内存地址添加到data[0]中，data[0]中的data[1]与原来的data[1]共用一份内存地址
# print(data)     # [[11, 33, 44, [77, 88, 99]], [77, 88, 99]]
# data[1].append(00)  # 往data[1]中添加数据00时，data[0]中的data[1]的数据也会同步更新
# print(data)     # [[11, 33, 44, [77, 88, 99, 0]], [77, 88, 99, 0]]

########################################################
msg_list = [
    {'id':1,'content':'xxx','parent_id':None},
    {'id':2,'content':'xxx','parent_id':None},
    {'id':3,'content':'xxx','parent_id':None},
    {'id':4,'content':'xxx','parent_id':1},
    {'id':5,'content':'xxx','parent_id':4},
    {'id':6,'content':'xxx','parent_id':2},
    {'id':7,'content':'xxx','parent_id':5},
    {'id':8,'content':'xxx','parent_id':3},
]

# 一、将字典列表格式重新组装成字典格式，key为字典中的id号，两者中的值对应同一内存地址;
msg_list_dic={
}
for item in msg_list:
    item ['child'] = []     # 先给msg_list列表添加child空的k,v值：child:[]，为后续根据parent_id添加到对应id字典中做准备
    # print(msg_list)     # [{'id': 1, 'content': 'xxx', 'parent_id': None, 'child': []},……],
    # 也可写成列表生成式：v=[ row.setdefault('child',[]) for row in msg_list]

    msg_list_dic[item['id']] = item  # 将列表转换为字典，key为msg_list列表中的id号，value为msg_list列表中的字典，msg_list_dic中的value值与msg_list中保存的字典列表两者共用同一内存地址
    # print(msg_list_dic)    # {1: {'id': 1, 'content': 'xxx', 'parent_id': None, 'child': []}, 2:{}……},
    # 补充：字典查询速度比列表快，字典有hash索引，通过算法快速定位内存地址进行查询

# 二、 根据msg_list中parent_id的值找到对应的字典中的key，将该条数据添加至有索引的字典中,完成最后组装
result =[]  # 用来保存parent_id为Nnoe时的前3条数据：
for item in msg_list:
    pid = item['parent_id']     # 获得每条字典中parent_id的值
    if pid:
        msg_list_dic[pid]['child'].append(item)     # 根据parent_id的索引号，从msg_list列表中取出对应的数据向msg_list_dic字典中的child中添加
    else:
        result.append(item)     # 该item中的数据中，parent_id为Nnoe,result就是最后结果
print(result)
"""
[
{'id': 1, 'content': 'xxx', 'parent_id': None, 'child': [{'id': 4, 'content': 'xxx', 'parent_id': 1, 'child': [{'id': 5, 'content': 'xxx', 'parent_id': 4, 'child': [{'id': 7, 'content': 'xxx', 'parent_id': 5, 'child': []}]}]}]}, 
{'id': 2, 'content': 'xxx', 'parent_id': None, 'child': [{'id': 6, 'content': 'xxx', 'parent_id': 2, 'child': []}]}, 
{'id': 3, 'content': 'xxx', 'parent_id': None, 'child': [{'id': 8, 'content': 'xxx', 'parent_id': 3, 'child': []}]}
]
"""
print(msg_list)
"""
[
{'id': 1, 'content': 'xxx', 'parent_id': None, 'child': [{'id': 4, 'content': 'xxx', 'parent_id': 1, 'child': [{'id': 5, 'content': 'xxx', 'parent_id': 4, 'child': [{'id': 7, 'content': 'xxx', 'parent_id': 5, 'child': []}]}]}]}, 
{'id': 2, 'content': 'xxx', 'parent_id': None, 'child': [{'id': 6, 'content': 'xxx', 'parent_id': 2, 'child': []}]}, 
{'id': 3, 'content': 'xxx', 'parent_id': None, 'child': [{'id': 8, 'content': 'xxx', 'parent_id': 3, 'child': []}]}, 
{'id': 4, 'content': 'xxx', 'parent_id': 1, 'child': [{'id': 5, 'content': 'xxx', 'parent_id': 4, 'child': [{'id': 7, 'content': 'xxx', 'parent_id': 5, 'child': []}]}]}, 
{'id': 5, 'content': 'xxx', 'parent_id': 4, 'child': [{'id': 7, 'content': 'xxx', 'parent_id': 5, 'child': []}]},
{'id': 6, 'content': 'xxx', 'parent_id': 2, 'child': []},
{'id': 7, 'content': 'xxx', 'parent_id': 5, 'child': []}, 
{'id': 8, 'content': 'xxx', 'parent_id': 3, 'child': []}
]
"""

print(msg_list_dic)
"""
{
1: {'id': 1, 'content': 'xxx', 'parent_id': None, 'child': [{'id': 4, 'content': 'xxx', 'parent_id': 1, 'child': [{'id': 5, 'content': 'xxx', 'parent_id': 4, 'child': [{'id': 7, 'content': 'xxx', 'parent_id': 5, 'child': []}]}]}]}, 
2: {'id': 2, 'content': 'xxx', 'parent_id': None, 'child': [{'id': 6, 'content': 'xxx', 'parent_id': 2, 'child': []}]}, 
3: {'id': 3, 'content': 'xxx', 'parent_id': None, 'child': [{'id': 8, 'content': 'xxx', 'parent_id': 3, 'child': []}]}, 
4: {'id': 4, 'content': 'xxx', 'parent_id': 1, 'child': [{'id': 5, 'content': 'xxx', 'parent_id': 4, 'child': [{'id': 7, 'content': 'xxx', 'parent_id': 5, 'child': []}]}]},
5: {'id': 5, 'content': 'xxx', 'parent_id': 4, 'child': [{'id': 7, 'content': 'xxx', 'parent_id': 5, 'child': []}]}, 
6: {'id': 6, 'content': 'xxx', 'parent_id': 2, 'child': []}, 
7: {'id': 7, 'content': 'xxx', 'parent_id': 5, 'child': []},
8: {'id': 8, 'content': 'xxx', 'parent_id': 3, 'child': []}
}
"""


















