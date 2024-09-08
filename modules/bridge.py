from web3 import Web3
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class Bridge:
    def __init__(self, private_key, rpc_url, explorer_url, chain_id_from, chain_id_to, from_contract_address, balance):
        self.private_key = private_key
        self.rpc_url = rpc_url
        self.explorer_url = explorer_url
        self.chain_id_from = chain_id_from
        self.chain_id_to = chain_id_to
        self.from_contract_address = from_contract_address
        self.balance = balance
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = self.web3.eth.account.from_key(private_key)

    async def prepare_tx(self, route):
        try:
            # Contoh logika untuk mempersiapkan transaksi
            # Anda mungkin perlu menyesuaikannya dengan kebutuhan spesifik Anda
            nonce = self.web3.eth.get_transaction_count(self.account.address)
            gas_price = self.web3.eth.gas_price
            value = self.balance

            tx = {
                'to': route,
                'value': value,
                'gas': 21000,
                'gasPrice': gas_price,
                'nonce': nonce
            }

            signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            logger.info(f"Transaction sent: {tx_hash.hex()}")

            return tx_hash.hex()

        except Exception as e:
            logger.error(f"Error preparing transaction: {e}")
            raise
