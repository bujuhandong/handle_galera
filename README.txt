# MySQL galera �ڵ���ӡ��ڵ�ɾ����MGR״̬��顢���ݿ���ͣ����
��������handle_galera

### ����ṹ��
```
handle_galera/
|-- bin/
|   |-- __init__.py
|   |-- handle_galera.py
|
|-- core/
|   |-- __init__.py
|   |-- main.py  
|-- conf/
|   |-- galera.conf   ##handle_galera�����ļ�
|   |-- example_galera.conf  ##�ο������ļ�
|-- README

```

### ���л�����
    Python3.0�����ϰ汾�������ɡ�


### ִ�з�����
    python3 handle_galera.py
	
### ʹ�÷�����
    1) �༭�����ļ�conf/galera.conf������Ϊ�����ļ���������:
	  ####[default]������ڣ���MySQL��һЩ�����Ϣ������defaults-file��datadir��basedir��
	  ####user��password��socket��������
      ####�û����Ը���ʵ��������ġ�����datadir��������ǰ�Ѵ��ڡ�
      [default]
      defaults-file = /57data/galera_my/my.cnf
      datadir = /57data/galera_my
      basedir = /usr/local/mysql215
      user = root
      password = mysql
      socket = /tmp/mysql3307.sock
      
      
      ###########����ΪMySQL�����ļ�����Ҫ�������##############
      [client]
      default-character-set = utf8
      port = 3307
      
      [mysql]
      default-character-set = utf8
      
      
      [mysqld]
      basedir = /usr/local/mysql215
      datadir = /57data/galera_my
      socket = /tmp/mysql3307.sock
      user = mysql
      character-set-server = utf8
      collation-server = utf8_general_ci
      port = 3307
      server-id = 3
      
      
      binlog_format=ROW
      default_storage_engine=innodb
      innodb_autoinc_lock_mode=2
      innodb_flush_log_at_trx_commit=0
      innodb_buffer_pool_size=122M
      
      #########����wsrep_��ͷ����Ϊgalera���������Ϣ#######################
      wsrep_provider=/usr/local/mysql215/lib/plugin/libgalera_smm.so
      wsrep_provider_options="gcache.size=300M; gcache.page_size=300M"
      wsrep_cluster_name="example_cluster"
      wsrep_cluster_address="gcomm://10.0.0.13"
      
      ##########����wsrep_sst_��ͷ������[sst]����Ϊ����½ڵ��Ǳ�����ڵ���Ϣ##################
      wsrep_sst_method=xtrabackup
      wsrep_sst_donor = vm3
      wsrep_sst_auth = sstuser:mysql
      
      [sst]
      streamfmt=xbstream
      
	  
    2) ����ϵͳ��ʾ������Ҫ�Ĳ������͡�
	    1:'Check the galera status',
        2:'Add new galera node',
        3:'Delete galera node',
        4:'Start MySQL instance',
        5:'Stop MySQL instance',
        6:'Exit'

