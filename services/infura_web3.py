import asyncio
import json
import os
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import geth_poa_middleware
import asyncio

load_dotenv()


class Web3Service:

    def __init__(self, device_service):
        self.infura_url = os.getenv("INFURA_URL")
        self.from_account = os.getenv("FROM_ACCOUNT")
        self.private_key = os.getenv("PRIVATE_KEY")
        self.master_address = os.getenv("MASTER_CONTRACT_ADDRESS")
        self.web3 = Web3(Web3.HTTPProvider(self.infura_url))
        abi = open('abi.json')
        self.master_contract_abi = json.load(abi)["abi"]
        self.device_service = device_service
        asyncio.create_task(self.get_event())
        print("Hello world")

    def create_master_contract(self):
        nonce = self.web3.eth.getTransactionCount(self.from_account)
        tx = {
            'type': '0x2',
            'nonce': nonce,
            'from': self.from_account,
            'to': '',
            'value': self.web3.toWei(0.01, 'ether'),
            'maxFeePerGas': self.web3.toWei('250', 'gwei'),
            'maxPriorityFeePerGas': self.web3.toWei('3', 'gwei'),
            'chainId': 3
        }

        gas = self.web3.eth.estimateGas(tx)
        tx['gas'] = gas
        signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print("Transaction hash: " + str(self.web3.toHex(tx_hash)))

    def create_digital_twin(self, device_id, public_key):
        contract_reference = self.web3.eth.contract(address=self.master_address, abi=self.master_contract_abi)
        device_id_bytes = Web3.to_bytes(bytes(device_id, 'utf-8'))
        print(device_id_bytes)
        public_key_bytes = Web3.to_bytes(bytes(str(public_key), 'utf-8'))
        print(public_key_bytes)
        contract_reference_transaction = contract_reference.functions.createDeviceDigitalTwin(device_id_bytes,
                                                                                              public_key_bytes)
        contract_reference_transaction = contract_reference_transaction.build_transaction(
            {
                'from': self.from_account,
                'nonce': self.web3.eth.get_transaction_count(self.from_account),
            }
        )
        tx_create = self.web3.eth.account.sign_transaction(contract_reference_transaction, self.private_key)

        tx_hash = self.web3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

        return tx_receipt.transactionHash.hex()

    def create_transaction(self, address, signature, data):
        contract_reference = self.web3.eth.contract(address=self.master_address, abi=self.master_contract_abi)
        signature_bytes = Web3.to_bytes(bytes(signature, 'utf-8'))
        data_bytes = Web3.to_bytes(bytes(data, 'utf-8'))
        contract_reference_transaction = contract_reference.functions.createTransaction(address, signature_bytes,
                                                                                        data_bytes)
        contract_reference_transaction = contract_reference_transaction.build_transaction(
            {
                'from': self.from_account,
                'nonce': self.web3.eth.get_transaction_count(self.from_account),
            }
        )
        tx_create = self.web3.eth.account.sign_transaction(contract_reference_transaction, self.private_key)

        tx_hash = self.web3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

        return tx_receipt.transactionHash.hex()

    async def get_event(self):
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        contract = self.web3.eth.contract(address=self.master_address, abi=self.master_contract_abi)

        try:
            event_filter = contract.events.DigitalTwinCreated.create_filter(fromBlock="0x0")
            while True:
                for event in event_filter.get_new_entries():
                    print("Event received")
                    twin_info = event.args.twinInfo
                    self.device_service.join_digital_twin(twin_info.deviceId, twin_info.deviceAddress)
                await asyncio.sleep(1)

        except Exception as e:
            print(e)
