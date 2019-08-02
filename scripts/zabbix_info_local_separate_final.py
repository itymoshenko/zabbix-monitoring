import requests
import json
import csv
import os

__author__ = 'itymoshenko'

# Variables
zab_server = 'http://x.x.x.x/zabbix/'
zab_url = zab_server + '/api_jsonrpc.php'
username = "api_name"
password = "api_pass"


def check_file(file_name):
    """ Check if output files exist and remove them with new execution of the script """
    if os.path.exists(file_name):
        os.remove(file_name)


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
                simple_writer.writerow(["{0} count: {1}".format(data_name, data_count)])
                simple_writer.writerow(["There is no {0} for {1}!".format(data_name, hostname)])
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
                  'output': ['status', 'description', 'state', 'priority', 'comments', 'error', 'expression',
                             'recovery_expression', 'manual_close'],
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
    return problem_triggers, triggers_count, data_name


def all_triggers():
    """ Get list of all configured triggers for each host """
    values = {'jsonrpc': '2.0',
              'method': 'trigger.get',
              'params': {
                  'filter': {'hostid': host_id},
                  'output': ['status', 'description', 'state', 'priority', 'comments', 'error', 'expression',
                             'recovery_expression', 'manual_close'],
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
    return triggers, triggers_count, data_name


def trigger_prototype():
    """ Get list of all trigger prototypes for each host """
    values = {'jsonrpc': '2.0',
              'method': 'triggerprototype.get',
              'params': {
                  'filter': {'hostid': host_id},
                  'output': ['expression', 'description', 'status', 'priority', 'comments', 'error', 'state',
                             'recovery_expression', 'manual_close', 'discoveryRule'],
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
    return triggerprototype, tp_count, data_name


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
    return discovery, discovery_count, data_name


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
    return web, web_count, data_name


host_list = hosts_list(zab_token)

for h in host_list:
    host_id = h['hostid']
    hostname = h['host']
    output_file = "{0}.csv".format(hostname)
    check_file(output_file)
    csv_out(active_triggers()[0], output_file, active_triggers()[1], active_triggers()[2])
    csv_out(all_triggers()[0], output_file, all_triggers()[1], all_triggers()[2])
    csv_out(discovery_rules()[0], output_file, discovery_rules()[1], discovery_rules()[2])
    csv_out(trigger_prototype()[0], output_file, trigger_prototype()[1], trigger_prototype()[2])
    csv_out(web_monitoring()[0], output_file, web_monitoring()[1], web_monitoring()[2])
