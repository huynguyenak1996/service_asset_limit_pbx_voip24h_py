import pymongo

def config_mongodb(config):
    array = {}
    if config.get('hostname'):
        array['hostname'] = config['hostname']
    if config.get('port'):
        array['port'] = config['port']
    if config.get('database'):
        array['database'] = config['database']
    return array
def connect_to_mongo(config):
    if config.get('hostname'):
        hostname = config.get('hostname')
        port = config.get('port') if config.get('port') else '27017'
        database = config.get('database') if config.get('database') else 'admin'
        client = pymongo.MongoClient(f"mongodb://{hostname}:{port}/")
        database = client[database]
        return database
    else:
        return "không tìm thấy hostname"

