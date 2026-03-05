# 🌟 AstroCity

**AstroCity** è un'app web di astrocartografia che calcola le linee planetarie della tua mappa natale e ti indica le città nel mondo più favorevoli per carriera, amore, crescita personale e vita privata.

## ✨ Funzionalità

- **Calcolo effemeridi** in puro JavaScript (algoritmi di Jean Meeus)
- **10 pianeti**: Sole, Luna, Mercurio, Venere, Marte, Giove, Saturno, Urano, Nettuno, Plutone
- **40 linee astrocartografiche** (MC, IC, AC, DC per ogni pianeta)
- **Database di 500+ città** mondiali con coordinate geografiche
- **Scoring multi-categoria**: Carriera, Relazioni, Crescita Personale, Casa
- **Profili multipli** salvati in localStorage
- **Design dark** con stelle animate e tema astrologico
- **Funziona offline** (dopo il primo caricamento)

## 🚀 Come usare

1. Apri `index.html` nel browser (o servilo con qualsiasi server statico)
2. Inserisci i tuoi dati natali (nome, data, ora, luogo di nascita)
3. Clicca **Calcola** e attendi il calcolo
4. Esplora le 4 categorie: Carriera, Relazioni, Crescita, Casa
5. Scopri le tue città più favorevoli nel mondo!

## 🔭 Matematica astronomica

I calcoli planetari seguono il libro **"Astronomical Algorithms"** di Jean Meeus (2a edizione). Per ogni pianeta vengono calcolati:
- **Right Ascension (RA)** e **Declinazione (Dec)** alla data/ora di nascita
- **Local Mean Sidereal Time (LMST)** per il luogo di nascita
- **Linee MC/IC** (verticali): meridiani dove il pianeta culmina/è all'antinadir
- **Linee AC/DC** (curve): latitudini dove il pianeta sorge/tramonta

## 📁 Struttura

```
astrocity/
├── index.html    ← app completa self-contained
├── README.md     ← questo file
└── .gitignore
```

## 🛠️ Tecnologie

- HTML5 / CSS3 / Vanilla JavaScript (ES6+)
- Google Fonts (Inter + Playfair Display)
- Zero dipendenze esterne

---

*Creato con ❤️ e stelle ✨*
