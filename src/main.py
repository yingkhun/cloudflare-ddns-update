import requests, sys, time, datetime, pytz, os

class Clondflare:
    def __init__(self, email, domain, api_key, interval_time):
        self.interval_time = interval_time
        self.email = email
        if len(domain.split('.')) == 2:
            self.domain = domain
            self.full_domain = domain
        elif len(domain.split('.')) == 3:
            self.domain = domain.split('.')[1] + '.' +domain.split('.')[2]
            self.full_domain = domain
        self.api_key = api_key

        self.headers = {'X-Auth-Key': self.api_key,'X-Auth-Email': self.email}
        self.api_url = 'https://api.cloudflare.com/client/v4/zones/'
        try:
            self.zone_id = self.getZone()
            self.record_id = self.getRecord('A', self.full_domain)
        except:
            self.logFail()

    def logSuccess(self):
        dateTimeLog = datetime.datetime.now(pytz.timezone('Asia/Bangkok')).strftime(r'[%d/%m/%Y, %H:%M:%S]')
        print(f'{dateTimeLog} Update success {self.public_ip} to {self.domain} ')
        time.sleep(self.interval_time)

    def logFail(self):
        dateTimeLog = datetime.datetime.now(pytz.timezone('Asia/Bangkok')).strftime(r'[%d/%m/%Y, %H:%M:%S]')
        print(f'{dateTimeLog} DDNS Update to {self.domain} Failed')
        time.sleep(self.interval_time)
        sys.exit(0)

    def getPubilcIP(self):
        try:
            public_ip = requests.get('https://api.ipify.org').content.decode('utf8')
            ip_list = public_ip.split('.')
            if len(ip_list) != 4:
                self.logFail()
            for ip in ip_list:
                if not ip.isdigit():
                    self.logFail()
                i = int(ip)
                if i < 0 or i > 255:
                    self.logFail()
            self.public_ip = public_ip
            return public_ip
        except:
            self.logFail()

    def getZone(self):
        response = requests.get(self.api_url, headers=self.headers, json=None)
        if response.status_code == 200:
            domains = (response.json())['result']
            for domain in domains:
                if domain['name'] == self.domain:
                    return domain['id']
        else:
            print('zone id not found')
            sys.exit(0)

    def getRecord(self, dns_type, name):
        url = 'https://api.cloudflare.com/client/v4/zones/' + self.zone_id + '/dns_records'
        response = requests.get(url, headers=self.headers)
        domains = (response.json())['result']
        for domain in domains:
            if domain['name'] == name:
                return domain['id']
        url = 'https://api.cloudflare.com/client/v4/zones/' + self.zone_id + '/dns_records'
        ip = self.getPubilcIP()
        data = {'type': dns_type, 'name': name, 'content': ip, 'ttl': 1, 'proxied': False}
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()['result']['id']

    def updateRecord(self, dns_type, name, content, ttl=1, proxied=False):
        self.record_id = self.getRecord(dns_type, name)
        api_url = self.api_url + self.zone_id + '/dns_records/' + self.record_id
        data = {'type': dns_type, 'name': name, 'content': content, 'ttl': ttl, 'proxied': proxied}
        response = requests.put(api_url, headers=self.headers, json=data)
        self.record_id = (response.json())['result']['id']
        return response

    def run(self):
        while True:
            public_ip = self.getPubilcIP()
            if public_ip != False:
                self.updateRecord('A', self.full_domain, public_ip)
                self.logSuccess()
            else:
                self.logFail()

email = os.environ['email']
domain = os.environ['domain']
api_key = os.environ['api_key']
interval_time = int(os.environ['interval_time'])
if interval_time < 20:
    interval_time = 20
    
cf = Clondflare(email, domain, api_key, interval_time)
cf.run()