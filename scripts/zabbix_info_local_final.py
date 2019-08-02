import requests
import json
import csv
import os

__author__ = 'itymoshenko'

# Variables
csv_file_for_active_triggers = "active_triggers_local.csv"
csv_file_for_all_triggers = "all_triggers_local.csv"
csv_file_for_discovery_rules = "discovery_rules_local.csv"
csv_file_for_web_monitoring = "web_monitoring_output_local.csv"
csv_file_for_trigger_prototype = "trigger_prototype_local.csv"
file_list = [csv_file_for_active_triggers, csv_file_for_all_triggers,
             csv_file_for_discovery_rules, csv_file_for_web_monitoring,
             csv_file_for_trigger_prototype]
zab_server = 'http://x.x.x.x/zabbix/'
zab_url = zab_server + '/api_jsonrpc.php'
username = "api_name"
password = "api_pass"


def check_file():
    """ Check if output files exist and remove them with new execution of the script """
    for item in file_list:
        if os.path.exists(item):
            os.remove(item)
        else:
            print("Sorry, I can not remove %s file. This file doesn't exist." % item)


check_file()


def request(zab_url, values):
    """ Send request to Zabbix via API """
    headers = {"content-type": "application/json-rpc"}
    data = json.dumps(values)
    req = requests.post(zab_url, data=data, headers=headers)
    response = req.json()
    result = response['result']
    return result


def authenticate(user_name, passwd):
    """ Get authorization token for Zabbix API """
    values = {'jsonrpc': '2.0',
              'method': 'user.login',
              'params': {
                  'user': user_name,
                  'password': passwd
              },
              'id': '0'
              }
    result = request(zab_url, values)
    return result


zab_token = authenticate(username, password)


def hosts_list(zab_token):
    """ Get list of active hosts from Zabbix """
    values = {'jsonrpc': '2.0',
              'method': 'host.get',
              'params': {
                  'output': ['hostid', 'host'],
                  'monitored_hosts': 1,
              },
              'auth': zab_token,
              'id': '1'
              }
    hosts = request(zab_url, values)
    return hosts


def csv_out(data_source, output_file, data_count, data_name):
    """ This function writes data to csv files
    :param data_name: just specific data name
    :param data_count: count of elements in list
    :param output_file: name of csv file
    :param data_source: list with specific data
    :return: csv files
    """
    if not data_source:
        try:
            with open(output_file, 'a', newline='') as file:
                simple_writer = csv.writer(file)
                simple_writer.writerow(["Hostname: {0}".format(hostname)])
                simple_writer.writerow(["{0} count: {1}".format(data_name, data_count)])
                simple_writer.writerow(["There is no active problems for {0}!".format(hostname)])
                simple_writer.writerow([])
        except IOError as err:
            errno, strerror = err.args
            print("I/O error({0}): {1}".format(errno, strerror))
    else:
        try:
            csv_columns = data_source[0].keys()
            try:
                with open(output_file, 'a', newline='') as file:
                    simple_writer = csv.writer(file)
                    simple_writer.writerow(["Hostname: {0}".format(hostname)])
                    simple_writer.writerow(["{0} count: {1}".format(data_name, data_count)])
                    simple_writer.writerow(["{0} details:".format(data_name)])
                    writer = csv.DictWriter(file, fieldnames=csv_columns)
                    writer.writeheader()
                    for data in data_source:
                        writer.writerow(data)
                    simple_writer.writerow([])
            except IOError as err:
                errno, strerror = err.args
                print("I/O error({0}): {1}".format(errno, strerror))
        except IndexError:
            pass


def active_triggers():
    """ Get list of all active triggers for each host """
    values = {'jsonrpc': '2.0',
              'method': 'trigger.get',
              'params': {
                  'filter': {'hostid': host_id, 'value': 1},
                  'output': 'extend',
                  'expandExpression': 1,
                  'expandDescription': 1,
                  'expandComment': 1,
                  'monitored': 1,
                  'active': 1
              },
              'auth': zab_token,
              'id': '2'
              }
    problem_triggers = request(zab_url, values)
    tid_list = []
    for tid in problem_triggers:
        tid_list.append(tid['triggerid'])
    triggers_count = len(tid_list)
    data_name = "Active triggers"
    csv_out(problem_triggers, csv_file_for_active_triggers, triggers_count, data_name)


def all_triggers():
    """ Get list of all configured triggers for each host """
    values = {'jsonrpc': '2.0',
              'method': 'trigger.get',
              'params': {
                  'filter': {'hostid': host_id},
                  'output': 'extend',
                  'expandExpression': 1,
                  'expandDescription': 1,
                  'expandComment': 1
              },
              'auth': zab_token,
              'id': '3'
              }
    triggers = request(zab_url, values)
    tid_list = []
    for tid in triggers:
        tid_list.append(tid['triggerid'])
    triggers_count = len(tid_list)
    data_name = "All triggers"
    csv_out(triggers, csv_file_for_all_triggers, triggers_count, data_name)


def trigger_prototype():
    """ Get list of all trigger prototypes for each host """
    values = {'jsonrpc': '2.0',
              'method': 'triggerprototype.get',
              'params': {
                  'filter': {'hostid': host_id},
                  'output': 'extend',
                  'expandExpression': 1,
                  'selectDiscoveryRule': 'extend',
              },
              'auth': zab_token,
              'id': '4'
              }
    triggerprototype = request(zab_url, values)
    tp_list = []
    for tid in triggerprototype:
        tp_list.append(tid['triggerid'])
    tp_count = len(tp_list)
    data_name = "Trigger prototypes"
    csv_out(triggerprototype, csv_file_for_trigger_prototype, tp_count, data_name)


def discovery_rules():
    """ Get list of all discovery rules for each host """
    values = {'jsonrpc': '2.0',
              'method': 'discoveryrule.get',
              'params': {
                  'filter': {'hostid': host_id},
                  'output': 'extend',
                  'expandDescription': 1,
              },
              'auth': zab_token,
              'id': '5'
              }
    discovery = request(zab_url, values)
    discovery_list = []
    for iid in discovery:
        discovery_list.append(iid['itemid'])
    discovery_count = len(discovery_list)
    data_name = "Discovery rules"
    csv_out(discovery, csv_file_for_discovery_rules, discovery_count, data_name)


def web_monitoring():
    """ Get list of all web checks for each host """
    values = {'jsonrpc': '2.0',
              'method': 'httptest.get',
              'params': {
                  'filter': {'hostid': host_id},
                  'output': 'extend',
                  'selectSteps': 'extend',
                  'monitored': 1,
              },
              'auth': zab_token,
              'id': '6'
              }
    web = request(zab_url, values)
    web_list = []
    for http_id in web:
        web_list.append(http_id['httptestid'])
    web_count = len(web_list)
    data_name = "Web monitoring"
    csv_out(web, csv_file_for_web_monitoring, web_count, data_name)


host_list = hosts_list(zab_token)

for h in host_list:
    host_id = h['hostid']
    hostname = h['host']
    active_triggers()
    all_triggers()
    discovery_rules()
    trigger_prototype()
    web_monitoring()
