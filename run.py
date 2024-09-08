import asyncio
import logging

from modules.helper import get_random_network_data_new, get_balance
from modules.bridge import Bridge
from constans import NETWORK_CONFIG, PRIVATE_KEYS_PATH
from modules.helper import load_private_key_from_file

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_bridge(private_key):
    try:
        # Mendapatkan data jaringan acak
        random_data = get_random_network_data_new(NETWORK_CONFIG)
        if not random_data:
            raise ValueError("Gagal mendapatkan data jaringan acak.")

        # Mengambil saldo dan memastikan bahwa saldo valid
        balance = get_balance(random_data["rpc_url"], private_key)
        if balance is None:
            raise ValueError("Gagal mendapatkan saldo.")

        # Membuat instance Bridge dengan parameter yang diperlukan
        bridge = Bridge(
            private_key,
            random_data["rpc_url"],
            random_data["explorer_url"],
            random_data["chain_identifier_from"],
            random_data["chain_identifier_to"],
            random_data["from_contract_address"],
            balance
        )

        # Mempersiapkan transaksi
        await bridge.prepare_tx(route=random_data["to_contract_address"])
    except ValueError as e:
        logger.error(f"Kesalahan nilai: {e}")
    except AttributeError as e:
        logger.error(f"Kesalahan atribut: {e}")
    except Exception as e:
        logger.error(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    private_key = load_private_key_from_file(PRIVATE_KEYS_PATH)

    try:
        asyncio.run(start_bridge(private_key))
    except RuntimeError as e:
        logger.error(f"Kesalahan runtime: {e}")
    except Exception as e:
        logger.error(f"Terjadi kesalahan: {e}")
