import paho.mqtt.client as mqtt
import json
import time
import random


ACCESS_TOKEN = "OKF3F2DpazNvWYNmIaul"  


BROKER = "thingsboard.cloud"
PORT = 1883


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(" Connecté à ThingsBoard Cloud")
    else:
        print(" Échec de connexion, code :", rc)
    


def on_message(client, userdata, msg):
    print(" Commande reçue :", msg.payload.decode())
    

    try:
        commande = json.loads(msg.payload.decode())
        methode = commande.get("method")
        params = commande.get("params")

        
        if methode == "led":
            if params == "on":
                print("LED = ON (simulé)")
            elif params == "off":
                print("LED = OFF (simulé)")
        elif methode == "mode":
            print(f"Mode changé à : {params} (simulé)")

        
        response_topic = msg.topic.replace("request", "response")
        client.publish(response_topic, json.dumps({"status": "executed"}))
    except Exception as e:
        print(" Erreur lors du traitement de la commande :", e)


client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)  
client.on_connect = on_connect
client.on_message = on_message


client.connect(BROKER, PORT, 60)


client.subscribe("v1/devices/me/rpc/request/+")


client.loop_start()


try:
    while True:
        telemetry = {
            "temperature": round(20 + random.uniform(-5, 5), 2),
            "humidity": round(50 + random.uniform(-10, 10), 2)
        }
        client.publish("v1/devices/me/telemetry", json.dumps(telemetry))
        print(" Données envoyées :", telemetry)
        time.sleep(5)

except KeyboardInterrupt:
    print("\n Arrêt du simulateur.")
    client.loop_stop()
    client.disconnect()
