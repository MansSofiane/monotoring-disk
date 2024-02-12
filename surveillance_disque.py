import psutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import wmi

import ssl

# Paramètres de configuration
adresse_machine_distante = "127.0.0.1"
utilisateur_windows = "wissalwinkeys@gmail.com"
mot_de_passe_windows = "1962"
limite_taille_disque = 90  # En pourcentage
adresse_email_expediteur = "votre_email@gmail.com"
mot_de_passe_email_expediteur = "votre_mot_de_passe"
adresse_email_destinataire = "email_alerte@example.com"

def obtenir_informations_disque_wmi():
    c = wmi.WMI(computer=adresse_machine_distante, user=utilisateur_windows, password=mot_de_passe_windows)

    disk_info = []
    for disk in c.Win32_LogicalDisk():
        disk_info.append({'DeviceID': disk.DeviceID, 'Size': disk.Size, 'FreeSpace': disk.FreeSpace})

    return disk_info
def surveiller_taille_disque():
    disk_info = obtenir_informations_disque_wmi()

    for disk in disk_info:
        total_space = disk['Size']
        free_space = disk['FreeSpace']
        used_space_percent = ((total_space - free_space) / total_space) * 100

        if used_space_percent > limite_taille_disque:
            envoyer_alerte(disk['DeviceID'], used_space_percent)

def envoyer_alerte(disque, pourcentage_utilise):
    sujet = f"Alerte : La taille du disque {disque} a atteint {pourcentage_utilise}%"
    message = f"La taille du disque {disque} a atteint {pourcentage_utilise}%. Veuillez prendre des mesures."

    # Configurer le serveur SMTP
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(adresse_email_expediteur, mot_de_passe_email_expediteur)

    # Construire le message
    msg = MIMEMultipart()
    msg.attach(MIMEText(message, 'plain'))

    # Envoyer l'e-mail
    server.sendmail(adresse_email_expediteur, adresse_email_destinataire, msg.as_string())

    # Fermer la connexion SMTP
    server.quit()

if __name__ == "__main__":
    surveiller_taille_disque()

"""
limite_taille_disque = 90  # En pourcentage
adresse_email_envoi = "ensofiane65@gmail.com"
mot_de_passe_envoi = "Mansouri$02"
adresse_email_destinataire = "yehiaouifatiha@gmail.com"
serveur_smtp = "smtp.gmail.com"
port_smtp = 587

def surveiller_taille_disque():
    try:
        partitions = psutil.disk_partitions()
        
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            pourcentage_utilise = usage.percent
            
            if pourcentage_utilise < limite_taille_disque:
                envoyer_alerte(partition.device, partition.mountpoint, pourcentage_utilise)
                print("yesss")

    except Exception as e:
        print(f"Erreur lors de la surveillance du disque : {e}")

def envoyer_alerte(device, mountpoint, pourcentage_utilise):
    sujet = f"Alerte : La taille du disque {device} a atteint {pourcentage_utilise}%"
    message = f"La taille du disque {device} ({mountpoint}) a atteint {pourcentage_utilise}%. Date et heure : {datetime.now()}"

    msg = MIMEMultipart()
    msg['From'] = adresse_email_envoi
    msg['To'] = adresse_email_destinataire
    msg['Subject'] = sujet

    msg.attach(MIMEText(message, 'plain'))
    context = ssl.create_default_context()
    with smtplib.SMTP(serveur_smtp, port_smtp) as server:
        server.starttls()
        server.login(adresse_email_envoi, mot_de_passe_envoi)
        server.sendmail(adresse_email_envoi, adresse_email_destinataire, msg.as_string())

if __name__ == "__main__":
    while True:
        surveiller_taille_disque()
        time.sleep(10)  
"""