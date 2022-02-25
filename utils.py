from web3 import Web3
import json, datetime

now = datetime.datetime.now()

def log(whatever: str):
    with open("faucet_log.csv","a+") as f:
        f.write(f"{whatever}\n")

def check_wallet(wallet):
    if Web3.isAddress(wallet):
        return True
    else:
        return None
        
def send_fweb3(amount, sender_public_key, sender_private_key, receiver):

    RPC = "https://polygon-mainnet.g.alchemy.com/v2/iS4IWtq7YDL6J5MWwPOK_KyfLKEs4vwc"
    chain_Id = 137
    web3 = Web3(Web3.HTTPProvider(RPC))
    print(f"* {receiver} requested some $FWEB3")

    try:
        with open('fweb3_abi.json') as json_file:
            abi = json.load(json_file)

        receiver = web3.toChecksumAddress(receiver)
        contract = web3.eth.contract(address=web3.toChecksumAddress("0x4a14AC36667B574B08443a15093e417dB909D7a3"), abi=abi)
        amount = web3.toWei(amount, 'ether')
        nonce = web3.eth.getTransactionCount(sender_public_key)
        token_tx = contract.functions.transfer(receiver, amount).buildTransaction({'chainId':chain_Id, 'gas': 100000,'gasPrice': web3.eth.gas_price, 'nonce':nonce})
        sign_txn = web3.eth.account.signTransaction(token_tx, private_key=sender_private_key)
        raw_tx = web3.eth.sendRawTransaction(sign_txn.rawTransaction)
        tx_hash = web3.toHex(raw_tx)
        return tx_hash
        
        log(f"{now.strftime('%Y-%m-%d %H:%M:%S')};{receiver}")
        
    except Exception as e:
        print(e)
        log(f"{now.strftime('%Y-%m-%d %H:%M:%S')};{e}")
        pass

# disabled (needs some work but i'm too lazy...)        
def check_balance(wallet):

    RPC = "https://polygon-mainnet.g.alchemy.com/v2/iS4IWtq7YDL6J5MWwPOK_KyfLKEs4vwc"
    chain_Id = 137
    web3 = Web3(Web3.HTTPProvider(RPC))

    try:
        with open('fweb3_abi.json') as json_file:
            abi = json.load(json_file)
    
        wallet = web3.toChecksumAddress(wallet)
        contract = web3.eth.contract(address=web3.toChecksumAddress("0x4a14AC36667B574B08443a15093e417dB909D7a3"), abi=abi)
        matic_balance = web3.eth.get_balance(wallet)
        fweb3_balance = contract.functions.balanceOf(wallet).call()
        return fweb3_balance, matic_balance
        
    except Exception as e:
        print(e)
        log(f"{now.strftime('%Y-%m-%d %H:%M:%S')};{e}")
        pass
        

if __name__ == "__main__":
    print("this was intended to be used as a module, exiting...")
    exit()