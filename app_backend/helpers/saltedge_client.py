import OpenSSL.crypto as crypto
import requests
import base64
import time
import os


class SaltEdge:
    digest = "sha256"

    @classmethod
    def verify(cls, path_to_public_key, message, signature):
        """
        Verifies the signature on a message.
        :param path_to_public_key: string, Absolute or relative path to Spectre public key
        :param message: string, The message to verify.
        :param signature: string, The signature on the message.
        :return:
        """
        x509 = crypto.X509()
        with open(path_to_public_key, 'r') as public_key_data:
            public_key = crypto.load_publickey(crypto.FILETYPE_PEM, public_key_data)
        x509.set_pubkey(public_key)

        try:
            crypto.verify(x509, base64.b64decode(signature), message, cls.digest)
            return True
        except crypto.Error:
            return False

    def __init__(self, app_id, secret, private_path):
        self.app_id = app_id
        self.secret = secret

        with open(private_path, "rb") as private_key:
            keydata = private_key.read()

        self._private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, keydata)

    def sign(self, message):
        """
        Signs a message.
        :param message: string, Message to be signed.
        :return: string, The signature of the message for the given key.
          """
        return base64.b64encode(crypto.sign(self._private_key, message, self.digest))

    def generate_signature(self, method, expire, url, payload=""):
        """
        Generates base64 encoded SHA256 signature of the string given params, signed with the client's private key.
        :param method: uppercase method of the HTTP request. Example: GET, POST, PATCH, PUT, DELETE, etc.;
        :param expire: request expiration time as a UNIX timestamp in UTC timezone. Recommended value is 1 minute from now. The maximum value is 1 hour from now.
        :param url: the full requested URL, with all its complementary parameters;
        :param payload: the request post body. Should be left empty if it is a GET request, or the body is empty;
        :return: base64 encoded SHA1 signature
        """
        message = "{expire}|{method}|{url}|{payload}".format(**locals())
        return self.sign(message)

    def generate_headers(self, expire=None):
        if not expire:
            expire = self.expires_at()
        return {
            'Accept': 'application/json',
            'Content-type': 'application/json',
            'Expires-at': expire,
            'App-id': self.app_id,
            'Secret': self.secret
        }

    def expires_at(self):
        return str(time.time() + 500)

    def get(self, url):
        expire = self.expires_at()
        headers = self.generate_headers(expire)
        headers['Signature'] = self.generate_signature("GET", expire, url)
        return requests.get(url, headers=headers)

    def post(self, url, payload, headers=None):
        if not headers:
            expire = self.expires_at()
            headers = self.generate_headers(expire)
        expire = headers['Expires-at']
        headers['Signature'] = self.generate_signature("POST", expire, url, payload)
        return requests.post(url, data=payload, headers=headers)

    def put(self, url, payload):
        expire = self.expires_at()
        headers = self.generate_headers(expire)
        headers['Signature'] = self.generate_signature("POST", expire, url, payload)
        return requests.put(url, data=payload, headers=headers)

    def delete(self, url, payload):
        expire = self.expires_at()
        headers = self.generate_headers(expire)
        headers['Signature'] = self.generate_signature("DELETE", expire, url, payload)
        return requests.delete(url, data=payload, headers=headers)


def initiate_saltedge_client():
    saltedge_client = SaltEdge(
        app_id=os.environ.get("APP_ID"),
        secret=os.environ.get("SECRET"),
        private_path=os.environ.get("PRIVATE_SE_PEM_FILE_PATH"),
    )
    return saltedge_client