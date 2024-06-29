#!/usr/bin/python3
from telnetlib import Telnet
from ansible.module_utils.basic import *
import dns.resolver
import logging

logging.basicConfig(level=logging.DEBUG)

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def telnet(dst: str, port: int, timeout=3):
    try:
        with Telnet(host=dst, port=port, timeout=timeout) as tn:
            return True
    except Exception as error:
        logging.error('Error on telnet %s', error)
        return False

def main():

    module = AnsibleModule(
        {
            "dst": {"default": True, "type": "str"},
            "port": {"default": True, "type": "int"},
            "timeout": {"default": False, "type": "int"},
            "failed_on": {"default": False, "type": "bool"},
        }
    )
    logging.info('Arguments: %s', module.params)
    print(module.params['failed_on'])
    # Check IP format
    if validate_ip(module.params['dst']):
        logging.debug('Dst has IP format')
        access = telnet(module.params['dst'], module.params['port'], module.params['timeout'])
        if module.params['failed_on']:
            module.exit_json(failed=not access, changed=not access, access=access)
        else:
            module.exit_json(changed=not access, access=access)
    # Domain Format
    else:
        logging.debug('Dst has DOMAIN format')
        access_returns = []
        try:
            ips = dns.resolver.resolve(module.params['dst'], 'A', search=True)
            logging.debug('list of A records for %s: %s', module.params['dst'], [ip.to_text() for ip in ips])
            for ip in ips:
                logging.debug(ip)
                access_returns.append(telnet(str(ip), module.params['port'], module.params['timeout']))
            logging.debug(all(access_returns))
            if module.params['failed_on']:
                module.exit_json(failed=not all(access_returns), changed=not all(access_returns), access=all(access_returns))
            else:
                module.exit_json(changed=not all(access_returns), access=all(access_returns))
        except Exception as e:
            logging.error('Error on DNS resolver %s', e)
            module.fail_json(e)
if __name__ == '__main__':
    main()