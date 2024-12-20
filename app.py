
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, RadioField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired
from experta import KnowledgeEngine, Rule, Fact
import os
from experta import L


from flask_wtf.csrf import CSRFProtect




app = Flask(__name__)

# Set a secret key for CSRF protection
app.config['SECRET_KEY'] = os.urandom(24)

class ParfumForm(FlaskForm):
    # Questions sur la personnalité
    personnalite= RadioField('Comment décririez-vous votre personnalité ?', choices=[
        ('Introvertie', 'Introvertie'),
        ('Romantique', 'Romantique'),
        ('Extravertie', 'Extravertie'),
        ('Audacieuse', 'Audacieuse'),
        ('Calme et réfléchie', 'Calme et réfléchie')], validators=[DataRequired()])

    ambiance = RadioField('Préférez-vous les ambiances suivantes ?', choices=[
        ('Dynamiques', 'Dynamiques'),
        ('Calmes', 'Calmes'),
        ('Paisibles', 'Paisibles')], validators=[DataRequired()])

    tendance = RadioField('Préférez-vous les tendances suivantes ?', choices=[
        ('Classiques', 'Classiques'),
        ('Modernes', 'Modernes')], validators=[DataRequired()])

    cadre = RadioField('Vous sentez-vous plus à l’aise dans un cadre :', choices=[
        ('Naturel', 'Naturel'),
        ('Urbain', 'Urbain')], validators=[DataRequired()])

    # Genre et usage
    genre = RadioField('Quel est votre genre ?', choices=[
        ('Homme', 'Homme'),
        ('Femme', 'Femme')],
        validators=[DataRequired()])

    occasion = RadioField('À quelle occasion souhaitez-vous porter ce parfum ?',
                                  choices=[('Quotidien', 'Quotidien'),
                                           ('Travail', 'Travail'),
                                           ('Soirée', 'Soirée'),
                                           ('Rendez-vous romantique', 'Rendez-vous romantique'),
                                           ('Sport', 'Sport')])

    saison = RadioField('Recherchez-vous un parfum pour une saison spécifique ?', choices=[
        ('Printemps', 'Printemps'),
        ('Été', 'Été'),
        ('Automne', 'Automne'),
        ('Hiver', 'Hiver')])

    # Préférences olfactives
       # Sélection multiple avec BooleanField pour chaque option
  
    famille = RadioField('Avez-vous une note ou un ingrédient préféré ?',
        choices=[
        ('Floral', 'Floral'),
        ('Fruité', 'Fruité'),
        ('Boisé', 'Boisé'),
        ('Oriental', 'Oriental'),
        ('Frais', 'Frais'),
        ('Gourmand', 'Gourmand'),
        ('Aquatique', 'Aquatique'),
        ('Épicé', 'Épicé')],
        
        validators=[DataRequired()])

    # Budget et marque
    budget = RadioField('Quel est votre budget pour ce parfum ?', choices=[
        ('50 € à 100 €', '50 € à 100 €'),
        ('Plus de 100 €', 'Plus de 100 €')], validators=[DataRequired()])

    marque = StringField('Avez-vous une marque préférée ?', validators=[DataRequired()])

   

    submit = SubmitField('Soumettre')

