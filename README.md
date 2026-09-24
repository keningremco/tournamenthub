# TournamentHub Service

Deze README beschrijft hoe TournamentHub als een **systemd-service** draait.

Wanneer de service is ingeschakeld:

* ✅ Start TournamentHub automatisch na een reboot.
* ✅ Herstart TournamentHub automatisch wanneer de applicatie crasht.
* ✅ Draait de website op de achtergrond.
* ✅ Kan eenvoudig beheerd worden met `systemctl`.

Daarnaast kan de **TournamentHub Updater** als aparte systemd-service draaien. Deze updater kan periodieke taken uitvoeren, zoals het bijwerken van wedstrijdstatussen.

---

# Vereisten

Voor het draaien van TournamentHub heb je nodig:

* Python 3
* Git
* Een Python virtual environment
* systemd
* De dependencies uit `requirements.txt`

---

# Installatie

Clone eerst de repository:

```bash
git clone <repository-url>
cd tournamenthub
```

Maak een virtual environment:

```bash
python3 -m venv venv
```

Activeer de virtual environment:

```bash
source venv/bin/activate
```

Installeer alle dependencies:

```bash
pip install -r requirements.txt
```

Zorg ervoor dat `gunicorn` in `requirements.txt` staat. Bijvoorbeeld:

```text
gunicorn
```

---

# TournamentHub Service

Het systemd-servicebestand bevindt zich op:

```text
/etc/systemd/system/tournamenthub.service
```

Voorbeeld:

