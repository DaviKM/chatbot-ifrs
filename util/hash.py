import hashlib

def hash(content: str) -> str:
    hash = content.encode()
    for _ in range(1000):
        hash = hashlib.md5(hash).digest()
        hash = hashlib.sha256(hash).digest()
    return hash.hex()

def verify_hash(content: str, hashed: str) -> bool:
    return hash(content) == hashed

if __name__ == "__main__":
    print(hash("oidavi"))  # Exemplo de uso