PARFUMS = [
    {"nom": "Dior Homme", "famille": "Boisé", "genre": "Homme", "occasion": "Soirée", "saison": "Hiver", 
     "budget": "Plus de 100 €", "marque": "Dior", "tendance": "Classiques", "ambiance": "Dynamiques", "cadre": "Urbain", "personnalite": "Audacieuse"},
    {"nom": "Flower by Kenzo", "famille": "Floral", "genre": "Femme", "occasion": "Rendez-vous romantique", "saison": "Printemps", 
     "budget": "50 € à 100 €", "marque": "Kenzo", "tendance": "Modernes", "ambiance": "Paisibles", "cadre": "Naturel", "personnalite": "Romantique"},
    {"nom": "L'Homme Yves Saint Laurent", "famille": "Boisé", "genre": "Homme", "occasion": "Travail", "saison": "Automne", 
     "budget": "Plus de 100 €", "marque": "Yves Saint Laurent", "tendance": "Classiques", "ambiance": "Paisibles", "cadre": "Urbain", "personnalite": "Extravertie"},
    {"nom": "Chloé", "famille": "Floral", "genre": "Femme", "occasion": "Quotidien", "saison": "Printemps", 
     "budget": "50 € à 100 €", "marque": "Chloé", "tendance": "Classiques", "ambiance": "Paisibles", "cadre": "Naturel", "personnalite": "Romantique"},
    {"nom": "La Nuit de l'Homme", "famille": "Oriental", "genre": "Homme", "occasion": "Soirée", "saison": "Hiver", 
     "budget": "Plus de 100 €", "marque": "Yves Saint Laurent", "tendance": "Modernes", "ambiance": "Dynamiques", "cadre": "Urbain", "personnalite": "Extravertie"},
    {"nom": "J'adore Dior", "famille": "Floral", "genre": "Femme", "occasion": "Rendez-vous romantique", "saison": "Été", 
     "budget": "Plus de 100 €", "marque": "Dior", "tendance": "Classiques", "ambiance": "Paisibles", "cadre": "Naturel", "personnalite": "Romantique"},
    {"nom": "Tom Ford Oud Wood", "famille": "Boisé", "genre": "Unisexe", "occasion": "Soirée", "saison": "Automne", 
     "budget": "Plus de 100 €", "marque": "Tom Ford", "tendance": "Modernes", "ambiance": "Dynamiques", "cadre": "Urbain", "personnalite": "Audacieuse"},
    {"nom": "Paco Rabanne Invictus Aqua", "famille": "Aromatique", "genre": "Homme", "occasion": "Sport", "saison": "Été", 
     "budget": "50 € à 100 €", "marque": "Paco Rabanne", "tendance": "Modernes", "ambiance": "Dynamiques", "cadre": "Naturel", "personnalite": "Audacieuse"},
    {"nom": "Viktor & Rolf Spicebomb", "famille": "Épicé", "genre": "Homme", "occasion": "Soirée", "saison": "Hiver", 
     "budget": "Plus de 100 €", "marque": "Viktor & Rolf", "tendance": "Modernes", "ambiance": "Dynamiques", "cadre": "Urbain", "personnalite": "Audacieuse"},
    {"nom": "Guerlain L'Homme Idéal", "famille": "Boisé", "genre": "Homme", "occasion": "Quotidien", "saison": "Automne", 
     "budget": "50 € à 100 €", "marque": "Guerlain", "tendance": "Modernes", "ambiance": "Paisibles", "cadre": "Naturel", "personnalite": "Extravertie"},
    {"nom": "Lancôme Trésor", "famille": "Floral", "genre": "Femme", "occasion": "Soirée", "saison": "Hiver", 
     "budget": "Plus de 100 €", "marque": "Lancôme", "tendance": "Classiques", "ambiance": "Paisibles", "cadre": "Urbain", "personnalite": "Romantique"},
    {"nom": "Yves Saint Laurent Mon Paris", "famille": "Floral", "genre": "Femme", "occasion": "Rendez-vous romantique", "saison": "Été", 
     "budget": "Plus de 100 €", "marque": "Yves Saint Laurent", "tendance": "Modernes", "ambiance": "Paisibles", "cadre": "Naturel", "personnalite": "Romantique"},
    {"nom": "Aventus by Creed", "famille": "Fruité", "genre": "Homme", "occasion": "Soirée", "saison": "Automne", 
     "budget": "Plus de 100 €", "marque": "Creed", "tendance": "Classiques", "ambiance": "Dynamiques", "cadre": "Urbain", "personnalite": "Extravertie"},
    {"nom": "Acqua di Parma Colonia", "famille": "Citrus", "genre": "Unisexe", "occasion": "Quotidien", "saison": "Printemps", 
     "budget": "Plus de 100 €", "marque": "Acqua di Parma", "tendance": "Classiques", "ambiance": "Paisibles", "cadre": "Naturel", "personnalite": "Audacieuse"},
    {"nom": "Bvlgari Man in Black", "famille": "Oriental", "genre": "Homme", "occasion": "Soirée", "saison": "Hiver", 
     "budget": "Plus de 100 €", "marque": "Bvlgari", "tendance": "Modernes", "ambiance": "Dynamiques", "cadre": "Urbain", "personnalite": "Audacieuse"},
    {"nom": "Chanel Allure Homme Sport", "famille": "Aromatique", "genre": "Homme", "occasion": "Sport", "saison": "Été", 
     "budget": "Plus de 100 €", "marque": "Chanel", "tendance": "Modernes", "ambiance": "Dynamiques", "cadre": "Naturel", "personnalite": "Audacieuse"},
    {"nom": "Coco Mademoiselle", "famille": "Chypré", "genre": "Femme", "occasion": "Soirée", "saison": "Automne", 
     "budget": "Plus de 100 €", "marque": "Chanel", "tendance": "Classiques", "ambiance": "Paisibles", "cadre": "Urbain", "personnalite": "Romantique"},
    {"nom": "Tom Ford Black Orchid", "famille": "Oriental", "genre": "Femme", "occasion": "Soirée", "saison": "Hiver", 
     "budget": "Plus de 100 €", "marque": "Tom Ford", "tendance": "Modernes", "ambiance": "Dynamiques", "cadre": "Urbain", "personnalite": "Audacieuse"},
    {"nom": "Hermès Terre d'Hermès", "famille": "Boisé", "genre": "Homme", "occasion": "Travail", "saison": "Automne", 
     "budget": "Plus de 100 €", "marque": "Hermès", "tendance": "Classiques", "ambiance": "Paisibles", "cadre": "Naturel", "personnalite": "Calme et réfléchie"},
    {"nom": "Mugler Alien", "famille": "Floral", "genre": "Femme", "occasion": "Soirée", "saison": "Hiver", 
     "budget": "Plus de 100 €", "marque": "Mugler", "tendance": "Classiques", "ambiance": "Paisibles", "cadre": "Urbain", "personnalite": "Romantique"},
    {"nom": "Bvlgari Omnia Crystalline", "famille": "Floral", "genre": "Femme", "occasion": "Quotidien", "saison": "Été", 
     "budget": "50 € à 100 €", "marque": "Bvlgari", "tendance": "Modernes", "ambiance": "Paisibles", "cadre": "Naturel", "personnalite": "Romantique"},
    {"nom": "Prada L'Homme", "famille": "Floral", "genre": "Homme", "occasion": "Travail", "saison": "Automne", 
     "budget": "Plus de 100 €", "marque": "Prada", "tendance": "Modernes", "ambiance": "Paisibles", "cadre": "Urbain", "personnalite": "Classique"}
]




