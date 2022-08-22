import socketserver
import copy
import requests
import json

class WECHAT_HTTP_APIS:
    # login check
    WECHAT_IS_LOGIN = 0                         # 登录检查

    # self info
    WECHAT_GET_SELF_INFO = 1                    # 获取个人信息

    # send message
    WECHAT_MSG_SEND_TEXT = 2                    # 发送文本
    WECHAT_MSG_SEND_AT = 3                      # 发送群艾特
    WECHAT_MSG_SEND_CARD = 4                    # 分享好友名片
    WECHAT_MSG_SEND_IMAGE = 5                   # 发送图片
    WECHAT_MSG_SEND_FILE = 6                    # 发送文件
    WECHAT_MSG_SEND_ARTICLE = 7                 # 发送xml文章
    WECHAT_MSG_SEND_APP = 8                     # 发送小程序

    # receive message
    WECHAT_MSG_START_HOOK = 9                   # 开启接收消息HOOK，只支持socket监听
    WECHAT_MSG_STOP_HOOK = 10                   # 关闭接收消息HOOK
    WECHAT_MSG_START_IMAGE_HOOK = 11            # 开启图片消息HOOK
    WECHAT_MSG_STOP_IMAGE_HOOK = 12             # 关闭图片消息HOOK
    WECHAT_MSG_START_VOICE_HOOK = 13            # 开启语音消息HOOK
    WECHAT_MSG_STOP_VOICE_HOOK = 14             # 关闭语音消息HOOK

    # contact
    WECHAT_CONTACT_GET_LIST = 15                # 获取联系人列表
    WECHAT_CONTACT_CHECK_STATUS = 16            # 检查是否被好友删除
    WECHAT_CONTACT_DEL = 17                     # 删除好友
    WECHAT_CONTACT_SEARCH_BY_CACHE = 18         # 从内存中获取好友信息
    WECHAT_CONTACT_SEARCH_BY_NET = 19           # 网络搜索用户信息
    WECHAT_CONTACT_ADD_BY_WXID = 20             # wxid加好友
    WECHAT_CONTACT_ADD_BY_V3 = 21               # v3数据加好友
    WECHAT_CONTACT_ADD_BY_PUBLIC_ID = 22        # 关注公众号
    WECHAT_CONTACT_VERIFY_APPLY = 23            # 通过好友请求
    WECHAT_CONTACT_EDIT_REMARK = 24             # 修改备注

    # chatroom
    WECHAT_CHATROOM_GET_MEMBER_LIST = 25        # 获取群成员列表
    WECHAT_CHATROOM_GET_MEMBER_NICKNAME = 26    # 获取指定群成员昵称
    WECHAT_CHATROOM_DEL_MEMBER = 27             # 删除群成员
    WECHAT_CHATROOM_ADD_MEMBER = 28             # 添加群成员
    WECHAT_CHATROOM_SET_ANNOUNCEMENT = 29       # 设置群公告
    WECHAT_CHATROOM_SET_CHATROOM_NAME = 30      # 设置群聊名称
    WECHAT_CHATROOM_SET_SELF_NICKNAME = 31      # 设置群内个人昵称

    # database
    WECHAT_DATABASE_GET_HANDLES = 32            # 获取数据库句柄
    WECHAT_DATABASE_BACKUP = 33                 # 备份数据库
    WECHAT_DATABASE_QUERY = 34                  # 数据库查询

    # version
    WECHAT_SET_VERSION = 35                     # 修改微信版本号

    # log
    WECHAT_LOG_START_HOOK = 36                  # 开启日志信息HOOK
    WECHAT_LOG_STOP_HOOK = 37                   # 关闭日志信息HOOK

APIS = WECHAT_HTTP_APIS

