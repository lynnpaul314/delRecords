#-*- coding: UTF-8 -*-
import argparse
import os
import re

class Records():
    #初始化传递文件,num的值
    def __init__(self, dirpath, pathRe, num):
        self.dirpath = dirpath
        self.pathRe = pathRe
        self.num = num
        # self.plists = []

    #打开文件records.txt
    def openRe(self):
        with open(self.pathRe, 'r', encoding='utf-8') as f:
            self.data = f.read()
            return self.data

    #获取当前安装包记录列表
    def getRecodes(self):
        self.recodes = self.data.split('==========\n')
        return self.recodes

    #获得保留的列表记录数据，根据num值确认保留num条数据
    def getSave_Recodes(self):
        # self.save_codes = self.data.split('==========\n')
        self.save_codes = self.recodes[-self.num:]
        print('保留的安装包记录为：')
        print(self.save_codes)
        return self.save_codes

    #解析获得需要删除安装包的记录
    def getRemove_Recodes(self):
        # self.remove_codes = self.data.split('==========\n')
        count = len(self.recodes) - self.num
        if count > 0:
            self.remove_codes = self.recodes[:count]
            print('删除的安装包记录为：')
            print(self.remove_codes)
        else:
            self.remove_codes = []
            print('没有可以删除的安装包记录')
        return self.remove_codes

    #删除安装包
    def removePlist(self):
        for remove_code in self.remove_codes:
            plist = re.search(r'HealthTaiZhou_(.*?)plist', remove_code).group()
            print('安装包 %s 将被删除：' % plist)
            remove_path = f'{self.dirpath}{plist}'
            if os.path.exists(remove_path):
                # print(remove_path)
                os.remove(remove_path)
            else:
                print('需要删除的安装包没有找到')

        #     self.plists.append(plist)
        # print(self.plists)
        # return self.plists


    #保存列表记录
    def saveRecodes(self):
        with open(self.pathRe, 'w', encoding='utf-8') as f:
            count = 1
            for recode in self.save_codes:
                # 处理首行回车符
                # if recode.find('\n', 0, 4) == 0:
                #     recode = recode.replace('\n', '', 1)
                #     # print(recode)
                #数据末尾添加分隔符
                if count != len(self.save_codes):
                    recode = recode + '==========' + '\n'
                else:
                    recode = recode
                count += 1
                f.writelines(recode)
            print('\n' + '安装包记录清除完毕......')

# 获取当前脚本路劲
def getWay():
    myway = os.getcwd()
    # print(myway)
    return myway

#命令行获得保留记录参数
def getNum():
    parser = argparse.ArgumentParser(description='清除安装包列表记录脚本')
    #命令行输入保留安装包记录的num值
    parser.add_argument('-n', '--num', type=int, default=3, help='请输入保留记录数：')
    #命令行输入recodes所在文件夹名
    parser.add_argument('-f', '--filename', default='HealthTaiZhou', help='获取recodes所在文件夹名')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = getNum()
    #pathRe = f'{os.path.dirname(__file__)}/html/{args.filename}/records.txt'
    dirPath = f'{getWay()}/html/{args.filename}/'
    # print(dirPath)
    pathRe = f'{dirPath}records.txt'
    # print(pathRe)
    rec = Records(dirPath, pathRe, args.num)
    rec.openRe()
    rec.getRecodes()

    #删除安装包
    rec.getRemove_Recodes()
    rec.removePlist()
    #保存安装包记录
    rec.getSave_Recodes()
    rec.saveRecodes()


