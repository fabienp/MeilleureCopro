Meilleure Copro

Back-office Django REST Framework + Front-office Angular 20
Application pour consulter des statistiques sur les charges de copropriété et ajouter des annonces en base.

📝 Description

Ce projet permet de :

Consulter et rechercher des statistiques sur les charges de copropriété depuis la base de données fourrnie
Attention seule une moitié du jeu de données original à été importé pour des raisons de volume.

Ajouter une annonce dans la base de données via l’URL de l’annonce.

Le front-office est réalisé en Angular 20, le back-office en Django REST Framework.

⚙️ Prérequis

Python 3.x (installation via requirements.txt)

Node.js 22 et npm

Base de données : fichier SQL fourni (téléchargeable depuis le lien fourni dans le mail)

🏗️ Installation
1. Back-office Django
# Aller dans le dossier backend
cd backend

# Créer un environnement virtuel (optionnel mais recommandé)
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

2. Front-office Angular
# Aller dans le dossier frontend
cd frontend

# Installer les dépendances
npm install

🚀 Lancer le projet
Back-office
# Depuis le dossier backend
python manage.py runserver


L’API sera disponible par défaut sur : http://127.0.0.1:8000/

Front-office
# Depuis le dossier front-end
ng serve


L’application Angular sera disponible sur : http://localhost:4200/

📂 Structure du projet
Meilleur copro/
├─ backend/          # Django REST backend
│  ├─ manage.py
│  ├─ requirements.txt
│  └─ ...
├─ front-end/        # Angular 20 frontend
│  └─ ...
└─ README.md

⭐ Fonctionnalités principales

Recherche et consultation de statistiques

Filtrage par département, ville ou code postal

Consultation de statistiques sur les charges de copropriété

Calcul de : moyenne, 10% quantile, 90% quantile

Ajout d’annonce dans la base de données

Ajout via l’URL Bienici

Validation de l’URL et extraction automatique des informations (ville, département, code postal, charges)

📌 Remarques

La base de données fournie contient seulement la moitié du jeu de données original.

Les filtres statistiques sont insensibles à la casse et excluent les valeurs nulles ou inférieures à 0 pour les charges.

Les quantiles (10% / 90%) permettent d’exclure les valeurs extrêmes lors de l’affichage des résultats.
