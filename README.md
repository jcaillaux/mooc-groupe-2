# Projet MOOC Groupe 2

## Prérequis 

### Configuration de l'environnement

```bash
# Cloner le projet
git clone https://github.com/jcaillaux/mooc-groupe-2.git

# Création de l'environnement virtuel
python -m venv .venv

# Activation de l'environnement virtuel
source .venv/bin/activate
```

### Docker

```bash
# Construction de l'image docker
docker buildx build -t mooc:latest .

# Exécution du conteneur
docker run -p 7860:7860 mooc:latest
```

L'application sera accessible à partir d'un navigateur web.  



### Arborescence projet

```bash
.
├── .env.template
├── analyse/
├── app/
├── data/
├── docs/
├── frontend/
├── scripts/
├── tests/
├── config.py
├── README.md
└── requirements.txt
```

### Structure du fichier .env

Le fichier .env.template est à modifier avec ses propres paramètres.
Ensuite, il faut le renommer en .env 

