user={
    'name':'cool',
    'birth':'1955-01-01',
    'note':None
}

query=[]
for key, value in user.items():
    if value != None:
        query.append(key + "=" + "'{}".format(value))
query = ",".join(query)

