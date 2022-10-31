# standard python imports

postgresql = {'host': 'localhost',
         'user': 'lj22',
         'passwd': '123456',
         'db': 'mpesatest'}

postgresqlConfig = "postgresql://{}:{}@{}/{}".format(postgresql['user'], postgresql['passwd'], postgresql['host'], postgresql['db'])
