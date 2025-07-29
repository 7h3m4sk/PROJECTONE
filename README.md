

# PROJECTONE - AUTO IP CHANGER

---

## Funkcje

- Dynamiczna zmiana IP przez Tor (`NEWNYM`)
- Detekcja zależności przy starcie
- Podgląd aktualnego IP
- Tryb stealth (w planach)

---

## 🛠Wymagania

- Linux (testowany na Arch Linux / Hyprland)
- Python `>=3.10`
- Zainstalowane biblioteki:
  - `stem`
  - `requests`
  - `pysocks`
  - `colorama`

---

## Instalacja

### Zainstaluj Tor

```bash
sudo pacman -S tor
systemctl status tor

```

puzniej wejdz w tor komendą poniżej

```bash
sudo nano /etc/tor/torrc
```
i zmień lub dodaj port i cookieautentication

```bash
ControlPort 9051
CookieAuthentication 1
```

Potem zrestartuj Tor

```bash
sudo systemctl restart tor
```

⚠️Zastrzeżenie

Ten projekt został stworzony do celów edukacyjnych i demonstracyjnych. Nie ponoszę odpowiedzialności za sposób jego wykorzystania.
📜 Licencja

Projekt objęty licencją MIT



