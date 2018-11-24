import base64


def search_head_sculpture(phone):
    """
    传入一个手机号，返回此手机号的用户的头像base64
    :param phone: 要查询的用户手机号
    :return: 返回此手机号的用户的头像base64
    """
    # 二进制方式打开图文件(图片是根据头像的路径+好友手机号+.png)
    file_path = "upload/image/head_sculpture/%s.png" % phone
    f = open(file_path, 'rb')  # 拼接：路径+手机号+.png然后打开文件
    head_sculpture_base64 = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    f.close()
    return head_sculpture_base64
