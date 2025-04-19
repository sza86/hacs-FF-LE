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
1. Skopiuj folder `ff_le_03mw` do katalogu `custom_components` w Home Assistant
2. Zrestartuj Home Assistant
3. Dodaj integrację przez interfejs użytkownika

## Wymagania
- `pymodbus >= 3.0.0`

## Licencja
MIT
