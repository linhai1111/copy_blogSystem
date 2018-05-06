"""
多级评论生成组件
"""
def comment(msg_list):
    """
    :param comment_list: 传入的参数格式为字典列表
    :return:
    """
    # 数据格式重新组装
    msg_list_dic = { }
    for item in msg_list:
        item['child'] = []  # 先给msg_list列表添加child空的k,v值：child:[]，为后续根据parent_id添加到对应id字典中做准备
        msg_list_dic[item['id']] = item  # 将列表转换为字典，key为msg_list列表中的id号，value为msg_list列表中的字典，msg_list_dic中的value值与msg_list中保存的字典列表两者共用同一内存地址
         # print(msg_list_dic)    # {1: {'id': 1, 'content': 'xxx', 'parent_id': None, 'child': []}, 2:{}……},

    result = []  # 用来保存parent_id为Nnoe时的前3条数据：
    for item in msg_list:
        pid = item['parent_id']  # 获得每条字典中parent_id的值
        if pid:
            msg_list_dic[pid]['child'].append(item)  # 根据parent_id的索引号，从msg_list列表中取出对应的数据向msg_list_dic字典中的child中添加
        else:
            result.append(item)  # 该item中的数据中，parent_id为Nnoe,result就是最后结果
    return result
    """
    result列表中的结果：
    [
    {'id': 1, 'content': 'xxx', 'parent_id': None, 'child': [{'id': 4, 'content': 'xxx', 'parent_id': 1, 'child': [{'id': 5, 'content': 'xxx', 'parent_id': 4, 'child': [{'id': 7, 'content': 'xxx', 'parent_id': 5, 'child': []}]}]}]}, 
    {'id': 2, 'content': 'xxx', 'parent_id': None, 'child': [{'id': 6, 'content': 'xxx', 'parent_id': 2, 'child': []}]}, 
    {'id': 3, 'content': 'xxx', 'parent_id': None, 'child': [{'id': 8, 'content': 'xxx', 'parent_id': 3, 'child': []}]}
    ]
   """

#  组装多级评论表数据
def comment_tree(comment_list):
    commnt_str = '<div class=comment>'  # 组装头部
    for row in comment_list:
        tp1='<div class="content">%s</div>'%(row['content']) # 组装第一级的评论内容
        commnt_str += tp1
        if row['child']:    # 如果有子评论
            child_str = comment_tree(row['child'])    # 递归调用，组装出所有子评论中的内容
            commnt_str += child_str
    commnt_str += '</div>'  # 组装尾部
    return commnt_str