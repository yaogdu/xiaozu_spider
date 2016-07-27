DB={'address':'127.0.0.1:27017','db':'douban','col':'posts','replicaSet':'dmmongo'}

skip = [',','.',':',';','<','>','/','&','#']

url = 'https://www.douban.com/group/fangzi/discussion?start=100'
print url.split('=').pop(0)