# Database Remote Backup Script.

### Example configuration usage:
```shell
# DBackuper
A MySql batch Backuper server.
#username:password@hostname,dbusername,dbpassword,dbhostname,dbname,backupurl,localurl
#username: Remote server SSH username.
#password: Remote server SSH password.
#hostname: Remote server ip or hostname.
#dbusername: Remote server MySql username.
#dbpassword: Remote server MySql password.
#dbhostname: Which ip or hostname can be access on remote access for MySql.
#dbname:  Which db you want to backup?
#backupurl: Remote server local backup url.
#localurl: Backup Server local store to?
#Items must be 9 element, other will be ignore.
#
```
