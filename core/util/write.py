import os
import json
from Naked.toolshed.shell import muterun_js

class JsWrite:
    
    def __init__(self):
        pass
    
    def write(self, network, passphrase, secondphrase, publickey, recipientid, nonce, vendor, amount, fee):
        f = open("tx.js", "w")
        f.writelines("const fs = require('fs')\n")
        f.writelines("const { Transactions, Managers } = require('@arkecosystem/crypto');\n")
        f.writelines("Managers.configManager.getMilestone().aip11 = true\n")
        f.writelines("Managers.configManager.config.network.pubKeyHash = "+network+";\n")
        f.writelines("var tx = Transactions.BuilderFactory.transfer().network("+network+").nonce("+nonce+").senderPublicKey('"+publickey+"').recipientId('"+recipientid+"').fee("+fee+").amount("+amount+").expiration(0).vendorField('"+vendor+"')\n")
        f.writelines("tx.sign('"+passphrase+"');\n")
        if secondphrase is not None:
            f.writelines("    tx.secondSign('"+secondphrase+"');\n")
        f.writelines("var jsonData = tx.build().toJson()\n")
        f.writelines("console.log(JSON.stringify(jsonData));\n")
        #f.writelines("var jsonContent = JSON.stringify(jsonData);\n")
        #f.writelines("fs.writeFile('output.json', jsonContent, 'utf8', function (err) {\n")
        #f.writelines("    if (err) {\n")
        #f.writelines(" console.log('An error occured while writing JSON Object to File.');\n")
        #f.writelines(" return console.log(err);\n")
        #f.writelines("    }\n")
        #f.writelines("});\n")
        f.close()
        
    
    def run(self):
        '''execute_js('tx.js')
        filename = 'output.json'

        if filename:
            with open(filename, 'r') as f:
                datastore = json.load(f)
        return datastore
        '''
        response = muterun_js('tx.js')
        if response.exitcode == 0:
            os.remove('tx.js')
            return json.loads(response.stdout.decode('utf-8'))
        else:
            sys.stderr.write(response.stderr.decode('utf-8'))  
            
                
    #def delete(self):
    #    os.remove('output.json')
    #    os.remove('tx.js')
