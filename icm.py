#!/usr/bin/env python3

import socket
import json
from math import inf as infinity

def record_ip(addr, clients, min_machines = 0):
    if addr not in clients:
        clients[addr] = 0
    if len(clients) >= min_machines:
        clients[addr] += 1

def too_many_pings(clients, max_pings):
    return min(clients.items(), key = lambda x: x[1])[1] > max_pings

def dump_json(clients):
    client_array = []
    for key in clients:
        d = {}
        d["ip"] = key
        d["count"] = clients[key]
        client_array.append(d)

    f = open("ping.json", "w")
    json.dump(client_array, f, indent = 4)
    f.close()

def listen(max_pings = infinity, clients = {}):
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
    while 1:
        data, addr = s.recvfrom(1508)
        record_ip(addr[0], clients)
        print(addr[0], "\t:", clients[addr[0]])
        dump_json(clients)
        if too_many_pings(clients, max_pings):
            return True

if __name__ == "__main__":
    listen()

