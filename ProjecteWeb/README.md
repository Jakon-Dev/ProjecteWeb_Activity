
# Projecte Web Valorant (Django)

Aquest projecte és una aplicació web feta amb Django que utilitza la API no oficial de Valorant per obtenir informació sobre el joc i mostrar-la a través d'una petita visualització web amb autenticació d'usuari.

## Models de la Base de Dades

Els models es poden dividir en dues categories:

### Models de la API No Oficial (https://dash.valorant-api.com/)

| Model        | Descripció |
|--------------|------------|
| Agent        | Representa un agent de Valorant amb imatges, rols i habilitats. |
| AgentRole    | Rol que pot tindre un agent (ex: Duelist, Sentinel, etc). |
| AgentAbility | Abilitat d'un agent (ex: Q, E, C, X, passiva). |
| Map          | Representa un mapa del joc amb diverses imatges i descripcions. |
| PlayerCard   | Targeta de jugador decorativa. |
| PlayerTitle  | Títol decoratiu d'un jugador. |

### Models de la API Oficial (https://developer.riotgames.com/apis)

| Model        | Descripció |
|--------------|------------|
| User         | Model personalitzat d'usuari, relacionat amb PlayerCard i PlayerTitle, guarda també els partits recents. |
| Match        | Guarda un partit complet amb el mapa, resultat, duració i informació JSON del partit. |
| MatchPlayer  | Guarda la informació d'un jugador dins d'un partit (kills, deaths, assists, agent usat, etc). |
| MatchRound   | Guarda informació detallada de cada ronda d'un partit (guanyador, planter de bomba, defuser, temps, etc). |

---

## Estructura i Funcionament del Dockerfile

En l'arxiu `entrypoint.sh` es pot veure com funciona l'entorn dins del Docker:

```
# Executa el servidor Django
poetry run python manage.py runserver 0.0.0.0:8000 &

# Executa el script per descarregar dades de la API no oficial
poetry run python -c "from scripts.fetch_data import main; main()"
```

Això significa que quan aixequem el projecte amb `docker-compose up`:

1. Es baixa la informació de la API no oficial (`agents`, `maps`, `cosmetics`) mitjançant el fitxer `fetch_data.py`.
2. Després d'això, es deixa el servidor de Django disponible a `localhost:8000`.

Exemple del fitxer `UN_OFFICIAL.py`:

```python
def get_agents():
    return get('agents')['data']
```

---

## Visualització i Validació de les Dades

El projecte té una petita visualització per validar que les dades s'han descarregat i processat correctament.

En concret:

- Sistema d'autenticació bàsic (Login/Register/Logout).
- Visualització de tots els agents des de la base de dades (`/agents`).
- Admin panel amb gestió de totes les dades obtingudes.

Aquestes funcionalitats permeten comprovar ràpidament que les dades baixades amb `fetch_data.py` s'han guardat correctament i es poden consumir des de la web.

---

## Execució del Projecte

```
docker-compose up --build
```

Accedir a:
- `localhost:8000` per a la web.
- `localhost:8000/admin` per a l'administració.

---

## Autor

Marc Lapeña Riu

Jordi Pifarré Ribes

Pau Ortiz Sanchez

Gerard Pueyo Sanz