from experta import Fact
from experta import MATCH

class Parfum(Fact):
    """Représente les caractéristiques d'un parfum."""
    
    pass
class ParfumRecommender(KnowledgeEngine):
    def __init__(self, parfums):
        super().__init__()
        self.parfums = parfums
        self.recommendation = None
        self.scores = []  # Liste pour stocker les scores de correspondance
    # Règle pour recommander un parfum
    @Rule(Fact(genre=MATCH.genre),
      Fact(famille=MATCH.famille),
      Fact(occasion=MATCH.occasion),
      Fact(saison=MATCH.saison),
      Fact(budget=MATCH.budget),
      Fact(personnalite=MATCH.personnalite),
      Fact(cadre=MATCH.cadre),
      Fact(tendance=MATCH.tendance),
      Fact(ambiance=MATCH.ambiance))
    def calculate_scores(self, genre, famille, occasion, saison, budget, personnalite, cadre, tendance, ambiance):
        for parfum in self.parfums:
            score = 0  # Initialiser le score
            total_criteres = 6  # Nombre total de critères

            # Calcul du score en fonction des correspondances
            if parfum["genre"].lower() != genre.lower():
                continue  # Si le genre du parfum ne correspond pas, on le saute
            if parfum["famille"].lower() == famille.lower():
                score += 1
            if parfum["occasion"].lower() == occasion.lower():
                score += 1
            if parfum["saison"].lower() == saison.lower():
                score += 1
            if parfum["budget"].lower() == budget.lower():
                score += 1
            if parfum["personnalite"].lower() == personnalite.lower():
                score += 1
            if parfum["ambiance"].lower() == ambiance.lower():
                score += 1
            if parfum["cadre"].lower() == cadre.lower():
                score += 1
            if parfum["tendance"].lower() == tendance.lower():
                score += 1
       

            # Calculer le pourcentage de correspondance
            pourcentage =  round((score / total_criteres) * 100)

            # Ajouter le résultat à la liste
            self.scores.append({"nom": parfum["nom"], "pourcentage": pourcentage})
    def get_recommendations(self):
      # Vérifier que des scores existent
     if not self.scores:
        return []
      # Filtrer les scores pour inclure uniquement ceux >= 50%
     filtres = [score for score in self.scores if score["pourcentage"] >= 50]
     # Trier les scores par ordre décroissant
     filtres.sort(key=lambda x: x["pourcentage"], reverse=True)
     return filtres
   


# Fonction pour recommander un parfum
def recommend_parfum(preferences):
    recommender = ParfumRecommender(PARFUMS)
    
    # Déclarez les faits basés sur les préférences de l'utilisateur
    for key, value in preferences.items():
        recommender.declare(Fact(**{key: value}))
    
    # Exécute le moteur de règles
    recommender.run()
    recommendations = recommender.get_recommendations()
    if not recommendations:
        print("Aucune recommandation trouvée.")
    return recommendations
# Route principale
@app.route('/')
def index():
    return render_template('index.html')
# Route page du formulaire
@app.route('/form.html', methods=['GET', 'POST'])
def form():
    form = ParfumForm()
    recommandations = None

    if form.validate_on_submit():
        # Récupérer les préférences de l'utilisateur
        preferences = {
            "genre": form.genre.data,
            "famille": form.famille.data,
            "occasion": form.occasion.data,
            "saison": form.saison.data,
            "budget": form.budget.data,
            "personnalite": form.personnalite.data,
            "cadre": form.cadre.data,
            "tendance": form.tendance.data,
            "ambiance": form.ambiance.data,

        }
        # Afficher les données du formulaire dans la console (facultatif)
        print("Données du formulaire :", preferences)

        # Recommander des parfums
        recommandations = recommend_parfum(preferences)
        # Vérifiez si des recommandations existent
        if not recommandations:
            return render_template('result.html', message="Aucune recommandation trouvée.")
        return render_template('result.html', recommandations=recommandations)

    return render_template('form.html', form=form)

# Exécution de l'application
if __name__ == '__main__':
    app.run(debug=True)