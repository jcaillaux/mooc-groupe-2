# Projet MOOC Groupe 2

## Prérequis 

### Configuration de l'environement

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
docker run -p 8000:8000 mooc:latest
```

L'application sera accessible à partir d'un navigateur web.  



### Arborescence projet

```bash
.
├── analyse/
├── app/
├── data/
├── docs/
├── frontend/
├── README.md
└── scripts/
```



