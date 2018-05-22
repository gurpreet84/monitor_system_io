# -*- coding:utf-8 -*-
import time
from datetime import datetime
from collections import defaultdict
from requests import Request, Session
from requests.auth import HTTPBasicAuth

from config import LOGIN_URL, DISK_URL, CONTAINER_URL, IOPS_URL, USERNAME, PASSWORD


def join_url(ip, *apiurl):
    base = 'https://' + ip
    for api in apiurl:
        base = base + api
    return base


def cal_diff_with_utc():
    now = datetime.now()
    time.sleep(1)
    utc = datetime.utcnow()

    return int((utc - now).seconds / 3600) * 3600


def get_loginfo(ip):
    logurl = join_url(ip, LOGIN_URL)
    auth = HTTPBasicAuth(USERNAME, PASSWORD)

    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
    }

    s = Session()
    req = Request('GET', logurl, headers=headers, auth=auth)
    prepp = s.prepare_request(req)
    resp = s.send(prepp, verify=False)
    return s, headers


def get_container(session, headers, ip):

    container_info = {}
    container_url = join_url(ip, CONTAINER_URL)
    dae_response = session.get(container_url, headers=headers, verify=False, params={'fields': 'XXX'})
    result = dae_response.json()
    # GET DAPE INFO

    return container_info


def get_disk(ip):
    container = {}
    session, headers = get_loginfo(ip)
    container_info = get_container(session, headers, ip)
    for k, v in container_info.iteritems():
        dae[k] = (v, {})

    disk_url = join_url(ip, DISK_URL)
    disk_response = session.get(disk_url, headers=headers, verify=False,
                                params={
                                    'fields': 'XXXX'})
    result = disk_response.json()
    # GET DISK

    return container


def get_disk_iops(ip, interval=300):
    diff_seconds = cal_diff_with_utc()
    iopses = defaultdict(list)
    iops = defaultdict(list)
    session, headers = get_loginfo(ip)
    iops_url = join_url(ip, IOPS_URL)
    # GET IOPS

    return iopses







