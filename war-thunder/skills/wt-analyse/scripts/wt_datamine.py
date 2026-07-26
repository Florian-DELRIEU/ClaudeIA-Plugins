#!/usr/bin/env python3
"""
wt_datamine.py — Extraction de données fiables depuis le datamine War Thunder
(gszabi99/War-Thunder-Datamine) pour le skill /WT-analyse.

Usage:
  python3 wt_datamine.py resolve <mot-clé>       -> liste les noms internes candidats
  python3 wt_datamine.py perf <nom_interne>      -> table vitesse/montée par altitude
  python3 wt_datamine.py limits <nom_interne>    -> limites structurelles, masse
  python3 wt_datamine.py br <nom_interne>        -> BR RB/AB/SB, coûts

Le nom interne (ex: "d_520_france", "spitfire_mk1", "ki_43_1") s'obtient
via `resolve` si on ne le connaît pas déjà.
"""
import json, subprocess, sys, os, urllib.request

REPO_DIR = os.path.expanduser("~/wtdm_cache")
REPO_URL = "https://github.com/gszabi99/War-Thunder-Datamine.git"
RAW_BASE = "https://raw.githubusercontent.com/gszabi99/War-Thunder-Datamine/master/"
WPCOST_PATH = "char.vromfs.bin_u/config/wpcost.blkx"
WPCOST_CACHE = os.path.join(REPO_DIR, "_wpcost_cache.json")
TREE_CACHE = os.path.join(REPO_DIR, "_tree_cache.txt")


def ensure_repo():
    """Clone en mode blobless (arborescence seule, pas de contenu) si absent."""
    os.makedirs(REPO_DIR, exist_ok=True)
    if not os.path.isdir(os.path.join(REPO_DIR, "repo", ".git")):
        subprocess.run(
            ["git", "clone", "--depth", "1", "--filter=blob:none", "--no-checkout",
             REPO_URL, os.path.join(REPO_DIR, "repo")],
            check=True, capture_output=True
        )


def list_tree():
    """Liste tous les chemins du dépôt (rapide : arborescence seule, pas de blobs)."""
    if os.path.isfile(TREE_CACHE):
        with open(TREE_CACHE) as f:
            return f.read().splitlines()
    ensure_repo()
    out = subprocess.run(
        ["git", "-C", os.path.join(REPO_DIR, "repo"), "ls-tree", "-r", "--name-only", "HEAD"],
        capture_output=True, text=True, check=True
    )
    with open(TREE_CACHE, "w") as f:
        f.write(out.stdout)
    return out.stdout.splitlines()


def _norm(s):
    """Normalise en retirant tous les séparateurs, pour une comparaison floue."""
    for ch in " .-_":
        s = s.replace(ch, "")
    return s.lower()


def resolve(query):
    q = _norm(query)
    paths = list_tree()
    hits = [p for p in paths if "/flightmodels/performance/" in p and p.endswith(".blkx")]
    names = sorted(set(os.path.basename(p)[:-len(".blkx")] for p in hits
                        if q in _norm(os.path.basename(p)[:-len(".blkx")])))
    return names


def fetch_raw(path):
    url = RAW_BASE + path
    with urllib.request.urlopen(url) as r:
        return r.read()


def perf(name):
    try:
        data = json.loads(fetch_raw(f"aces.vromfs.bin_u/gamedata/flightmodels/performance/{name}.blkx"))
    except Exception as e:
        print(f"Erreur : fichier performance introuvable pour '{name}' ({e})")
        return
    print(f"{'Altitude':>10} | {'Vmax (km/h)':>12} | {'Vy opt (km/h)':>13} | {'Montée (m/s)':>13}")
    for alt_key, s in data["altSpecs"].items():
        alt = alt_key.replace("altSpecs", "") or "0"
        print(f"{alt:>9}m | {s['maxSpeed']*3.6:12.1f} | {s['optSpeed']*3.6:13.1f} | {s['maxClimb']:13.2f}")
    print(f"\nDistance décollage/atterrissage : {data['takeoffDistance']:.0f} m / {data['landingDistance']:.0f} m")
    print("\n[Note] Table calculée par le moteur du jeu (config optimale/spadée). Fiable en")
    print("comparaison relative entre appareils ; recouper avec une source communautaire")
    print("pour une valeur absolue annoncée telle quelle.")


