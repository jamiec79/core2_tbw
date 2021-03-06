from config.config import Config
from flask import Flask, render_template, request
from flask_api import status
from network.network import Network
from util.sql import SnekDB
from util.util import Util

app = Flask(__name__)


@app.route('/')
def index():    
    s = {} 
    dstats = client.delegates.get(data.public_key)

    s['forged'] = dstats['data']['blocks']['produced']
    #s['missed'] = dstats['data']['blocks']['missed']
    s['missed'] = 0 # temp fix
    s['rank'] = dstats['data']['rank']
    #s['productivity'] = dstats['data']['production']['productivity']
    s['productivity'] = 100 # temp fix
    if data.network in ['ark_mainnet', 'ark_devnet']:
        if s['rank'] <= 51:
            s['forging'] = 'Forging'
        else:
            s['forging'] = 'Standby'

    snekdb = SnekDB(data.database_user, data.network, data.delegate)
    voter_data = snekdb.voters().fetchall()
    voter_count = client.delegates.voters(data.delegate)    
    s['votes'] = voter_count['meta']['totalCount']
    
    if data.pool_version == "original":
        return render_template('index.html', node=s, row=voter_data, n=navbar)
    else:
        return render_template('geops_index.html', node=s, row=voter_data, n=navbar)


@app.route('/payments')
def payments():
    snekdb = SnekDB(data.database_user, data.network, data.delegate)
    data_out = snekdb.transactions().fetchall()
    tx_data = []
    for i in data_out:
        data_list = [i[0], int(i[1]), i[2], i[3]]
        tx_data.append(data_list)
    
    if data.pool_version == 'original':
       return render_template('payments.html', row=tx_data, n=navbar)
    else:
       return render_template('geops_payments.html', row=tx_data, n=navbar)
        
'''
@app.route('/webhook', methods=['POST'])
def webhook():
    hook_data = json.loads(request.data)
    authorization = request.headers['Authorization']
    token = authorization+second

    if token == webhookToken:
        # do something with the data like store in database
        block = [[hook_data['data']['id'], hook_data['data']['timestamp'], hook_data['data']['reward'],
                 hook_data['data']['totalFee'], hook_data['data']['height']]]

        # store block to get allocated by tbw
        snekdb = SnekDB(data['dbusername'])
        snekdb.storeBlocks(block)
        return "OK"

    # Token does not match
    return '', status.HTTP_401_UNAUTHORIZED
'''

if __name__ == '__main__':
    data = Config()
    network = Network(data.network)
    u = Util(data.network)
    client = u.get_client(network.api_port)
    navbar = {
       'dname': data.delegate,
       'proposal': data.proposal,
       'explorer': data.explorer,
       'coin': data.coin}
    app.run(host=data.pool_ip, port=data.pool_port)
