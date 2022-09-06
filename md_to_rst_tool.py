# -*- coding:utf8 -*-
# auther; 18793
# Date：2019/12/5 17:14
# filename: md_to_rst_tool.py
import os
import subprocess
import json
import hashlib
import time

"""
Script to convert markdown file to rst file format
"""
Search_Path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + "/source"


def log():
    def Out_Wrapper(func):
        
        def Internal(*args, **kwargs):
            start_time = time.time()
            func(*args, **kwargs)
            end_time = time.time()
            print("-----------------------------------------------------")
            print("运行时间:%s " % (end_time - start_time))
            print("-----------------------------------------------------")

        return Internal
    return Out_Wrapper


class Conversion:
    """
    文件格式转换类
    """

    def __init__(self):
        self.__js_file = "file_md5.json"

    def get_jsonfile(self):
        return self.__js_file

    def write_json(self, file, data):
        '''
        :param file: json文件名称
        :param data: 写入数据
        :return:
        '''
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def exec_cmd(self, cmd):
        """
        Execute arbitrary commands as sub-processes.
        """
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True,
                                shell=True)
        stdout, stderr = proc.communicate()
        return (proc.returncode, stdout, stderr)

    def trav_walk(self, pathname):
        """
        遍历pathname目录后，创建一个key-value的字典，key：md结尾的文件名，value：md5值
        :param pathname: 要遍历的目录
        :return:
        """
        d_file_info = {}
        for root, dirs, files in os.walk(pathname):
            for file in files:
                file = os.path.abspath(os.path.join(root, file))
                if file.endswith(".md"):
                    with open(file, 'rb') as f:
                        sha1obj = hashlib.sha1()
                        sha1obj.update(f.read())
                        hash = sha1obj.hexdigest()
                        d_file_info[file] = hash
        return d_file_info

    def Traversing_files(self, file):
        """
        将遍历后的字典写入到file文件中。 file是用于检测是否有文件修改的一个标本文件
        :param file: 巡检标本文件
        :return: 返回遍历后的字典
        """
        file_info = self.trav_walk(Search_Path)
        if not os.path.exists(file):
            self.write_json(file, file_info)
        else:
            return file_info

    @log()
    def Match_file(self):
        """
        读取md5文件，遍历文件后与md5中的文件进行比较，存在修改就进行转换
        :return:
        """
        # 开始遍历目录生成dict
        file_name = self.trav_walk(Search_Path)
        # 开始读文件
        f = open(self.get_jsonfile(), "r", encoding="utf-8")
        json_info = json.load(f)
        for name, md5_value in file_name.items():
            if name not in json_info.keys() or md5_value != json_info[name]:
                print("检测到{}文件change...已记录到{}中....".format(name, self.get_jsonfile()))
                rst_file_name = name.replace(".md", ".rst")
                result = self.exec_cmd(
                    "pandoc -s -t rst --toc {} -o {}".format(str(name).replace(" ", "").strip(), rst_file_name))
                print(("pandoc -s -t rst --toc {} -o {} ok!".format(name, rst_file_name)))
                if result[0] != 0:
                    return

        # 将更新后的数据重新写入文件，md5也更新到文件中
        self.write_json(self.get_jsonfile(), file_name)


if __name__ == '__main__':
    Com = Conversion()
    Com.Traversing_files(Com.get_jsonfile())
    Com.Match_file()
