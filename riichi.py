# -*- coding:utf-8 -*-

import json, sys
from datetime import datetime
from workflow import Workflow3, web

from utils import strSlicedNumber, strSlicedAlpha

reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

filename = "./score.json"
typeInError = '请按照\"X符Y番\"、\"X符 Y番\"或者\"X Y\"的格式输入...'


class CustomError(Exception):
    def __init__(self, ErrorInfo):
        super(CustomError, self).__init__(self) #初始化父类
        self.errorinfo=ErrorInfo
    def __str__(self):
        return self.errorinfo

def verifyFlag(cmd, indicator):
    number = strSlicedNumber(cmd)
    flag = cmd[len(number):]
    
    if not flag == '':
        if indicator == 'fu':
            if flag == 'fu' or flag == '符':
                # print "verify fu passed" 
                return True
            else:
                # print "verify fu fail" 
                return False
        elif indicator == 'fan':
            if flag == 'fan' or flag == '番':
                # print "verify fan passed" 
                return True
            else:
                # print "verify fan fail" 
                return False
    else:
        return True

def parseArgs(args, jsonDict):
    if len(args) == 2: ## 20fu 3fan
        fu = strSlicedNumber(args[0])
        fan = strSlicedNumber(args[1])
        verfiyfu = verifyFlag(args[0].lower(), 'fu')
        verfiyfan = verifyFlag(args[1].lower(), 'fan')

    elif len(args) == 1: ## 20fu3fan
        cmd = args[0]
        if len(cmd) < 5:
            raise CustomError(typeInError)
        fu = strSlicedNumber(cmd)
        cut = cmd[len(fu):]
        fu_flag = strSlicedAlpha(cut)
        cut2 = cut[len(fu_flag):]
        fan = strSlicedNumber(cut2)
        fan_flag = cut2[len(fan):]
        verfiyfu = verifyFlag(fu+fu_flag.lower(), 'fu')
        verfiyfan = verifyFlag(fan+fan_flag.lower(), 'fan')

    else:
        raise CustomError(typeInError)

    if verfiyfu == False or verfiyfan == False:
        raise CustomError(typeInError)
    if fu not in jsonDict.get('oya').keys():
        raise CustomError('符数输入不正确，请重新输入...')
    if not fan.isdigit() or int(fan) == 0:
        raise CustomError('翻数输入不正确，请重新输入...')
    else:
        if int(fan) > 13:
            fan = '13'
        return [jsonDict.get('oya').get(fu).get(fan), jsonDict.get('kotomo').get(fu).get(fan)]

def main(wf):
    with open("./score.json",'r') as load_f:
        responseJson = json.load(load_f)
        try:
            results = parseArgs(wf.args, responseJson)
        except CustomError as e:
            # print str(e)
            wf.add_item(title=str(e),icon='./icons/icon.png')
        else:
            for n in xrange(0, len(results)):
                if len(results[n]) == 3:
                    if n == 0:
                        output = '食和：{}； 自摸：{}ALL'.format(results[n][1], results[n][2])
                        clipboard = '亲家，{} => 食和：{}； 自摸：{}ALL'.format(results[n][0], results[n][1], results[n][2])
                        wf.add_item(title=output, subtitle=results[n][0], arg=clipboard, valid=True, icon='./icons/qin.png')
                    else:
                        #     wf.add_item(title='食和：{}； 自摸：{}'.format(results[n][1], results[n][2]), subtitle=results[n][0], valid=True, icon='./icons/zi.png')
                        # else:
                        output = '食和：{}； 自摸：{}/{}'.format(results[n][1], results[n][2].split(", ", 1)[0], results[n][2].split(", ", 1)[1])
                        clipboard = '子家，{} => 食和：{}； 自摸：{}/{}'.format(results[n][0], results[n][1], results[n][2].split(", ", 1)[0], results[n][2].split(", ", 1)[1])
                        wf.add_item(title=output, subtitle=results[n][0], arg=clipboard, valid=True, icon='./icons/zi.png')
                elif len(results[n]) == 2:
                    if n == 0:
                        if results[n][1] == '-':
                            output = '食和：{}； 自摸：{}'.format(results[n][0], results[n][1])
                            clipboard = '亲家，' + output
                            wf.add_item(title=output, arg=clipboard, valid=True, icon='./icons/qin.png')
                        else:
                            output = '食和：{}； 自摸：{}ALL'.format(results[n][0], results[n][1])
                            clipboard = '亲家，' + output
                            wf.add_item(title=output, arg=clipboard, valid=True, icon='./icons/qin.png')
                    else:
                        if results[n][1] == '-':
                            output = '食和：{}； 自摸：{}'.format(results[n][0], results[n][1])
                            clipboard = '子家，' + output
                            wf.add_item(title=output, arg=clipboard, valid=True, icon='./icons/zi.png')
                        else:
                            output = '食和：{}； 自摸：{}/{}'.format(results[n][0], results[n][1].split(", ", 1)[0], results[n][1].split(", ", 1)[1])
                            clipboard = '子家，' + output
                            wf.add_item(title=output, arg=clipboard, valid=True, icon='./icons/zi.png')

        wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))