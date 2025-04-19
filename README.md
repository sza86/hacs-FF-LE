# Integracja Home Assistant: F&F LE-03MW

Integracja niestandardowa (`custom_component`) dla licznika energii **F&F LE-03MW** komunikującego się przez Modbus RTU/TCP.

## Autor
- **Autor:** SZA
- **GitHub:** [sz86](https://github.com/sz86)

## Funkcje:
- Obsługa Modbus TCP
- Odczyt napięć, prądów, mocy czynnej, biernej, pozornej, współczynnika mocy, częstotliwości
- Odczyt energii czynnej i biernej (pobranej i oddanej)
- W pełni zgodna z Home Assistant 2025.x
- Konfiguracja przez UI (config flow)

## Instalacja

### 📁 Metoda 1: Ręczna instalacja w Home Assistant
1. Pobierz paczkę ZIP z tego repozytorium (zielony przycisk "Code" → "Download ZIP").
2. Rozpakuj archiwum i skopiuj folder `ff_le_03mw` do katalogu:
   ```
   /config/custom_components/
   ```
3. Uruchom ponownie Home Assistant.
4. Przejdź do `Ustawienia` → `Urządzenia i usługi` → `Dodaj integrację`.
5. Wyszukaj `F&F LE-03MW` i skonfiguruj (IP, port, slave ID).

---

### 🌐 Metoda 2: Instalacja przez HACS z repozytorium GitHub
1. W Home Assistant przejdź do **HACS → Integracje**.
2. Kliknij `⋯` w prawym górnym rogu → `Dodaj repozytorium niestandardowe`.
3. Wklej URL tego repozytorium:
   ```
   https://github.com/sz86/ff_le_03mw
   ```
4. Wybierz typ: **Integracja** i zatwierdź.
5. Po chwili integracja będzie dostępna w zakładce `Integracje` w HACS.
6. Zainstaluj ją, uruchom ponownie Home Assistant i dodaj integrację przez UI.

## Wymagania
- `pymodbus >= 3.0.0`

## Licencja
MIT

## 👤 Autor

Integracja stworzona przez [sza86](https://github.com/sza86)