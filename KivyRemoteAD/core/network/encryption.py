from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import os

class EncryptionManager:
    def __init__(self):
        self.aes_key = None
        self.aes_iv = None
        self.rsa_key = None
        self.remote_public_key = None
        
    def generate_rsa_key(self, key_size=2048):
        """生成RSA密钥对"""
        self.rsa_key = RSA.generate(key_size)
        return self.rsa_key
        
    def get_public_key(self):
        """获取RSA公钥"""
        if not self.rsa_key:
            self.generate_rsa_key()
        return self.rsa_key.publickey().export_key()
        
    def set_remote_public_key(self, public_key):
        """设置远程设备的RSA公钥"""
        self.remote_public_key = RSA.import_key(public_key)
        
    def generate_aes_key(self):
        """生成AES密钥和IV"""
        self.aes_key = get_random_bytes(32)  # AES-256
        self.aes_iv = get_random_bytes(16)   # AES block size
        return self.aes_key, self.aes_iv
        
    def encrypt_aes_key(self):
        """使用RSA公钥加密AES密钥和IV"""
        if not self.remote_public_key or not self.aes_key or not self.aes_iv:
            raise ValueError("Remote public key or AES key not set")
        
        cipher_rsa = PKCS1_OAEP.new(self.remote_public_key)
        encrypted_data = cipher_rsa.encrypt(self.aes_key + self.aes_iv)
        return encrypted_data
        
    def decrypt_aes_key(self, encrypted_data):
        """使用RSA私钥解密AES密钥和IV"""
        if not self.rsa_key:
            raise ValueError("RSA key not generated")
        
        cipher_rsa = PKCS1_OAEP.new(self.rsa_key)
        decrypted_data = cipher_rsa.decrypt(encrypted_data)
        self.aes_key = decrypted_data[:32]
        self.aes_iv = decrypted_data[32:]
        return self.aes_key, self.aes_iv
        
    def encrypt(self, data):
        """使用AES加密数据"""
        if not self.aes_key or not self.aes_iv:
            raise ValueError("AES key or IV not set")
        
        cipher_aes = AES.new(self.aes_key, AES.MODE_CBC, self.aes_iv)
        padded_data = pad(data, AES.block_size)
        encrypted_data = cipher_aes.encrypt(padded_data)
        return encrypted_data
        
    def decrypt(self, encrypted_data):
        """使用AES解密数据"""
        if not self.aes_key or not self.aes_iv:
            raise ValueError("AES key or IV not set")
        
        cipher_aes = AES.new(self.aes_key, AES.MODE_CBC, self.aes_iv)
        decrypted_data = cipher_aes.decrypt(encrypted_data)
        unpadded_data = unpad(decrypted_data, AES.block_size)
        return unpadded_data
        
    def encrypt_string(self, text):
        """加密字符串"""
        data = text.encode('utf-8')
        encrypted_data = self.encrypt(data)
        return base64.b64encode(encrypted_data).decode('utf-8')
        
    def decrypt_string(self, encrypted_text):
        """解密字符串"""
        encrypted_data = base64.b64decode(encrypted_text.encode('utf-8'))
        decrypted_data = self.decrypt(encrypted_data)
        return decrypted_data.decode('utf-8')
        
    def generate_pairing_code(self, length=6):
        """生成随机配对码"""
        import string
        import random
        chars = string.digits
        return ''.join(random.choice(chars) for _ in range(length))
        
    def save_rsa_key(self, file_path):
        """保存RSA密钥到文件"""
        if not self.rsa_key:
            self.generate_rsa_key()
        with open(file_path, 'wb') as f:
            f.write(self.rsa_key.export_key())
        
    def load_rsa_key(self, file_path):
        """从文件加载RSA密钥"""
        with open(file_path, 'rb') as f:
            self.rsa_key = RSA.import_key(f.read())
        return self.rsa_key

# 单例模式
encryption_manager = EncryptionManager()
