#!/usr/bin/env python3

import base64
import json
from cls.IpAddress import IpAddress
from cls.LocalFile import LocalFile
from cls.StrText import StrText

class SubConvert():

    # allvmess-->json-->name-->v2ray or clash (v2ray --> clash or clash --> v2ray)
        
    # 非标准格式的vmess明文地址转化为标准格式的明文json格式vmess
    def clash_all_to_json(onenode):
        try:
            # print('SubConvert-Line-83-oldnode:' + onenode)
            # V2ray格式
            # onenode = '{name: "211.72.35.110", server: 211.72.35.110, port: 443, type: vmess, uuid: 541ca026-58d3-48f1-d6ef-3a05543ddcb7, alterId: 0, cipher: auto, tls: true, skip-cert-verify: false, network: ws, ws-opts: {path: /, headers: {Host: ru.tzccifq.ga}}, udp: true}'
            # onenode = '{"add":"v.ssr.com", "v":"2", "ps":"\'v.ssr.com\'", "port":"168", "id":"e54a480c-77e3-41ca-8f8b-17ffb50dbd08", "aid":"0", "net":"ws", "type":"", "host":"", "path":"/ssrsub", "tls":"tls"}'
            # onenode = '{add:v1-asw-sg-14.niaoyun.online,port:666,id:b9cc1e88-5db0-37ff-840a-b882345e22d1,aid:1,scy:auto,net:ws,host:v1-asw-sg-14.niaoyun.online,path:/niaocloud,tls:,sni:,v:2,ps:Relay_新加坡-_7234,type:none,serverPort:0,nation:}'
            
            # Clash格式
            #- {alterId: 2,  cipher: auto,  name: '7.y.com',  network: ws,  port: 80,  server: 7.y.com,  tls: false,  type: vmess,  uuid: bac18e70-9964-3f99-805a-d809c4bdc6cb,  path: /ny}
            #- {name: CA-ss1.ssr.com, server: ss1.ssr.com, port: 10443, type: ss, cipher: aes-128-gcm, password: suo.yt.ssr, plugin: obfs, plugin-opts: {mode: tls, host: n46hm52773.wns.windows.com}, udp: true}
            #- {name: US-107.173.157.168, server: 107.173.157.168, port: 443, type: vmess, uuid: 4f6aa0c3-7be1-4eaa-a64c-a23418070422, alterId: 6, cipher: auto, skip-cert-vertify: false, network: ws, path: /b06fde1/, tls: True, headers: {Host: www.shunxin.ml}}
            #- {name: "172.67.196.0", server: 172.67.196.0, port: 443, type: vmess, uuid: 4db99e96-3ee3-419c-b1fb-856975801380, alterId: 64, cipher: auto, tls: true, skip-cert-verify: false, network: ws, ws-opts: {path: /ray, headers: {Host: localhoster.ml}}, udp: true}
            # onenode = '{name: 35.77.5.55, server: 034.ap.pop.bigairport.net, port: 12356, type: vmess, uuid: a6f82e7d-6e99-4a4e-8981-8e91453c13f7, alterId: 1, cipher: auto, skip-cert-vertify: false, network: ws, path: /, tls: True, headers: {Host: t.me/vpnhat}}'
            if(onenode == '' or onenode == '{}'):
                return ''
            if(len(onenode) < 20):
                LocalFile.write_LogFile('SubConvert-Line-42-onenode长度不能小于20, onenode:' + onenode)
                return ''
            nenode = ''            
            # 格式转变，生成标准的json格式字符串，方便后期字典生成
            onenode = onenode.replace(' ', '').replace('"', '').replace('\'', '')
            # 多行链接转换成一行
            onenode = onenode.replace('\r', ',').replace('\n', ',')
            # 去掉标题及广告信息            
            oname = StrText.get_str_btw(onenode, 'name:', ',', 1)
            if(oname != ''):
                onenode = onenode.replace(oname, 'name:,')
            ops = StrText.get_str_btw(onenode, 'ps:', ',', 1)
            if(ops != ''):
                onenode = onenode.replace(ops, 'ps:,')
            # 密码带些值出错
            onenode = onenode.replace('<', '').replace('>', '')
            # 去掉插件的{}和,值
            onenode = onenode.replace('{', ',').replace('}', ',').replace(',,', ',').replace(',,', ',').strip(',')
            
            # 避免,给处理掉，先替换，后还原
            onenode = onenode.replace('h2,http', 'h2=http')
            for i in onenode.split(','):
                if(i.find(':') > -1):
                    a = i.split(':', 1)[0]
                    if(a != ''):
                        b = i.split(':', 1)[1]
                        if(b.find(':') > -1):
                            nenode = nenode + ',"' + a + '":""'
                            nenode = nenode + ',"' + b.split(':')[0] + '":"' + b.split(':')[1] + '"'
                        else:
                            nenode = nenode + ',"' + a + '":"' + b + '"'
                else:
                    print('SubConvert-Line-117-key-and-value:[' + i + ']-onenode:' + onenode)
            nenode = '{' + nenode.strip(',') + '}'
            # 还原带,的值alpn中有两个值
            nenode = nenode.replace('h2=http', 'h2,http')

            # json格式字符串生成字典
            node = json.loads(nenode)
            # 端口为空，直接取消
            if('port' not in node.keys()):
                return ''
            # 处理节点名称为IP地址或域名
            if('add' in node.keys()):
                node['ps'] = node['add']
            elif('server' in node.keys()):
                node['name'] = node['server']
            # 删除不需要的Key
            if('v' in node.keys()):
                del node['v']

            # 字典转换成json格式字符串。
            nenode = json.dumps(node)
            # print('SubConvert-Line-105-nenode:\n' + nenode + '\n')
        except Exception as ex:
            LocalFile.write_LogFile('SubConvert-Line-77-Exception: ' + str(ex) + '\n' + nenode + '\n')
            nenode = ''
        return nenode

    def check_url_v2ray_vmess(onenode):
        try:
            # onenode = '{add:v1-asw-sg-14.niaoyun.online,port:666,id:b9cc1e88-5db0-37ff-840a-b882345e22d1,aid:1,scy:auto,net:ws,host:v1-asw-sg-14.niaoyun.online,path:/niaocloud,tls:,sni:,v:2,ps:Relay_新加坡-_7234,type:none,serverPort:0,nation:}'
            newnode = base64.b64decode(StrText.get_str_base64(onenode[8:])).decode('utf-8')
            if(newnode == '' or newnode == '{}'):
                return ''
            if(len(newnode) < 20):
                LocalFile.write_LogFile('SubConvert-Line-97-onenode长度不能小于20, onenode:' + newnode)
                return ''
            # json格式字符串生成字典
            node = json.loads(newnode)            
            # 添加丢失的非重要字段
            if('add' not in node.keys()):
                LocalFile.write_LogFile('SubConvert-Line-103-add=IP=null, onenode:' + newnode)
                return ''
            else:
                if(node['add'] == ''):
                    LocalFile.write_LogFile('SubConvert-Line-103-add=IP=\'\', onenode:' + newnode)
                    return ''
            # 默认net类型为tcp
            if('net' not in node.keys()):
                node['net'] = 'tcp'
                print('[net] is added.')
            if('ps' not in node.keys()):
                node['ps'] = 'tmpname'
                print('[ps] is added.')
            if('type' not in node.keys()):
                node['type'] = 'none'
                print('[type] is added.')
            if('scy' not in node.keys()):
                node['scy'] = 'auto'
                print('[scy] is added.')
            if('aid' not in node.keys()):
                node['aid'] = '0'
                print('[aid] is added.')
            if('tls' not in node.keys()):
                node['tls'] = 'false'
                LocalFile.write_LogFile('SubConvert-Line-150-Add-TLS-Onenode:\n' + newnode)
                print('[tls] is added.')
            #tls = true or tls 时 可设置 skip-cert-vertify: true
                
            # 端口为空，UUID-id无效（id长度=36）
            if('port' not in node.keys() or len(node['id']) != 36):
                return ''
            # 不管ps是否存在，都替换带广告的标题为add:port
            newname = IpAddress.get_country(node['add']) + '-' + node['add']
            node['ps'] = newname
            # 删除不需要的Key
            if('v' in node.keys()):
                del node['v']
            # 字典转换成json格式字符串。
            newnode = json.dumps(node)
            newnode = "vmess://" + base64.b64encode(newnode.encode('utf-8')).decode('utf-8')
            # print('SubConvert-Line-105-nenode:\n' + nenode + '\n')
        except Exception as ex:
            LocalFile.write_LogFile('SubConvert-Line-116-Exception: ' + str(ex) + '\nonenode:' + onenode + '\n')
            newnode = ''
        return newnode

    # 不同格式的ss转换为标准格式的ss
    def url_ss_to_json(oldonenode):
        try:
            # oldonenode = "ss://YWVzLTI1Ni1nY206WTZSOXBBdHZ4eHptR0M=@167.88.61.119:5000#US%E3%80%90%E4%BB%98%E8%B4%B9%E6%8E%A8%E8%8D%90%EF%BC%9Ahttps%2F%2Fgoo.gs%2Fvip%E3%80%91"
            if (oldonenode.find("#") == -1):
                onenode = oldonenode[5:] + "#0"
            else:
                onenode = oldonenode[5:]

            # onenode = "YWVzLTEyOC1nY206c3VvLnl0L3NzcnN1Yg==@212.102.54.163:10443/?plugin=obfs-123#title"
            # onenode = "YWVzLTI1Ni1nY206bjh3NFN0bmJWRDlkbVhZbjRBanQ4N0VBQDIxMi4xMDIuNTQuMTYzOjMxNTcy#title"
            onenode = onenode.replace("/?", "#")
            jjs = onenode.split("#", 1) # 第二个参数为 1，返回两个参数列表
            onenode = jjs[0]
            if (onenode.find("@") > -1):
                jjs = onenode.split("@", 1) # 第二个参数为 1，返回两个参数列表
                onenode = base64.b64decode(StrText.get_str_base64(jjs[0]).encode('utf-8')).decode('utf-8') + '@' + jjs[1]
            else:
                onenode = base64.b64decode(StrText.get_str_base64(jjs[0]).encode('utf-8')).decode('utf-8')
            #aes-256-gcm:n8w4StnbVD9dmXYn4Ajt87EA@212.102.54.163:31572
            cipher = onenode.split(':')[0]
            port = onenode.rsplit(':', 1)[1]
            server = onenode.rsplit(':', 1)[0].rsplit('@', 1)[1]
            password = StrText.get_str_btw(onenode, cipher + ':', '@' + server, 0)
            name = server + ':' + port

            # 19位以上纯数字或者为空时报错，float64位数字不为string
            if((password.isnumeric() and len(password) > 19) or password == ''):
                return ''
            # 过滤不支持的cipher
            if (cipher == '2022-blake3-aes-128-gcm'):
                return ''
            
            # 字典格式SS信息
            onenode = '{"cipher":"' + cipher + '","password":"' + password + '","server":"' + server + '","port":"' + str(port) + '","name":"' + name + '"}'
            
            node = json.loads(onenode, strict=False)
            # 端口为空，UUID-id无效（id长度=36）
            if('port' not in node.keys()):
                return ''
            # 字典转换成json格式字符串。
            onenode = json.dumps(node)
            return onenode
        except Exception as ex:
            LocalFile.write_LogFile('SubConvert-Line-516-Exception:' + str(ex) + '\nonenode:' + onenode + '\noldonenode:' + oldonenode)
            return ''

    # 不同格式的ss转换为标准格式的ss
    def url_trojan_to_json(j):
        try:
            onenode = ''
            if(j.find('#') == -1):
                j = j + '#'
            newname = j.split("#", 1)[1]
            password = StrText.get_str_btw(j, "trojan://", "@", 0).replace('<', '').replace('>', '')
            server = StrText.get_str_btw(j, "@", ":", 0)
            if (j.find("?") > -1):
                port = StrText.get_str_btw(StrText.get_str_btw(j, "@", "#", 0), ":", "?", 0)
            else:
                port = StrText.get_str_btw(j, "@", "#", 0).split(":", 1)[1]
            if(port.isnumeric() and password != '' and password != 'null'):
                onenode = '{' + '"name": "' + newname + '", "type": "trojan", "server": "' + server + '", "port": "' + str(port) + '", "password": "' + password + '"}'
            else:
                onenode = ''
            node = json.loads(onenode)
            # 端口为空，UUID-id无效（id长度=36）
            if('port' not in node.keys()):
                return ''
            # 字典转换成json格式字符串。
            onenode = json.dumps(node)
            return onenode
        except Exception as ex:
            LocalFile.write_LogFile('SubConvert-Line-516-Exception:' + str(ex) + '\nonenode:' + onenode + '\nj:' + j)
            return ''

    # vless网址转化为标准格式的json
    def url_vless_to_json(onenode):
        try:
            #vless://892ebb75-7055-3007-8d16-356e65c6a49a@45.66.134.219:443?encryption=none&security=tls&sni=45.66.134.219&type=ws&host=45.66.134.219&path=%2fv1t-vless#filename
            if(onenode == ''):
                return '' # 空值忽略
            else:
                print('SubConvert-Line-135-oldnode:' + onenode)
            nenode = '{\n'
            nenode = nenode + '  "name":"tmpname",\n'
            nenode = nenode + '  "uuid":"' + StrText.get_str_btw(onenode, 'vless://', '@', 0) + '",\n'
            nenode = nenode + '  "server":"' + StrText.get_str_btw(onenode, '@', ':', 0) + '",\n'
            nenode = nenode + '  "port":"' + onenode.split('?', 1)[0].rsplit(':', 1)[1] + '",\n'
            onenode = StrText.get_str_btw((onenode + '#'), '?', '#', 0)
            for i in onenode.split('&'):
                if(i.find('=') > -1):
                    a = i.split('=', 1)[0]
                    if(a != ''):
                        b = i.split('=', 1)[1]
                        nenode = nenode + '  "' + a + '":"' + b.strip(' ') + '",\n'
                else:
                    LocalFile.write_LogFile('SubConvert-Line-154-i:' + i + '-onenode:' + onenode + '\n')
            onenode = nenode.strip(',\n') + '\n}'
            # 处理节点名称
            node = json.loads(onenode)
            # 端口为空，UUID-id无效（id长度=36）
            if('port' not in node.keys()):
                return ''
            server = node["server"]
            # node["name"] = IpAddress.get_country(server) + '-' + server
            # 设置IP为名称name的值
            node["name"] = server
            # 字典转换成json格式字符串。
            onenode = json.dumps(node)
            print('SubConvert-Line-157-nenode:\n' + onenode + '\n')
            
            return onenode
        except Exception as ex:
            LocalFile.write_LogFile('SubConvert-Line-162-Exception: ' + str(ex) + '\n' + onenode + '\n')
            return ''
    
    # vmess-clash格式名称转换成v2ray格式名称
    def name_clash_to_v2ray(oldonenode):
        try:
            # 字段转换
            onenode = oldonenode.replace(' ', '')
            if(onenode.find('"uuid":') > -1):
                onenode = onenode.replace('name":', 'ps":')
                onenode = onenode.replace('cipher":', 'scy":')
                onenode = onenode.replace('network":', 'net":')
                onenode = onenode.replace('server":', 'add":')
                onenode = onenode.replace('alterId":', 'aid":')
                onenode = onenode.replace('uuid":', 'id":')
            elif(onenode.find('"id":') == -1):
                LocalFile.write_LogFile('SubConvert-Line-99-onenode: ' + onenode + '\n')
                return ''
            onenode = onenode.replace('"Host":', '"host":')
            onenode = onenode.replace('"HOST":', '"host":')

            # 将标准格式的字符串转换为字典
            node = json.loads(onenode)           
            # 添加丢失的非重要字段
            # 默认net类型为tcp
            if('net' not in node.keys()):
                node['net'] = 'tcp'
                print('[net] is added.')
            if('ps' not in node.keys()):
                node['ps'] = 'tmpname'
                print('[ps] is added.')
            if('type' not in node.keys()):
                node['type'] = 'vmess'
                print('[type] is added.')
            if('scy' not in node.keys()):
                node['scy'] = 'auto'
                print('[scy] is added.')
            if('aid' not in node.keys()):
                node['aid'] = '0'
                print('[aid] is added.')
            if('tls' not in node.keys()):
                node['tls'] = 'false'
                # LocalFile.write_LogFile('SubConvert-Line-294-Add-TLS-Onenode:\n' + oldonenode)
                print('[tls] is added.')
                #tls = true or tls 时 可设置 skip-cert-vertify: true
            # 处理无效的net值
            if(node['net'] == '' or node['net'] == 'none' or node['net'] == 'null'):
                node['net'] = 'tcp'
            # 处理无效的type值 默认type类型为none，如果type类型为vmess，则还原为none，其他状态为tcp,kcp,QUIC,grpc等
            if(node['type'] == '' or node['type'] == 'vmess' or node['type'] == 'null'):
                node['type'] = 'none'
            # 判断UUID-id是否有效（id长度=36）
            id = node['id']
            if (len(id) != 36):
                return ''
            # 检查aid值是否为数字
            aid = str(node['aid'])
            if (aid.isdigit() == False):
                aid = '0'
            # cipher = node['scy']
            # if (cipher == 'rc4-md5'):
            #     return ''
            # 处理关联参数
            net = node['net']
            if(net == 'grpc' or net == 'h2'):
                node['tls'] = 'true'

            # 字典转换为字符串"格式
            onenode = json.dumps(node)
        except Exception as ex:
            LocalFile.write_LogFile('SubConvert-Line-301-Exception: ' + str(ex) + '\n' + onenode)
            onenode = ''
        return onenode

    # 字典格式节点转换成节点URL
    def clash_to_all_url(oldonenode):
        try:
            # 一般格式转化为字典
            onenode = SubConvert.clash_all_to_json(oldonenode)
            if(onenode == ''):
                return ''
            node = json.loads(onenode)
            if (node['type'] == 'ss'):
                onenode = 'ss://' +  base64.b64encode((node['cipher'] + ':' + node['password'] + '@' + node['server'] + ':' + str(node['port'])).encode("utf-8")).decode("utf-8") + '#' + node['name']
            elif (node['type'] == 'trojan'):
                onenode = 'trojan://' + node['password'] + '@' + node['server'] + ':' + str(node['port']) + '#' + node['name']
            elif (node['type'] == 'vmess'):
                onenode = SubConvert.name_clash_to_v2ray(onenode)
                onenode = 'vmess://' + base64.b64encode(onenode.encode("utf-8")).decode("utf-8")
                onenode = SubConvert.check_url_v2ray_vmess(onenode)
            elif (node['type'] == 'ssr'):
                # {name: "[SSR] 🇸🇬 SG", server: sg-am3.eqsunshine.com, port: 32001, type: ssr, cipher: aes-256-cfb, password: 3g0dHlKME, protocol: origin, obfs: tls1.2_ticket_auth, protocol-param: "", obfs-param: "", udp: true}
                # ====>>>>>>> 
                # gz1.52168.xyz:1115:auth_aes128_sha1:aes-256-cfb:tls1.2_ticket_auth:ZXBDaEpTMzVmVg==/?obfsparam=OTRkOWIyNjkwMS5iYWlkdS5jb20&protoparam=MjY5MDE6Z2d5ZjNjMnF6b2c&remarks=MTcz5py65Zy64oie6aaZ5riv&group=
                onenode = node['server'] + ':' + node['port'] + ':' + node['protocol'] + ':' + node['cipher'] + ':' + node['obfs'] + ':' + base64.b64encode(node['password'].encode("utf-8")).decode("utf-8")
                if('obfs-param' in node.keys()):
                    onenode += '/?obfsparam=' + base64.b64encode(node['obfs-param'].encode("utf-8")).decode("utf-8")
                else:
                    onenode += '/?obfsparam='
                if('protocol-param' in node.keys()):
                    onenode += '&protoparam=' + base64.b64encode(node['protocol-param'].encode("utf-8")).decode("utf-8") 
                onenode += '&remarks=' + base64.b64encode(node['name'].encode("utf-8")).decode("utf-8")
                onenode = 'ssr://' + base64.b64encode(onenode.encode("utf-8")).decode("utf-8")
        except Exception as ex:
            LocalFile.write_LogFile('SubConvert-Line-375-Exception:' + str(ex) + '\noldonenode:' + oldonenode)
            onenode = ''
        return onenode

    # Surge格式转化对应的ss,trojan,vmess等
    def surge_to_all_url(onenode):
        try:
            #ssrsub__02=ss,211.99.96.10,11316,encrypt-method=aes-256-gcm,password=gTVvCY
            if(onenode.find(',') == -1 or onenode == ''):
                return '' # 空值忽略
            else:
                print('SubConvert-Line-168-oldnode:' + onenode)
            #onenode = onenode.strip('- ')
            onenode = onenode.replace(' ', '')
            onenode = onenode.replace('encrypt-method=', 'cipher=')
            onenode = onenode.replace('username=', 'uuid=')
            onenode = onenode.split('=', 1)[1]
            ii = 0
            nenode = ''
            for i in onenode.split(','):
                if(ii == 0 and i.find('=') > -1):
                    nenode = nenode + ',"type":"' + i.rsplit('=', 1)[1]
                elif(ii == 1):
                    nenode = nenode + ',"server":"' + i
                elif(ii == 2):
                    nenode = nenode + ',"port":"' + i
                else:
                    if(i.find('=') > -1):
                        a = i.split('=', 1)[0]
                        b = i.split('=', 1)[1]
                        if(len(a) > 0):
                            nenode = nenode + ',"' + a + '":"' + b.strip(' ')
                ii += 1
            onenode = '{' + nenode.strip(',') + '}'
            # 转换为字典格式
            node = json.loads(onenode.replace(' ', '').replace('\n', ''))
            if (node['type'] == 'ss'):
                onenode = 'ss://' +  base64.b64encode((node['cipher'] + ':' + node['password'] + '@' + node['server'] + ':' + node['port']).encode("utf-8")).decode("utf-8") + '#' + node['name']
            elif (node['type'] == 'trojan'):
                onenode = 'trojan://' + node['password'] + '@' + node['server'] + ':' + node['port'] + '#' + node['name']
            elif (node['type'] == 'vmess'):
                onenode = SubConvert.clash_all_to_json(onenode)
                onenode = SubConvert.name_clash_to_v2ray(onenode)
                onenode = 'vmess://' + base64.b64encode(onenode.encode("utf-8")).decode("utf-8")
                onenode = SubConvert.check_url_v2ray_vmess(onenode)
        except Exception as ex:
            LocalFile.write_LogFile('SubConvert-Line-201-Exception:' + str(ex) + '\n' + onenode)
            onenode = ''
        return onenode
        
    # vmess-v2ray格式名称转换成clash格式名称
    def name_v2ray_to_clash(onenode):
        try:
            # 字段转换
            # {"name":"\ud83c\uddfa\ud83c\uddf8-\u7f8e\u56fd-47.253.58.149","server":"47.253.58.149","port":"443","type":"vmess","uuid":"91646f9a-b4e9-4aca-bfe3-8892b3e58fe7","alterId":"0","cipher":"auto","tls":"true","network":"ws","ws-opts":"","path":"/ray","headers":"","host":"lg30.cfcdn3.xyz"}
            if (onenode.find('"id":') > -1):
                onenode = onenode.replace('"ps":', '"name":')
                onenode = onenode.replace('"scy":', '"cipher":')
                onenode = onenode.replace('"net":', '"network":')
                onenode = onenode.replace('"add":', '"server":')
                onenode = onenode.replace('"aid":', '"alterId":')
                onenode = onenode.replace('"id":', '"uuid":')
            elif(onenode.find('"uuid":') == -1):
                LocalFile.write_LogFile('SubConvert-Line-159-onenode: ' + onenode + '\n')
                return ''
            onenode = onenode.replace('"ws-headers":', '"headers":')
            onenode = onenode.replace('"ws-path":', '"path":')

            node = json.loads(onenode)

            # 处理UUID名称
            if (len(node['uuid']) != 36):
                return ''
            # 端口不能为非数字，过滤V2ray不支持的加密方式的节点
            alterId = str(node['alterId'])
            if(alterId.isdigit() == False):
                node['alterId'] = '0'
            # 处理关联参数
            if(node['network'] == 'grpc' or node['network'] == 'h2'):
                node['tls'] = 'true'
            # port3 = port.isdigit()

            # 字典转换为json格式的字符串
            onenode = json.dumps(node)
        except Exception as ex:
            LocalFile.write_LogFile('SubConvert-Line-189-Exception: ' + str(ex) + '\n' + onenode + '\n')
            onenode = ''
        return onenode

    # vmess的v2ray格式转换成clash格式
    def v2ray_vmess_to_clash(onenode):
        try:
            # onenode = '{"server":"8.219.216.254","alterId":0,"host":"p1.chigua.tk","uuid":"ffffffff-ffff-ffff-ffff-ffffffffffff","network":"ws","path":"/vmess","port":443,"name":"\ud83c\udde8\ud83c\uddf3-\u4e2d\u56fd-8.219.216.254","cipher":"aes-128-gcm","sni":"p1.chigua.tk","tls":"tls","type":"none"}'
            # V2ray处理为数组格式，解决值中的{}问题
            onenode = SubConvert.name_v2ray_to_clash(onenode)
            onenode = onenode.replace(' ', '')
            node = json.loads(onenode)
            onode = ''
            # 模式1，显示所有参数
            for key, value in node.items():
                if(key == 'name'):
                    onode = onode + '\n  name: ' + '\'' + value + '\''
                elif(key == 'type'):
                    onode = onode + '\n  ' + key + ': vmess'
                elif(key == 'password'):
                    onode = onode + '\n  ' + key + ': ' + value.replace('!<str>', '').replace('<', '').replace('>', '')
                elif(key == 'port'):
                    if(isinstance(value, int)):
                        onode = onode + '\n  ' + key + ': ' + str(value)
                    else:
                        onode = onode + '\n  ' + key + ': 443' # 只有端口有效，其他两参数如果不为数字，则错误
                elif(key == 'tls' or key == 'udp' or key == 'skip-cert-verify' or key == 'allowinsecure'):
                    if(value == 'tls' or value == 'True' or value == 'true'):
                        onode = onode + '\n  ' + key + ': true'
                        # 此行修改字典数据，要不后面的操作出错
                        node[key] = 'true'
                    else:
                        onode = onode + '\n  ' + key + ': false'
                        # 此行修改字典数据，要不后面的操作出错
                        node[key] = 'false'
                elif(key == 'host' or key == 'Host'):
                    if(value.find('%') == -1):
                        onode = onode + '\n  ' + key + ': ' + value
                elif(key == 'alpn'):
                    onode = onode + '\n  ' + key + ': '
                    alpn = value.replace('%2C',',').replace('%2F','/') + ','
                    for ia in alpn.split(','):
                        if(ia != ''):
                            onode = onode + '\n    - ' + ia
                else:
                    if(len(key) > 0):
                        onode = onode + '\n  ' + key + ': ' + str(value)
                # ws-opts: {path: /6, headers: {host: "%7B%22Host%22:%22live.bilibili.com%22%7D"}}
            onode = onode.strip('\n  ')
            # 安全认证设置
            if(onenode.find('tls: true') > -1 and onenode.find('allowinsecure') == -1):
                onode = onode + '\n  allowinsecure: true'
            # CLash不支持密码中存在<>
            if((onenode.find('<') > -1 and onenode.find('>') > -1) or onenode.find('%') > -1):
                print('SubConvert-Line-262-not-supported-node:\n' + onenode)
                return ''
            else:
                print('SubConvert-Line-265-onenode:\n' + onenode)
            
            # 严格模式2
            onode = 'name: \'' + node['name'] + '\''
            onode += '\n  server: ' + node['server']
            onode += '\n  port: ' + str(node['port'])
            onode += '\n  type: vmess'
            onode += '\n  uuid: ' + node['uuid']
            onode += '\n  alterId: ' + str(node['alterId'])
            onode += '\n  cipher: ' + node['cipher']
            onode += '\n  tls: ' + node['tls']
            onode += '\n  skip-cert-verify: true'
            onode += '\n  network: ' + node['network']
            if(onenode.find('"sni"') > -1):
                onode += '\n  sni: ' + node['sni']
            if(onenode.find('"alpn"') > -1):
                onode += '\n  alpn: ' + node['alpn']
            if(onenode.find('"plugin-opts"') > -1):
                # plugin: obfs, plugin-opts: {mode: tls, host: n46hm52773.wns.windows.com}
                onode += '\n  plugin-opts: {mode: ' + node['mode'] + ', host: ' + node['host'] + '}'
            if(onenode.find('"headers"') > -1):
                # headers: {Host: t.me/vpnhat}}
                onode += '\n  headers: {Host: ' + node['host'] + '}'
            if(onenode.find('"ws-opts"') > -1 and onenode.find('"host"') > -1):
                # ws-opts: {path: /ray, headers: {Host: localhoster.ml}}
                onode += '\n  ws-opts: {path: ' + node['path'] + ', headers: {Host: ' + node['host'] + '}}'
            elif(onenode.find('"ws-opts"') > -1 and onenode.find('"host"') == -1):
                # ws-opts: {path: /ray}
                onode += '\n  ws-opts: {path: ' + node['path'] + '}'
            if('path' in node.keys()):
                path = node['path']
                if(path.find('[') == -1):
                    path = '[' + path + ']'
                if(onenode.find('"http-opts"') > -1 and onenode.find('"method"') > -1):
                    # http-opts: {method: GET, path: [/]}
                    onode += '\n  http-opts: {method: ' + node['method'] + ', path: ' + path + '}'
                elif(onenode.find('"http-opts"') > -1 and onenode.find('"method"') == -1):
                    # http-opts: {path: [/]}
                    node['network'] = 'http'
                    onode += '\n  http-opts: {path: ' + path + '}'
            if(onenode.find('"udp"') > -1):
                onode += '\n  udp: ' + node['udp']
            # onenode = '- ' + onode

            # 严格模式3
            onode = 'name: \'' + node['name'] + '\''
            onode += ', server: ' + node['server']
            onode += ', port: ' + str(node['port'])
            onode += ', type: vmess'
            onode += ', uuid: ' + node['uuid']
            onode += ', alterId: ' + str(node['alterId'])
            onode += ', cipher: ' + node['cipher']
            onode += ', tls: ' + node['tls']
            onode += ', skip-cert-verify: true'
            onode += ', network: ' + node['network']
            if(onenode.find('"sni"') > -1):
                if(node['sni'] != ''):
                    onode += ', sni: ' + node['sni']
            if(onenode.find('"alpn"') > -1):
                if(node['alpn'] != ''):
                    onode += ', alpn: ' + node['alpn']
            # 带插件的vmess
            if('ws-opts' in node.keys()):
                # ws-opts: {path: /, headers: {Host: london1.na.invari.na.oonvari.com}}
                node['network'] = 'ws'
                onode += ', ws-opts: {'
                xonode = ''
                #if('method' in node.keys()):
                #    xonode += 'method: ' + node['method'] + ', '
                if('path' in node.keys()):
                    xonode += 'path: ' + node['path'] + ', '
                if('headers' in node.keys()):
                    xonode += 'headers: {Host: ' + node['host'] + '}, '
                onode += xonode.strip(', ') + '}'
            elif('http-opts' in node.keys()):
                # http-opts: {method: GET, path: [/]} # http-opts: {path: [/]}
                node['network'] = 'http'
                onode += ', http-opts: {'
                xonode = ''
                if('method' in node.keys()):
                    xonode += 'method: ' + node['method'] + ', '
                if('headers' in node.keys()):
                    if(node['host'].find('[') == -1):
                        xonode += 'headers: {Host: [' + node['host'] + ']}, '
                    else:
                        xonode += 'headers: {Host: ' + node['host'] + '}, '
                if('path' in node.keys()):
                    path = node['path']
                    if(path.find('[') == -1):
                        path = '[' + path + ']'
                    xonode += 'path: ' + path + ', '
                onode += xonode.strip(', ') + '}'
            elif('plugin-opts' in node.keys()):
                # plugin: obfs, plugin-opts: {mode: tls, host: n46hm52773.wns.windows.com}
                # plugin-opts: mode: tls # or http # host: bing.com
                # node['network'] = 'http'
                onode += ', plugin: obfs, plugin-opts: {'
                xonode = ''
                if('mode' in node.keys()):
                    xonode += 'mode: ' + node['mode'] + ', '
                if('headers' in node.keys()):
                    xonode += 'host: [' + node['host'] + ', '
                onode += xonode.strip(', ') + '}'
            else:
                if(onenode.find('"headers"') > -1):
                    # headers: {Host: t.me/vpnhat}}
                    onode += ', headers: {Host: ' + node['host'] + '}'
            if(onenode.find('"udp"') > -1):
                onode += ', udp: ' + node['udp']
            onenode = '  - {' + onode + '}'            
        except Exception as ex:
            LocalFile.write_LogFile('SubConvert-Line-590-Exception:' + str(ex) + '\n' + onenode)
            onenode = ''
        return onenode
