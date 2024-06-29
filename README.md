# hostcheck

Check and validate host details:
+ Check OS release
+ Add default apt repo list
+ Disk checks:
    + Partitions **&#x2611;**
    + LVM lists **&#x2611;**
    + Mounting
        + /var/log
        + NFS mount
    + Check /etc/fstab
+ Resource Check
    + CPU **&#x2611;**
    + Memory **&#x2611;**
+ Network
    + IP/Netmask Check **&#x2611;**
    + DNS **&#x2611;**
    + netplan config **&#x2611;**
+ Sysbench
    + Resource Health Check
+ Check Access Lists **&#x2611;**
+ Services:
    + Timesyncd(similar to NTP) **&#x2611;**
    + Zabbix Agent: service status (health check + service enabled)
    + Splunk Agent: service status (health check + service enabled) **&#x2611;**
    + Journald: set log size **&#x2611;**
    + syslog: /etc/logrotate.d/rsyslog (7 --> 1;sudo systemctl restart syslog)
    + SSHD: Increase SSH process priority
    + SSSD + Sudoers: **&#x2611;**
    + SSH authorized_keys **&#x2611;**
    + ManageEngine Log Rotate: 
        /usr/local/manageengine/uems_agent/data/patch
        /usr/local/manageengine/uems_agent/data/logs
+ Add asax.local crt **&#x2611;**.
+ Check /etc/hosts to avoid hardcode repos

# Tags

* For each role, there is a Tag name equal with its name (e.g. `access_check`)
* To do just check host details and check there is mismatched or not use `info_check` tag.

# Info Check
Some roles (with `info_check` tag) contains checking information like disks, network and etc.
If there is mismatched, add `-vvv` to `ansible-playbook` command to show details.
> You can also use debug output( by adding -vvv). They are in yaml format, simply can copy and paste to inventory.

## Access Check
If there is a failed access, we show them as *Change* task not a fail.

+ Ping all:
```
ansible -K -k -i ../inventory -e 'ansible_user=<YOUR_USER>@<ENV_DOMAIN>' -m ping all
```

+ Check all access lists:
```
ansible-playbook -K -k -i ../inventory main.yml -b -e 'ansible_user=<YOUR_USER>@<ENV_DOMAIN>' -t access_check
```

+ Check access lists of specific host:
```
ansible-playbook -K -k -i ../inventory main.yml -b -e 'ansible_user=<YOUR_USER>@<ENV_DOMAIN>' -t access_check -l "<HOST>"
```

+ Check single access (Use `access_check.yml` playbook):
```
ansible-playbook -K -k -i ../inventory access_check.yml -b -e 'ansible_user=<YOUR_USER>@<ENV_DOMAIN>' -t access_check -l "<HOST>" -e "access_check_single=<IP/DOMAIN>:<PORT>"
```

For example:
```
ansible-playbook -K -k -i ../inventory access_check.yml -b -e 'ansible_user=test@stdc.local' -t access_check -l "bs-kube-lb*" -e "access_check_single=bs-kube-m1:6443"
```