def limits(name):
    try:
        data = json.loads(fetch_raw(f"aces.vromfs.bin_u/gamedata/flightmodels/fm/{name}.blkx"))
    except Exception as e:
        print(f"Erreur : fichier fm introuvable pour '{name}' ({e})")
        return
    print(f"Vitesse max (sol / altitude)  : {data.get('MaxSpeedNearGround','?')} / {data.get('MaxSpeedAtAltitude','?')} km/h")
    print(f"VneControl (limite IAS globale): {data.get('VneControl','?')} km/h")
    mass = data.get("Mass", {})
    print(f"Masse à vide                  : {mass.get('EmptyMass','?')} kg")
    print(f"Carburant interne max          : {mass.get('MaxFuelMass0','?')} kg")
    print(f"Limite train (IAS)             : {mass.get('GearDestructionIndSpeed','?')} km/h")
    for k, label in [("FlapsDestructionIndSpeedP0", "Volets décollage (IAS)"),
                      ("FlapsDestructionIndSpeedP1", "Volets combat (IAS)"),
                      ("FlapsDestructionIndSpeedP2", "Volets atterrissage (IAS)")]:
        if k in mass:
            print(f"{label:32s}: {mass[k][1]} km/h (seuil {mass[k][0]})")
    # Limites structurelles réelles : Aerodynamics.WingPlane.Strength
    aero = data.get("Aerodynamics", {})
    wing = aero.get("WingPlane", {})
    st = wing.get("Strength")
    if st:
        print(f"\nVNE (limite structurelle)      : {st.get('VNE')} km/h")
        print(f"MNE (limite Mach)              : {st.get('MNE')}")
        co = st.get("CritOverload")
        if co:
            print(f"CritOverload (aile, N)         : {co[0]:.0f} / {co[1]:.0f}  (négatif/positif — pas directement des G, cf. skill)")


def ensure_wpcost():
    if not os.path.isfile(WPCOST_CACHE):
        raw = fetch_raw(WPCOST_PATH)
        with open(WPCOST_CACHE, "wb") as f:
            f.write(raw)
    with open(WPCOST_CACHE, "rb") as f:
        return json.load(f)


def br(name):
    data = ensure_wpcost()
    # Toujours lister les homonymes : le nom du fichier fm/performance (ex: "d_520")
    # peut coexister dans wpcost avec des variantes par pays (ex: "d_520_france"),
    # y compris d'anciens véhicules premium retirés du jeu partageant le même nom nu.
    candidates = sorted(k for k in data if isinstance(data[k], dict) and _norm(name) in _norm(k))
    if len(candidates) > 1:
        print(f"Plusieurs entrées correspondent à '{name}' — choisir le nom exact :")
        for c in candidates:
            print(f"  {c:25s} pays={data[c].get('country','?'):18s} rang={data[c].get('rank','?')}")
        if name not in candidates:
            return
        print(f"(nom exact '{name}' aussi trouvé — utilisation de celui-ci, vérifier que c'est le bon)\n")
    e = data.get(name)
    if not e:
        print(f"'{name}' introuvable dans wpcost.blkx (vérifier le nom interne via resolve).")
        return
    def to_br(rank):
        return round(1 + rank / 3, 1)
    # Nommage interne du jeu : Arcade=AB, Historical=RB, Simulation=SB
    print(f"BR AB       : {to_br(e['economicRankArcade'])}")
    print(f"BR RB       : {to_br(e['economicRankHistorical'])}")
    print(f"BR SB       : {to_br(e['economicRankSimulation'])}")
    print(f"Rang        : {e.get('rank','?')}  |  Pays : {e.get('country','?')}")
    print(f"Achat       : {e.get('value','?')} SL  |  Recherche : {e.get('reqExp','?')} RP")
    print(f"Réparation (SL) AB/RB/SB : {e.get('repairCostArcade','?')}/{e.get('repairCostHistorical','?')}/{e.get('repairCostSimulation','?')}")


if __name__ == "__main__":
    try:
        cmd = sys.argv[1] if len(sys.argv) > 1 else ""
        if cmd == "resolve" and len(sys.argv) > 2:
            found = resolve(sys.argv[2])
            print("\n".join(found) if found else "Aucun résultat.")
        elif cmd == "perf" and len(sys.argv) > 2:
            perf(sys.argv[2])
        elif cmd == "limits" and len(sys.argv) > 2:
            limits(sys.argv[2])
        elif cmd == "br" and len(sys.argv) > 2:
            br(sys.argv[2])
        else:
            print(__doc__)
    except BrokenPipeError:
        pass
