import paho.mqtt.client as paho
import ssl

AWS_HOST = "a25kfjnhv6wcrv-ats.iot.us-east-1.amazonaws.com"
AWS_PORT = 8883
CA_PATH = "./CertificadosPlanta/ca.crt"
CERT_PATH = "./CertificadosPlanta/certificate.pem.crt"
KEY_PATH = "./CertificadosPlanta/private.pem.key"

#create an encryption key
from cryptography.fernet import Fernet
KEY_CYPHER = Fernet.generate_key()
CIPHER = Fernet(KEY_CYPHER)


def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("monitoramentoPlanta/umidade")
    client.subscribe("monitoramentoPlanta/temperatura")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    #The message to be encrypted must be in bytes
    mesg = b'msg'
    encrypted_msg = CIPHER.encrypt(mesg)
    
    if msg.payload == encrypted_msg:
        print("Mensagem publicada e recebida são as mesmas")
    #convert the decrypted byte message to a UTF-8 string as normal
    decrypted_msg = CIPHER.decrypt(msg.payload)
    print("Mensagem recebida", str(decrypted_msg.decode("utf-8"))



client = paho.Client()
client.on_connect = on_connect
client.on_message = on_message
#create a UTF-8 encoded string to pass as the message payload to the MQTT publish method
out_msg = encrypted_msg.decode()


#ciphers: a string specifying which encryption ciphers are allowable for this connection, or None to use the defaults.
client.tls_set(CA_PATH, 
               certfile = CERT_PATH,
               keyfile = KEY_PATH,
               cert_reqs = ssl.CERT_REQUIRED,
               tls_version = ssl.PROTOCOL_TLSv1_2,
               ciphers = encrypted_msg)

client.connect(AWS_HOST, AWS_PORT, keepalive=60)
client.loop_forever()

