#!/usr/bin/python

import os
import sys
import string

class ApacheConfig:
    """Implements the whole configuration of Apache server"""
    
    def __init__(self, conf_dir):
        self.conf_dir = conf_dir
        self.conf_list = os.listdir(self.conf_dir)
        self.confs = self.get_confs()
        self.domains = self.get_domains()
        self.conf_number = len(self.confs)
        
    def get_confs(self):
        """return a dictionnary describing all the Apache domains"""
        confs = []
        for conf in self.conf_list:
            c = ApacheVitualHost(self.conf_dir+os.sep+conf)
            conf_dict = {}
            conf_dict['domain'] = c.domain
            conf_dict['conf'] = c.conf
            confs.append(conf_dict)
        return confs

    def get_domains(self):
        domains = []
        for conf in self.confs:
            if conf['domain']:
                domains.append(conf['domain'])
        return domains
        
            #if 'ServerName' in conf:
                #domain = conf['ServerName']
            #else:
                #domain = 'unknown'
            #if domain and not 'stats' in domain:
                #domains.append(domain)
 
    def get_param(self, param):
        pass

    def get_custom_logs(self):
        logs = {}
        for conf in self.confs:
            if conf['conf']['CustomLog']:
                logs[conf['domain']] = conf['conf']['CustomLog']
        return logs


class ApacheVitualHost:
    """Implements an Apache virtualhost"""
    
    def __init__(self, conf_file):
        self.conf_file = conf_file
        self.conf = self.get_conf()
        self.domain = self.get_domain()
        
    def get_conf(self):
        """return a dictionnary describing the Apache virtualhost"""
        conf_file = open(self.conf_file)
        conf = conf_file.readlines()
        conf_dict = {}
        for line in conf:
            line = line.strip()
            if line:
                if line[0] != '<' and line[0] != '#':
                    #print line
                    param = line.split(' ')
                    param = [w for w in param if len(w) > 0]
                    #print param
                    if len(param) > 1:
                        conf_dict[param[0]] = param[1]
        #print conf_dict
        return conf_dict
        conf_file.close()

    def get_domain(self):
        if 'ServerName' in self.conf:
            domain = self.conf['ServerName']
        else:
            domain = 'unknown'
        if domain:
            return domain


class AwstatsConfig:
    """Implements the whole configuration of Awstats system"""
    
    def __init__(self, conf_dir):
        self.conf_dir = conf_dir
        self.conf_list = os.listdir(self.conf_dir)
        self.confs = self.get_confs()
        self.domains = self.get_domains()
        self.conf_number = len(self.confs)
        self.default_conf = 'awstats_default.conf'
        
    def get_confs(self):
        """return a dictionnary describing all the Awstats domains"""
        confs = []
        for conf in self.conf_list:
            c = AwstatsDomain(self.conf_dir+os.sep+conf)
            conf_dict = {}
            conf_dict['domain'] = c.domain
            conf_dict['conf'] = c.conf
            confs.append(conf_dict)
        return confs
    
    def get_domains(self):
        domains = []
        for conf in self.confs:
            if conf['domain']:
                domains.append(conf['domain'])
        return domains
            
    def get_custom_logs(self):
        """return a dictionnary of all the custom log files"""
        logs = {}
        for conf in self.confs:
            if conf['conf']:
                if conf['conf']['LogFile']:
                    logs[conf['domain']] = conf['conf']['LogFile']
        return logs


class AwstatsDomain:
    """Implements an Awstasts domain"""
    def __init__(self, conf_file):
        self.conf_file = conf_file
        self.conf = self.get_conf()
        self.domain = self.get_domain()
        
    def get_conf(self):
        """return a dictionnary describing the Awstats domain"""
        conf_file = open(self.conf_file)
        conf = conf_file.readlines()
        conf_dict = {}
        for line in conf:
            line = line.strip()
            if line:
                if line[0] != '<' and line[0] != '#':
                    #print line
                    param = line.split('=')
                    param = [w for w in param if len(w) > 0]
                    #print param
                    if len(param) > 1:
                        conf_dict[param[0]] = param[1].replace('"','').replace('\t','').strip()
        #print conf_dict
        return conf_dict
        conf_file.close()

    def get_domain(self):
        if 'SiteDomain' in self.conf:
            domain = self.conf['SiteDomain']
        else:
            domain = ''
        if domain:
            return domain

    def set_conf(self):
       pass

    def get_apache_conf(self):
        return """ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
        <Directory "/usr/lib/cgi-bin">
            AllowOverride All
            Options ExecCGI -MultiViews +SymLinksIfOwnerMatch
            Order allow,deny
            Allow from all
        </Directory>

        Alias /awstats-icon/ "/usr/share/awstats/icon/"
        <Directory /usr/share/awstats/icon>
            AllowOverride None
            Options None
            Order allow,deny
            Allow from all
        </Directory>
        """

def main():
    a = ApacheConfig('/etc/apache2/sites-available/')
    w = AwstatsConfig('/etc/awstats/')

    print a.get_domains()
    print a.get_custom_logs()

    #print w.get_confs()
    print w.get_domains()
    print w.get_custom_logs()
    print         

if __name__ == '__main__':
    main()

