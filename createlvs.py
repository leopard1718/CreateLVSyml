# coding=utf-8
import csv

#只支持单个VIP


def list_to_cfg(vip4list, vip6list, portlist, realip4list, realip6list, vriipv4, vriipv6, instances_state, priority, filename):
    with open(filename, 'a') as f:
        for vip4 in vip4list:
            for vri in vriipv4:
                f.write('''      "VI_'''+ vri +'''":\n        "auth_pass": "secret"\n        "auth_type": "PASS"\n        "instances_state": "'''+ instances_state +'''"\n        "interface": "bond0"\n        "priority": "'''+ priority +'''"\n        "track_interface":\n        - "bond0"\n        "virtual_ipaddress":\n        - "'''+ vip4 +'''/32"\n        "virtual_router_id": "'''+ vri +'''"\n''')
        for vip6 in vip6list:
            for vri in vriipv6:
                f.write('''      "VI_'''+ vri +'''":\n        "auth_pass": "secret"\n        "auth_type": "PASS"\n        "instances_state": "'''+ instances_state +'''"\n        "interface": "bond0"\n        "priority": "'''+ priority +'''"\n        "native_ipv6": !!bool "true"\n        "version": "3"\n        "track_interface":\n        - "bond0"\n        "virtual_ipaddress":\n        - "'''+ vip6 +'''/128"\n        "virtual_router_id": "'''+ vri +'''"\n''')
        f.write('''  "profiles::lb::l4":\n    "real_servers":\n''')
        f.write('''      "RS_8686_127.0.0.1":\n        "ip_address": "127.0.0.1"\n        "options":\n          "TCP_CHECK":\n            "connect_port": "8686"\n            "connect_timeout": "10"\n            "delay_before_retry": "3"\n            "nb_get_retry": "3"\n          "weight": "1"\n        "port": "8686"\n        "virtual_server": "LVS_8686"\n''')
        for vip4 in vip4list:
            for port in portlist:
                for realip4 in realip4list:
                    f.write('''      "RS_'''+port+'''_'''+realip4.replace(':', '-')+'''":\n        "ip_address": "'''+ realip4 +'''"\n        "options":\n          "TCP_CHECK":\n            "connect_port": "'''+port+'''"\n            "connect_timeout": "10"\n            "delay_before_retry": "3"\n            "nb_get_retry": "3"\n          "weight": "1"\n        "port": "'''+port+'''"\n        "virtual_server": "LVS_'''+vip4.replace(':', '-')+'''_ipv4"\n''')

        for vip6 in vip6list:
            for port in portlist:
                for realip6 in realip6list:
                    f.write('''      "RS_'''+port+'''_'''+realip6.replace(':', '-')+'''":\n        "ip_address": "'''+ realip6 +'''"\n        "options":\n          "TCP_CHECK":\n            "connect_port": "'''+port+'''"\n            "connect_timeout": "10"\n            "delay_before_retry": "3"\n            "nb_get_retry": "3"\n          "weight": "1"\n        "port": "'''+port+'''"\n        "virtual_server": "LVS_'''+vip6.replace(':', '-')+'''_ipv6"\n''')
        f.write('''    "virtual_servers":\n''')

        for vip4 in vip4list:
            f.write('''      "LVS_8686":\n        "delay_loop": "7"\n        "ip_address": "'''+vip4+'''"\n        "lb_algo": "wlc"\n        "lb_kind": "DR"\n        "persistence_timeout": "600"\n        "port": "8686"\n        "protocol": "TCP"\n        "virtualhost": "LVS"\n''')
            f.write('''      "LVS_'''+vip4.replace(':', '-')+'''_ipv4":\n        "delay_loop": "7"\n        "ip_address": "'''+vip4+'''"\n        "lb_algo": "wlc"\n        "lb_kind": "DR"\n        "persistence_timeout": "600"\n        "port": "0"\n        "protocol": "TCP"\n        "virtualhost": "LVS"\n''')
            f.write('''      "LVS_'''+vip6.replace(':', '-')+'''_ipv6":\n        "delay_loop": "7"\n        "ip_address": "'''+vip6+'''"\n        "lb_algo": "wlc"\n        "lb_kind": "DR"\n        "persistence_timeout": "600"\n        "port": "0"\n        "protocol": "TCP"\n        "virtualhost": "LVS"\n''')
if __name__ == '__main__':
    #list_to_cfg(['39.134.215.14'], ['2409:8087:4400:1:3:1710:802:1'], ['80'], ['39.134.215.6'], ['2409:8087:4400:1:3:1710:801:3'], 'txt')


    filename = 'lvs.csv'
    #注意csv使用utf-8编码
    #csv列表，按照(LVS主机名|LVS地址|80（默认80端口，暂只支持IP调度）|ipv4VIP(支持多个英文逗号分隔)|ipv6VIP(支持多个)|ipv4RIF(多个)|ipv6RIP(多个)|VRIipv4(virtual route ID)|VRIipv6|主备|权重)
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            portlist = row[2].strip(',').split(',')
            rip4ist = row[5].strip(',').split(',')
            rip6ist = row[6].strip(',').split(',')
            vri4ist = row[7].strip(',').split(',')
            vri6ist = row[8].strip(',').split(',')
            vip6ist = row[4].strip(',').split(',')
            vip4ist = row[3].strip(',').split(',')
            instances = row[9]
            prio = row[10]
            hostname = row[0]
            hostip = row[1]
            print(hostip)
            list_to_cfg(vip4ist, vip6ist, portlist, rip4ist, rip6ist, vri4ist, vri6ist, instances, prio, ""+hostname+"-"+hostip+".txt")