class WECHAT_HTTP_API_PARAM_TEMPLATES:
    __HTTP_API_PARAM_TEMPLATE = {
        # login check
        APIS.WECHAT_IS_LOGIN: {},


        # self info
        APIS.WECHAT_GET_SELF_INFO: {},


        # send message
        APIS.WECHAT_MSG_SEND_TEXT: {"wxid": "",
                                    "msg": ""},
        # wxids需要以`,`分隔，例如`wxid1,wxid2,wxid3`
        APIS.WECHAT_MSG_SEND_AT: {"chatroom_id":"",
                                  "wxids": "",
                                  "msg": "",
                                  "auto_nickname": 1},
        APIS.WECHAT_MSG_SEND_CARD: {"receiver":"",
                                    "shared_wxid":"",
                                    "nickname":""},
        APIS.WECHAT_MSG_SEND_IMAGE: {"receiver":"",
                                     "img_path":""},
        APIS.WECHAT_MSG_SEND_FILE: {"receiver":"",
                                    "file_path":""},
        APIS.WECHAT_MSG_SEND_ARTICLE: {"wxid":"",
                                       "title":"",
                                       "abstract":"",
                                       "url":"",
                                       "img_path":""},
        APIS.WECHAT_MSG_SEND_APP: {"wxid":"",
                                   "appid":""},


        # receive message
        APIS.WECHAT_MSG_START_HOOK: {"port": 10808},
        APIS.WECHAT_MSG_STOP_HOOK: {},
        APIS.WECHAT_MSG_START_IMAGE_HOOK: {"save_path":""},
        APIS.WECHAT_MSG_STOP_IMAGE_HOOK: {},
        APIS.WECHAT_MSG_START_VOICE_HOOK: {"save_path":""},
        APIS.WECHAT_MSG_STOP_VOICE_HOOK: {},


        # contact
        APIS.WECHAT_CONTACT_GET_LIST: {},
        APIS.WECHAT_CONTACT_CHECK_STATUS: {"wxid":""},
        APIS.WECHAT_CONTACT_DEL: {"wxid":""},
        APIS.WECHAT_CONTACT_SEARCH_BY_CACHE: {"wxid":""},
        APIS.WECHAT_CONTACT_SEARCH_BY_NET: {"keyword":""},
        APIS.WECHAT_CONTACT_ADD_BY_WXID: {"wxid":"",
                                          "msg":""},
        APIS.WECHAT_CONTACT_ADD_BY_V3: {"v3":"",
                                        "msg":"",
                                        "add_type": 0x6},
        APIS.WECHAT_CONTACT_ADD_BY_PUBLIC_ID: {"public_id":""},
        APIS.WECHAT_CONTACT_VERIFY_APPLY: {"v3":"",
                                           "v4":""},
        APIS.WECHAT_CONTACT_EDIT_REMARK: {"wxid":"",
                                          "remark":""},


        # chatroom
        APIS.WECHAT_CHATROOM_GET_MEMBER_LIST: {"chatroom_id":""},
        APIS.WECHAT_CHATROOM_GET_MEMBER_NICKNAME: {"chatroom_id":"",
                                                   "wxid":""},
        # wxids需要以`,`分隔，例如`wxid1,wxid2,wxid3`
        APIS.WECHAT_CHATROOM_DEL_MEMBER: {"chatroom_id":"",
                                          "wxids":""},
        # wxids需要以`,`分隔，例如`wxid1,wxid2,wxid3`
        APIS.WECHAT_CHATROOM_ADD_MEMBER: {"chatroom_id":"",
                                          "wxids":""},
        APIS.WECHAT_CHATROOM_SET_ANNOUNCEMENT: {"chatroom_id":"",
                                                "announcement":""},
        APIS.WECHAT_CHATROOM_SET_CHATROOM_NAME: {"chatroom_id":"",
                                                 "chatroom_name":""},
        APIS.WECHAT_CHATROOM_SET_SELF_NICKNAME: {"chatroom_id":"",
                                                 "nickname":""},


        # database
        APIS.WECHAT_DATABASE_GET_HANDLES: {},
        APIS.WECHAT_DATABASE_BACKUP: {"db_handle":0,
                                      "save_path":""},
        APIS.WECHAT_DATABASE_QUERY: {"db_handle":0,
                                     "sql":""},


        # version
        APIS.WECHAT_SET_VERSION: {"version": "3.7.0.30"},


        # log
        APIS.WECHAT_LOG_START_HOOK: {},
        APIS.WECHAT_LOG_STOP_HOOK: {},
    }

    def get_http_template(self, api_number):
        try:
            return copy.deepcopy(self.__HTTP_API_PARAM_TEMPLATE[api_number])
        except KeyError:
            raise ValueError("There is no interface numbered %s." % api_number)

get_http_template = WECHAT_HTTP_API_PARAM_TEMPLATES().get_http_template

class ReceiveMsgSocketServer(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self):
        conn = self.request
        while True:
            try:
                ptr_data = conn.recv(1024)
                print(ptr_data.decode())
                # try:
                #     if ptr_data.decode() == 'bye': break
                # except UnicodeDecodeError:
                #     pass
                # while len(ptr_data) < ctypes.sizeof(self.ReceiveMsgStruct):
                #     data = conn.recv(1024)
                #     if len(data) == 0: break
                #     ptr_data += data
                # if ptr_data:
                #     ptr_receive_msg = ctypes.cast(ptr_data, ctypes.POINTER(self.ReceiveMsgStruct))
                #     ReceiveMsgSocketServer.msg_callback(ptr_receive_msg.contents)
            except OSError:
                break
            except:
                pass
            conn.sendall("200 OK".encode())
        conn.close()

    @staticmethod
    def msg_callback(data):
        msg = {'pid': data.pid, 'time': data.time, 'type': data.type,
               'isSendMsg': data.isSendMsg, 'msgid': data.msgid,
               'wxid': data.wxid,'message': data.message,
               'sendto' if data.isSendMsg else 'from': data.sender}
        # TODO: 在这里写额外的消息处理逻辑

        print(msg)

def post_wechat_http_api(api,port,data = {}):
    url = "http://127.0.0.1:{}/api/?type={}".format(port,api)
    resp = requests.post(url = url,data = json.dumps(data))
    return resp.json()

def get_wechat_http_api(api,port,data = {}):
    url = "http://127.0.0.1:{}/api/?type={}".format(port,api)
    resp = requests.get(url = url,params = data)
    return resp.json()


test_port = 18888

print(post_wechat_http_api(APIS.WECHAT_IS_LOGIN,port = 18888)["is_login"])
