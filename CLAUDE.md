# Site de cours particuliers (Noé Carel & Marie Burtin)

Site statique publié par GitHub Pages : https://coursparticulierslille.github.io/Cours-Lille/

- Source de la page : `src/page.html` (contenu, styles, script, objet `CONFIG`).
- En-tête Google (SEO) : `src/seo-head.html`.
- `index.html` et `sitemap.xml` sont GÉNÉRÉS par `python3 scripts/build.py` : ne pas les modifier à la main.

## Mettre à jour les créneaux libres

1. Lire l'agenda Google de Noé (calendrier principal `noecarelnnl@gmail.com`) sur les 5 prochaines semaines
   avec le connecteur Google Agenda.
2. Écrire `data/events-noe.json` : `{"events": [["AAAA-MM-JJTHH:MM", "AAAA-MM-JJTHH:MM", "titre"], ...]}`
   (heure locale de Paris, sans fuseau ; ignorer les événements « journée entière » et ceux marqués disponibles).
   Ce fichier est privé : il est dans `.gitignore` et ne doit jamais être publié.
   Même chose pour Marie avec `data/events-marie.json` quand son agenda sera accessible.
3. `python3 scripts/build.py` puis commit + push de `index.html` et `sitemap.xml`.

Règles appliquées par `scripts/build.py` : lundi-vendredi 14h-20h, samedi 10h-20h, pas le dimanche,
40 min de trajet avant/après chaque événement, séances de 1 h 30 minimum, pas de réservation à moins de 24 h,
4 semaines affichées.

## Demandes de réservation

Le formulaire envoie la demande par mail au professeur via FormSubmit (`https://formsubmit.co/ajax/<mail du professeur>`).
Aucune réservation n'est enregistrée sur le site : le professeur confirme à la famille, puis ajoute le cours
dans son agenda, ce qui retire le créneau à la mise à jour suivante.
