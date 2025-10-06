# test673-rat

Questo repository contiene il codice per un Remote Access Trojan (RAT) e un server VPS per gestire le connessioni.

## Struttura del Repository

- `rat/`: Contiene il codice del RAT scritto in C#.
- `vps_server/`: Contiene il codice del server VPS scritto in Python.
- `.gitignore`: File per ignorare i file non necessari.
- `README.md`: Documentazione del progetto.

## Istruzioni

### RAT

1. Apri `Program.cs` nella cartella `rat` con Visual Studio.
2. Compila il progetto per generare `test673.exe`.
3. Esegui `test673.exe` sul PC della vittima.

### Server VPS

1. Assicurati di avere Python installato sul tuo server VPS.
2. Copia `server.py` dalla cartella `vps_server` al tuo server VPS.
3. Esegui il comando seguente per installare le dipendenze necessarie:
   ```bash
   pip install paramiko
