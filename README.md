# PROJECTONE

PROJECTONE was created with the goal of providing greater anonymity on the internet.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/5687ae5a-d10a-4a84-80b3-b5aa19fa3900" />

> The program was developed and tested on Arch Linux. In the future, support for other distributions will be added.

---

## Features

* Dynamic IP change via Tor (`NEWNYM`)
* Dependency check on startup
* Current IP address preview
* Stealth mode *(planned)*

---

## Requirements

* Linux (tested on Arch Linux / Hyprland)
* Python `>=3.10`
* Installed Python libraries:

  * `stem`
  * `requests`
  * `pysocks`
  * `colorama`

---

## Installation

### Install Tor

```bash
sudo pacman -S tor
systemctl status tor
```

Then open the Tor configuration file:

```bash
sudo nano /etc/tor/torrc
```

Add or modify the following lines:

```bash
ControlPort 9051
CookieAuthentication 1
```

Restart the Tor service:

```bash
sudo systemctl restart tor
```

---

### start program

now download the PROJECTONE.py file and put it in some folder or leave it in downlands
and type

```
cd "file location"
```

now give the file permissions
```
sudo chmod +x projectone.py
```

now start script 

```
sudo python projectone.py
```

and Well done, if you installed everything correctly the script will work, if something goes wrong the script will tell you

---

## ⚠️ Disclaimer

This project was created for educational and demonstrational purposes only.
The author is not responsible for any misuse of this software.

---

## Future update

In the future, I plan to add 
```
 ~Tor bridge mode 
 ~support for some Linux distributions and also Windows
```

---

## 📜 License

This project is licensed under the **MIT License**.
