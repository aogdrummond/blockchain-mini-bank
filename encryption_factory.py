import json
from hashlib import sha256
from typing import Any, Dict, List, Tuple
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


class Encryption:
    def create_keys_pair(self) -> Tuple[str, str]:
        """Generate a pair of RSA public and private keys.

        Returns:
            A tuple containing the public and private keys as strings.
        """
        def clean_key(key_string: str) -> str:
            return key_string.replace("'", "")

        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

        encrypted_pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        pem_public_key = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        public_key = clean_key(pem_public_key.decode("utf-8"))
        private_key = clean_key(encrypted_pem_private_key.decode("utf-8"))

        return public_key, private_key

    def encrypt_transaction(
        self, data: Dict[str, str], previous_hash: str, keys: Dict[str, str]
    ) -> Tuple[str, str]:
        """Encrypt a transaction using the given data, previous hash, and keys.

        Args:
            data: A dictionary containing the transaction data.
            previous_hash: The hash of the previous block in the chain.
            keys: A dictionary containing the public and private keys as strings.

        Returns:
            A tuple containing the hash value and proof of work as strings.
        """
        timestamp = data["date"]
        message = json.dumps(data)
        signature = sha256((keys["private"] + message).encode()).hexdigest()
        payload = {
            "transaction": message,
            "signature": signature,
            "public_key": keys["public"],
        }
        new_proof = 1
        block = self.assemble_block(payload, timestamp, previous_hash, new_proof)
        hash_value = sha256(json.dumps(block).encode()).hexdigest()

        print("Mining a solution for your message.")
        while not any(
            substring in hash_value for substring in ["012", "123", "abc", "xyz", "987", "456"]
        ):
            print(f"Testing proof {new_proof}")
            new_proof += 1
            block["proof"] = str(self.digest_proof(block, new_proof))
            hash_value = sha256(json.dumps(block).encode()).hexdigest()
            if new_proof == 30:
                raise MemoryError

        print("Solution found.")

        return hash_value, block["proof"]

    def assemble_block(
        self, payload: Dict[str, str], timestamp: str, previous_hash: str, proof: int
    ) -> Dict[str, str]:
        """Assemble a block using the given payload, timestamp, previous hash, and proof.

        Args:
            payload: A dictionary containing the payload data.
            timestamp: The timestamp of the block.
            previous_hash: The hash of the previous block in the chain.
            proof: The proof of work for the block.

        Returns:
            A dictionary containing the assembled block data.
        """
        block = {
            "message": payload,
            "timestamp": timestamp,
            "previous_hash": previous_hash,
            "proof": str(proof),
        }

        return block

    def digest_proof(self, block: Dict[str, Any], new_proof: int) -> int:
        """Computes a new digest based on the block's proof and the new proof.
        
        Args:
            block: The block from which to get the current proof.
            new_proof: The new proof to use in the computation.
        
        Returns:
            The new digest as an integer.
        """
        return int(str(new_proof*2 - int(block["proof"])*2))
    
    def recreate_chain_hashes(self, data: List[Tuple[Any, ...]], keys: Dict[str, str]) -> List[str]:
        """Recreates the hashes for the blockchain using the provided data and keys.
        
        Args:
            data: The transaction data to use in recreating the blockchain hashes.
            keys: The public and private keys to use in signing the transactions.
        
        Returns:
            The recreated blockchain hashes as a list of strings.
        """
        blockchain_hashes = []
        for idx, transaction in enumerate(data):
            if idx == 0:
                previous_hash = "0"
            else:
                previous_hash = data[idx-1][-2]
            timestamp = transaction[3].strftime("%Y-%m-%d %H:%M:%S")
            payload = {"value":transaction[2],"date":timestamp,"id":transaction[1]}
            proof = transaction[-1]
            message = json.dumps(payload)
            signature = sha256(keys["private"].encode()+message.encode()).hexdigest()
            payload = {"transaction":message,"signature":signature,"public_key":keys["public"]}
            block = self.assemble_block(payload,timestamp,previous_hash,proof)      
            hash = sha256(json.dumps(block).encode()).hexdigest()
            blockchain_hashes.append(hash)
        
        return blockchain_hashes
