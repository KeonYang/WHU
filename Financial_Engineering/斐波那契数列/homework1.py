# Subject: Financial Engineering

# Time: 11/9/2018
# Author: 杨宸宇 2016301550186

def fa(i, data=[]):
    '''
    :param i: 需要数列的项数
    :param data: 存储数列的列表
    :return: data，是一个i项的斐波那契数列
    '''
    if i == 1:  # 如果只要一项则只是1
        data.append(1)
    elif i == 2:  # 如果需要2项则是1，1
        data.extend([1, 1])
    else:
        # 需要的项多于2项，则开始正式的进行递归
        data.extend([1, 1])
        # 从第三项开始，每一项是前两项的和，不断递归
        for i in range(2, i):
            # 不断增加新的项进入数列，直到i位置
            data.append(data[i - 1] + data[i - 2])
a = []
# 在console里面进行尝试运行
fa(10, data=a)
print(a)
