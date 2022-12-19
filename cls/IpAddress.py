#!/usr/bin/env python3

import requests
import socket
import json
#from ip import QQwry
from qqwry import QQwry
from cls.IsValid import IsValid

class IpAddress():
    # 通过域名获取IP
    def getIP(domain):
      try:
        print('get-domain-Ip:' + domain)
        domain = socket.getaddrinfo(domain, 'http')
        return domain[0][4][0]
      except:
        return '127.0.0.1'

    def get_ip_list(domain): # 获取域名解析出的IP列表
        ip_list = []
        try:
            addrs = socket.getaddrinfo(domain, None)
            for item in addrs:
                if item[4][0] not in ip_list:
                    ip_list.append(item[4][0])
        except Exception as e:
            # print(str(e))
            pass
        return ip_list
            
    # 通过IP获取国家名称并添加国旗符号，print(get_country) 
    def get_country(ipdomain):
        if(ipdomain != ''):
            global ip_info
            ip_country = ''
            ipdomainurl = ''
            try:
                q = QQwry()
                q.load_file('./res/qqwry.dat', loadindex=False)
                #q.lookup('8.8.8.8')
                if(IsValid.isIP(ipdomain) == False):
                    domain = ipdomain
                    ipdomain = IpAddress.getIP(ipdomain)
                    print(domain + '---' + ipdomain)
                #print('QQwryIp is loaded. ' + str(q.is_loaded()) + '-' + str(IsValid.isIP(ipdomain)) + '-' + ipdomain + '-' + q.lookup(ipdomain)[0]) #+ '-' + q.lookup(ipdomain)[1]) #('国家', '省份')
                if(q.is_loaded() == True):
                    ip_country = q.lookup(ipdomain)[0]
                    if(ip_country == 'None'):
                        ip_country = ''
                if(ip_country == ''):
                    #rq = requests.get("http://ip-api.com/json/{}?lang=zh-CN".format(node['add']), timeout=30) #连接超时 和 读取超时 均为30
                    ipdomainurl = 'http://ip-api.com/json/' + ipdomain + '?lang=zh-CN'
                    #https://api.ip.sb/geoip/1.1.1.1
                    rq = requests.get(ipdomainurl, timeout=10) #连接超时 和 读取超时 均为30
                    if (rq.status_code == 200):
                        ip_info = json.loads(rq.content)
                        if (ip_info['status'] == 'success'):
                            ip_country = ip_info['country']
                    else:
                        print('Line-128: download sub error on link: [' + str(rq.status_code) + ']' + ipdomainurl)
                        ipdomainurl = 'http://ip.360.cn/IPQuery/ipquery?ip=' + ipdomain
                        rq = requests.get(ipdomainurl, timeout=10)
                        if (rq.status_code == 200):
                            ip_info = json.loads(rq.content)
                            if (ip_info['errno'] == '0'):
                                #ip_country = ip_info['data'].encode('utf-8').decode('unicode_escape')
                                ip_country = ip_info['data'].encode('utf-8').decode('utf-8')
                        else:
                            print('Line-137: download sub error on link: [' + str(rq.status_code) + ']' + ipdomainurl)
                            ipdomainurl = 'http://ipinfo.io/' + ipdomain + '?token=7f459101a94acc'
                            rq = requests.get(ipdomainurl, timeout=10)
                            if (rq.status_code == 200):
                                ip_info = json.loads(rq.content)
                                ip_country = ip_info['country'].encode('utf-8').decode('utf-8')
                            else:
                                ip_country = "未知"
                                print('Line-145: download sub error on link: [' + str(rq.status_code) + ']' + ipdomainurl)
                #print(ip_country)
                ip_country = ip_country.encode('utf-8').decode('utf-8')
                ip_country = ip_country.replace('台湾省', '台湾', 1)
                #if(len(ip_country)>3):
                #    old_ip_country = ip_country[0:3]
                #else:
                #    old_ip_country = ip_country
                emoji = {
                    'US': '🇺🇸', 'HK': '🇭🇰', 'SG': '🇸🇬', 'JP': '🇯🇵', 'TW': '🇹🇼', 'CA': '🇨🇦', 'GB': '🇬🇧', 'CN': '🇨🇳', 'NL': '🇳🇱',
                    'TH': '🇹🇭', 'BE': '🇧🇪', 'IN': '🇮🇳', 'IT': '🇮🇹', 'PE': '🇵🇪', 'RO': '🇷🇴', 'AU': '🇦🇺', 'DE': '🇩🇪', 'RU': '🇷🇺',
                    'KR': '🇰🇷', 'DK': '🇩🇰', 'PT': '🇵🇹', 'CY': '🇨🇾', 'ES': '🇪🇸', 'RELAY': '🏁', 'NOWHERE_LAND': '🇦🇶',
                    '澳大利亚': '🇦🇺', '阿尔巴尼亚': '🇦🇱', '阿根廷': '🇦🇷', '比利时': '🇧🇪', '秘鲁': '🇵🇪', '波兰': '🇵🇱', '德国': '🇩🇪', '俄罗斯': '🇷🇺',
                    '法国': '🇫🇷', '加拿大': '🇨🇦', '罗马尼亚': '🇷🇴', '日本': '🇯🇵', '韩国': '🇰🇷', '荷兰': '🇳🇱', 
                    '美国': '🇺🇸', '南非': '🇿🇦', '挪威': '🇳🇴', '葡萄牙': '🇵🇹', '瑞典': '🇸🇪', '泰国': '🇹🇭', '台湾': '🇹🇼', '斯洛伐克': '🇸🇰',
                    '瑞士': '🇨🇭', '乌克兰': '🇺🇦', '西班牙': '🇪🇸', '香港': '🇭🇰', '新加坡': '🇸🇬', '新西兰': '🇳🇿', 
                    '意大利': '🇮🇹', '伊朗': '🇮🇷', '英国': '🇬🇧', '印度': '🇮🇳', '智利': '🇨🇱', '中国': '🇨🇳', '欧洲': '🇪🇸',
                }
                if ip_country in emoji:
                    ip_country = emoji[ip_country] + '-' + ip_country
                else:
                    # 方法三: 最快，推荐方法
                    for k,v in emoji.items(): 
                        if(ip_country.find(k) > -1):
                            ip_country = v + '-' + ip_country
                            #print('n:' + v)
                            break
                if(ip_country.find('-') == -1 and (ip_country.find('省') == -1 or ip_country.find('市') == -1)):
                    ip_country = emoji['NOWHERE_LAND'] + '-' + ip_country
            except Exception as ex:
                print('IpAddress-Line-124-Exception: ' + str(ex) + '\nipdomainurl:' + ipdomainurl + '-ipdomain:' + ipdomain)
            return ip_country.encode('utf8').decode('utf-8')
        else:
            print('Line-122: 域名或IP为空')