```ini
[Unit]
Description=TournamentHub Flask App
After=network.target

[Service]
User=<linux-user>
Group=<linux-user>
WorkingDirectory=<project-directory>
Environment="PATH=<project-directory>/venv/bin"
ExecStart=<project-directory>/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:9859 app:app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Vervang:

* `<linux-user>` door de Linux-gebruiker waarmee de service moet draaien.
* `<project-directory>` door het absolute pad naar de TournamentHub-directory.

Maak het servicebestand aan:

```bash
sudo nano /etc/systemd/system/tournamenthub.service
```

Laad systemd opnieuw:

```bash
sudo systemctl daemon-reload
```

Schakel automatisch starten bij boot in:

```bash
sudo systemctl enable tournamenthub
```

Start de service:

```bash
sudo systemctl start tournamenthub
```

---

# TournamentHub Updater

De updater kan als een aparte systemd-service draaien:

```text
tournamenthub-updater
```

Hierdoor kan de updater onafhankelijk van de website worden gestart, gestopt en gecontroleerd.

## Updater starten

```bash
sudo systemctl start tournamenthub-updater
```

## Updater stoppen

```bash
sudo systemctl stop tournamenthub-updater
```

## Updater herstarten

```bash
sudo systemctl restart tournamenthub-updater
```

## Updater status bekijken

```bash
sudo systemctl status tournamenthub-updater
```

## Updater automatisch starten bij boot

```bash
sudo systemctl enable tournamenthub-updater
```

## Updater niet automatisch starten bij boot

```bash
sudo systemctl disable tournamenthub-updater
```

## Live logs bekijken

```bash
sudo journalctl -u tournamenthub-updater -f
```

## Laatste 100 logregels bekijken

```bash
sudo journalctl -u tournamenthub-updater -n 100 --no-pager
```

---

# Website beheren

## Status bekijken

```bash
sudo systemctl status tournamenthub
```

## Starten

```bash
sudo systemctl start tournamenthub
```

## Stoppen

```bash
sudo systemctl stop tournamenthub
```

## Herstarten

```bash
sudo systemctl restart tournamenthub
```

## Automatisch starten bij boot

```bash
sudo systemctl enable tournamenthub
```

## Automatisch starten bij boot uitschakelen

```bash
sudo systemctl disable tournamenthub
```

---

# Logs

## Live logs

```bash
sudo journalctl -u tournamenthub -f
```

## Laatste 100 regels

```bash
sudo journalctl -u tournamenthub -n 100 --no-pager
```

## Logs van vandaag

```bash
sudo journalctl -u tournamenthub --since today
```

## Serviceconfiguratie bekijken

```bash
sudo systemctl cat tournamenthub
```

---

# Wijzigingen aan de applicatie

Wanneer `app.py` of andere Python-code is gewijzigd:

```bash
sudo systemctl restart tournamenthub
```

Wanneer alleen de Python-code is aangepast, hoeft de updater normaal gesproken niet opnieuw gestart te worden.

---

# Wijzigingen aan de updater

Wanneer de updatercode is gewijzigd:

```bash
sudo systemctl restart tournamenthub-updater
```

Logs controleren:

```bash
sudo journalctl -u tournamenthub-updater -f
```

---

# Serviceconfiguratie aanpassen

Open het servicebestand:

```bash
sudo nano /etc/systemd/system/tournamenthub.service
```

Na wijzigingen:

```bash
sudo systemctl daemon-reload
sudo systemctl restart tournamenthub
```

Voor de updater geldt hetzelfde:

```bash
sudo systemctl daemon-reload
sudo systemctl restart tournamenthub-updater
```

---

# Poort wijzigen

De standaardpoort is `9859`.

Zoek in het servicebestand:

```ini
ExecStart=<project-directory>/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:9859 app:app
```

Pas `9859` aan naar de gewenste poort.

Daarna:

```bash
sudo systemctl daemon-reload
sudo systemctl restart tournamenthub
```

---

# Aantal Gunicorn-workers wijzigen

In het servicebestand staat bijvoorbeeld:

```ini
--workers 4
```

Pas het aantal workers aan naar de gewenste waarde.

Daarna:

```bash
sudo systemctl daemon-reload
sudo systemctl restart tournamenthub
```

---

# Testen

Controleer of de service draait:

```bash
sudo systemctl status tournamenthub
```

Je kunt lokaal testen met:

```bash
curl http://127.0.0.1:9859
```

De website is vervolgens bereikbaar via de host waarop TournamentHub draait:

```text
http://<host>:9859
```

---

# Beide services controleren

Website:

```bash
sudo systemctl status tournamenthub
```

Updater:

```bash
sudo systemctl status tournamenthub-updater
```

Beide starten:

```bash
sudo systemctl start tournamenthub
sudo systemctl start tournamenthub-updater
```

Beide automatisch laten starten bij boot:

```bash
sudo systemctl enable tournamenthub
sudo systemctl enable tournamenthub-updater
```

---

# Service verwijderen

## TournamentHub verwijderen

Stop de service:

```bash
sudo systemctl stop tournamenthub
```

Schakel automatisch starten uit:

```bash
sudo systemctl disable tournamenthub
```

Verwijder het servicebestand:

```bash
sudo rm /etc/systemd/system/tournamenthub.service
```

Laad systemd opnieuw:

```bash
sudo systemctl daemon-reload
```

## Updater verwijderen

Stop de updater:

```bash
sudo systemctl stop tournamenthub-updater
```

Schakel automatisch starten uit:

```bash
sudo systemctl disable tournamenthub-updater
```

Verwijder het servicebestand:

```bash
sudo rm /etc/systemd/system/tournamenthub-updater.service
```

Laad systemd opnieuw:

```bash
sudo systemctl daemon-reload
```

---

# Veelvoorkomende problemen

## Website start niet

Bekijk de status:

```bash
sudo systemctl status tournamenthub
```

Bekijk de logs:

```bash
sudo journalctl -u tournamenthub -n 100 --no-pager
```

## Updater start niet

Bekijk de status:

```bash
sudo systemctl status tournamenthub-updater
```

Bekijk de logs:

```bash
sudo journalctl -u tournamenthub-updater -n 100 --no-pager
```

Voor live logs:

```bash
sudo journalctl -u tournamenthub-updater -f
```

## Gunicorn wordt niet gevonden

Controleer of de virtual environment actief is:

```bash
source venv/bin/activate
```

Installeer vervolgens de dependencies opnieuw:

```bash
pip install -r requirements.txt
```

Controleer Gunicorn:

```bash
gunicorn --version
```

Of:

```bash
./venv/bin/gunicorn --version
```

## Flask-app wordt niet gevonden

Controleer of `app.py` een Flask-applicatie met de naam `app` bevat:

```python
from flask import Flask

app = Flask(__name__)
```

Wanneer de applicatie anders heet, moet ook het laatste gedeelte van `ExecStart` worden aangepast.

Bijvoorbeeld:

```ini
app:app
```

---

# Handige documentatie

* [systemd](https://www.freedesktop.org/wiki/Software/systemd/)
* [Gunicorn](https://docs.gunicorn.org/)
* [Flask](https://flask.palletsprojects.com/)
* [journalctl](https://www.freedesktop.org/software/systemd/man/journalctl.html)

---

# Projectinformatie

| Onderdeel          | Technologie             |
| ------------------ | ----------------------- |
| Project            | TournamentHub           |
| Framework          | Flask                   |
| WSGI-server        | Gunicorn                |
| Servicebeheer      | systemd                 |
| Website-poort      | 9859                    |
| Workers            | 4                       |
| Updater            | `tournamenthub-updater` |
| Python environment | `venv`                  |
| Applicatie         | `app.py`                |
| Dependencies       | `requirements.txt`      |
