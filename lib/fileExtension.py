# -*- coding: utf-8 -*-

class fileData:
    # 从文件取出数据，转成数组
    def fileToList(self,text):
        lines = open(text, 'r').readlines()
        res = []
        for i in lines:
            new = i.replace('\n','')
            res.append(new)
        return res

    #将列表进行分割
    def divList(self,ls, n):
        if not isinstance(ls, list) or not isinstance(n, int):
            return []
        ls_len = len(ls)
        if n <= 0 or 0 == ls_len:
            return []
        if n > ls_len:
            return []
        elif n == ls_len:
            return [[i] for i in ls]
        else:
            j = ls_len / n
            k = ls_len % n
            ls_return = []
            for i in xrange(0, (n - 1) * j, j):
                ls_return.append(ls[i:i + j])
            ls_return.append(ls[(n - 1) * j:]) # 算上末尾的j+k
            return ls_return