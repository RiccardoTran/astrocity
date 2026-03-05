"""
AstroCity — Backend Flask con Swiss Ephemeris (pyswisseph)
Calcola posizioni planetarie ad alta precisione (dati JPL NASA).
"""

import swisseph as swe
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.')
CORS(app)

# Mappa pianeti → ID Swiss Ephemeris
PLANETS = {
    'sun':     swe.SUN,
    'moon':    swe.MOON,
    'mercury': swe.MERCURY,
    'venus':   swe.VENUS,
    'mars':    swe.MARS,
    'jupiter': swe.JUPITER,
    'saturn':  swe.SATURN,
    'uranus':  swe.URANUS,
    'neptune': swe.NEPTUNE,
    'pluto':   swe.PLUTO,
}

# ── Endpoint principale ────────────────────────────────────────────────────────
@app.route('/api/planets', methods=['POST'])
def get_planets():
    """
    Input JSON:
      { year, month, day, hour, minute, [second] }
    Output JSON:
      { jd, gmst, planets: { sun: {ra, dec}, moon: {ra, dec}, ... } }

    RA restituito in ore (0–24) per compatibilità con il frontend.
    Dec restituito in gradi (-90 a +90).
    GMST restituito in gradi (0–360).
    """
    data = request.get_json(force=True)

    try:
        year   = int(data['year'])
        month  = int(data['month'])
        day    = int(data['day'])
        hour   = int(data.get('hour', 12))
        minute = int(data.get('minute', 0))
        second = float(data.get('second', 0))
    except (KeyError, ValueError) as e:
        return jsonify({'error': f'Parametri non validi: {e}'}), 400

    # Julian Day (UT)
    ut = hour + minute / 60.0 + second / 3600.0
    jd = swe.julday(year, month, day, ut, swe.GREG_CAL)

    # Greenwich Mean Sidereal Time → gradi
    gmst_hours = swe.sidtime(jd)      # ore (0–24)
    gmst_deg   = (gmst_hours * 15) % 360  # converti in gradi

    planets_out = {}
    for name, pid in PLANETS.items():
        try:
            # FLG_EQUATORIAL: restituisce direttamente RA/Dec geocentrici
            # FLG_SPEED: aggiunge velocità (utile per debug)
            pos, _ = swe.calc_ut(jd, pid, swe.FLG_EQUATORIAL | swe.FLG_SPEED)

            ra_deg  = pos[0]   # RA in gradi (0–360)
            dec_deg = pos[1]   # Declinazione in gradi

            planets_out[name] = {
                'ra':     ra_deg / 15.0,  # converti in ore per il frontend JS
                'ra_deg': ra_deg,
                'dec':    dec_deg,
            }
        except Exception as e:
            planets_out[name] = {'error': str(e)}

    return jsonify({
        'jd':     jd,
        'gmst':   gmst_deg,
        'source': 'swiss-ephemeris',
        'engine': f'pyswisseph {swe.version}',
        'planets': planets_out,
    })


# ── Health check ───────────────────────────────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status':  'ok',
        'engine':  'Swiss Ephemeris',
        'version': swe.version,
    })


# ── Serve frontend statico ─────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f'🌟 AstroCity API avviata su http://0.0.0.0:{port}')
    print(f'   Swiss Ephemeris v{swe.version}')
    app.run(host='0.0.0.0', port=port, debug=False)
