import os,re,paramiko,datetime,socket

class DBackper(object):

    def __init__(self,conf='db.conf'):
        self.conflist=[]
        for line in open(conf,'r').readlines():
            hostid=open(conf,'r').readlines().index(line)
            line = line.strip()
            if line.startswith("#"):
                #Bypass note line.
                continue
            else:
                item = re.split('\:|\@|\,', line)
                item.append(hostid)
                self.conflist.append(item)

    def initremotedir(self,backupurl,hostid):
        self.backupurl = backupurl
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try :
            self.ssh.connect(hostname=hostname, username=username, password=password,timeout=2)
            stdin, stdout, stderr = self.ssh.exec_command("ls -l " + backupurl)
            print('HostID: ' + str(hostid+1) +' Checking remote backup list......', end='')
            if "No such file or directory" in str(stderr.readlines()):
                self.ssh.exec_command("mkdir " + backupurl)
                print('Not Existed. Created it.')
            elif "total" in str(stdout.readlines()):
                print('Existed.')
        except paramiko.ssh_exception.AuthenticationException:
            print('HostID: ' + str(hostid + 1) +" \"" + hostname + '"  Authentication failed.')
            self.ssh.close()
            print('HostID: ' + str(hostid + 1) + " \"" + hostname + '"  connection closed.')
            raise Exception

        except socket.error:
            print('HostID: ' + str(hostid + 1) +" \"" + hostname + '"  Time out error.')

    def Backuper(self,hostname,dbhostname,dbpassword,dbname,type=1):
        self.hostname=hostname
        if type == 1:
            type='AutoBackup'
        else:
            type='ManualBackup'
        self.filname = datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S_%f-")+type+".sql"
        try:
            stdin, stdout, stderr = self.ssh.exec_command("mysqldump -u"+dbusername+" -h"+dbhostname+" -p"+dbpassword+" --databases "+dbname+" >"+self.backupurl+self.filname)
            error=stderr.readlines()
            if error.__len__() >0:
                for error in error:
                    print('HostID: ' +str(hostid+1)+" "+error.strip())
                    raise ConnectionError
            else:
                print('HostID: ' + str(hostid+1) + ' \"' +hostname+'\", Database: \"'+dbname+'\", File: '+self.filname+', Backup Done!')
        except AttributeError:
            pass


    def initlocaldir(self):
        if os.path.exists("./"+localurl+'/'+self.hostname.replace('.','_')+"/") == False:
            os.makedirs("./"+localurl+'/'+self.hostname.replace('.','_')+"/")

    def Getfile(self,localurl):
        try :
            self.sftp = self.ssh.open_sftp()
            self.sftp.get(self.backupurl+self.filname,localurl+'/'+self.hostname.replace('.','_')+"/"+self.filname)
            self.ssh.close()
            print('HostID: ' + str(hostid+1) + ' Backup to '+localurl+'/'+self.hostname.replace('.','_')+"/"+self.filname)
        except AttributeError:
            pass

if __name__ == '__main__':

    MyDBackper=DBackper()
    for instance in MyDBackper.conflist:
        if instance.__len__() != 10:
            #Bypass blank line
            continue
        username = instance[0]
        password = instance[1]
        hostname = instance[2]
        dbusername =  instance[3]
        dbpassword =  instance[4]
        dbhostname=  instance[5]
        dbname=  instance[6]
        backupurl=  instance[7]
        localurl=  instance[8]
        hostid =  instance[9]
        try:
            MyDBackper.initremotedir(backupurl, hostid)
        except Exception:
            continue
        try:
            MyDBackper.Backuper(hostname=hostname,dbhostname=dbhostname,dbpassword=dbpassword,dbname=dbname)
        except ConnectionError:
            continue
        MyDBackper.initlocaldir()
        MyDBackper.Getfile(localurl=localurl)
