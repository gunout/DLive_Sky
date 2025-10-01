# dashboard_audience_radio.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Audience Radio - Skyrock",
    page_icon="📻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B00;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #FF6B00, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B00;
        margin: 0.5rem 0;
    }
    .section-header {
        color: #FF6B00;
        border-bottom: 2px solid #FF6B00;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-weight: bold;
    }
    .skyrock-color {
        color: #FF6B00;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class RadioAudienceDashboard:
    def __init__(self):
        self.df = self.load_data()
        self.radios = ['Skyrock', 'NRJ', 'Fun Radio', 'RTL', 'Europe 1', 'France Inter', 'RMC', 'Virgin Radio']
        
    def load_data(self):
        """Charge les données d'audience des radios"""
        # Génération de données simulées réalistes pour 2015-2024
        np.random.seed(42)
        
        dates = pd.date_range('2015-01-01', '2024-12-31', freq='M')
        radios = ['Skyrock', 'NRJ', 'Fun Radio', 'RTL', 'Europe 1', 'France Inter', 'RMC', 'Virgin Radio']
        
        data = []
        
        for date in dates:
            for radio in radios:
                # Audience de base différente pour chaque radio
                base_audience = {
                    'Skyrock': 3.2, 'NRJ': 4.1, 'Fun Radio': 2.8, 'RTL': 3.9,
                    'Europe 1': 2.5, 'France Inter': 4.3, 'RMC': 2.9, 'Virgin Radio': 2.7
                }[radio]
                
                # Tendances spécifiques par radio
                trend = {
                    'Skyrock': -0.02,  # Légère baisse
                    'NRJ': 0.01,       # Stabilité
                    'Fun Radio': -0.01, # Légère baisse
                    'RTL': 0.005,      # Très légère hausse
                    'Europe 1': -0.015,# Légère baisse
                    'France Inter': 0.02, # Hausse
                    'RMC': 0.01,       # Légère hausse
                    'Virgin Radio': 0.005 # Stabilité
                }[radio]
                
                # Saisonnalité (variation mensuelle)
                month_effect = np.sin(2 * np.pi * date.month / 12) * 0.1
                
                # Effet COVID (baisse en 2020, reprise progressive)
                covid_effect = 0
                if date.year == 2020:
                    covid_effect = -0.3 + (date.month / 12) * 0.2
                elif date.year == 2021:
                    covid_effect = -0.1 + (date.month / 12) * 0.1
                
                # Calcul de l'audience
                years_from_start = (date.year - 2015) + (date.month - 1) / 12
                audience = base_audience * (1 + trend * years_from_start + month_effect + covid_effect)
                
                # Bruit aléatoire
                audience += np.random.normal(0, 0.05)
                
                # Parts de marché (calculées proportionnellement)
                data.append({
                    'date': date,
                    'radio': radio,
                    'audience_millions': max(audience, 0.1),  # Éviter les valeurs négatives
                    'annee': date.year,
                    'mois': date.month,
                    'trimestre': f"T{((date.month-1)//3)+1}-{date.year}",
                    'categorie': 'Musique' if radio in ['Skyrock', 'NRJ', 'Fun Radio', 'Virgin Radio'] else 'Généraliste'
                })
        
        df = pd.DataFrame(data)
        
        # Calcul des parts de marché par mois
        monthly_totals = df.groupby('date')['audience_millions'].transform('sum')
        df['part_marche_pourcent'] = (df['audience_millions'] / monthly_totals) * 100
        
        return df
    
    def generate_demographic_data(self):
        """Génère des données démographiques simulées"""
        demographics = []
        age_groups = ['13-17', '18-24', '25-34', '35-49', '50-64', '65+']
        
        for radio in self.radios:
            # Profils d'audience différents selon les radios
            if radio == 'Skyrock':
                profile = [0.35, 0.40, 0.15, 0.07, 0.02, 0.01]  # Très jeune
            elif radio in ['NRJ', 'Fun Radio', 'Virgin Radio']:
                profile = [0.15, 0.35, 0.25, 0.15, 0.07, 0.03]  # Jeune
            elif radio == 'France Inter':
                profile = [0.02, 0.08, 0.15, 0.25, 0.30, 0.20]  # Âgé
            else:  # Généralistes
                profile = [0.05, 0.15, 0.20, 0.25, 0.20, 0.15]  # Mixte
            
            for age_group, share in zip(age_groups, profile):
                demographics.append({
                    'radio': radio,
                    'tranche_age': age_group,
                    'part_audience': share * 100,
                    'audience_absolue': share * np.random.uniform(1, 3)  # en millions
                })
        
        return pd.DataFrame(demographics)
    
    def generate_time_slot_data(self):
        """Génère des données par créneau horaire"""
        time_slots = ['6h-9h', '9h-12h', '12h-14h', '14h-17h', '17h-20h', '20h-24h', '0h-6h']
        data = []
        
        for radio in self.radios:
            # Patterns différents selon les radios
            if radio == 'Skyrock':
                pattern = [0.12, 0.08, 0.10, 0.09, 0.15, 0.35, 0.11]  # Forte audience soir/nuit
            elif radio in ['NRJ', 'Fun Radio']:
                pattern = [0.20, 0.15, 0.12, 0.13, 0.18, 0.18, 0.04]  # Audience matin/soir
            else:
                pattern = [0.25, 0.18, 0.12, 0.15, 0.20, 0.08, 0.02]  # Audience journée
            
            for time_slot, share in zip(time_slots, pattern):
                data.append({
                    'radio': radio,
                    'creneau_horaire': time_slot,
                    'part_audience': share * 100,
                    'audience_relative': share * np.random.uniform(0.8, 1.2)
                })
        
        return pd.DataFrame(data)
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">📻 Dashboard Audience Radio - Analyse Skyrock</h1>', 
                   unsafe_allow_html=True)
        
        # Métriques principales pour Skyrock (année courante)
        current_year = 2024
        skyrock_data = self.df[(self.df['radio'] == 'Skyrock') & (self.df['annee'] == current_year)]
        previous_year_data = self.df[(self.df['radio'] == 'Skyrock') & (self.df['annee'] == current_year-1)]
        
        avg_audience = skyrock_data['audience_millions'].mean()
        avg_market_share = skyrock_data['part_marche_pourcent'].mean()
        
        prev_avg_audience = previous_year_data['audience_millions'].mean()
        prev_avg_market_share = previous_year_data['part_marche_pourcent'].mean()
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                label="Audience Moyenne Skyrock",
                value=f"{avg_audience:.2f}M",
                delta=f"{(avg_audience - prev_avg_audience):+.2f}M"
            )
        
        with col2:
            st.metric(
                label="Part de Marché Skyrock",
                value=f"{avg_market_share:.1f}%",
                delta=f"{(avg_market_share - prev_avg_market_share):+.1f}%"
            )
        
        with col3:
            # Position dans le classement
            current_rank = self.get_radio_ranking(current_year).index('Skyrock') + 1
            previous_rank = self.get_radio_ranking(current_year-1).index('Skyrock') + 1
            st.metric(
                label="Classement Skyrock",
                value=f"{current_rank}ème/8",
                delta=f"{(previous_rank - current_rank):+d}" if previous_rank != current_rank else None
            )
        
        with col4:
            # Audience maximale
            max_audience = skyrock_data['audience_millions'].max()
            st.metric(
                label="Audience Max Skyrock",
                value=f"{max_audience:.2f}M"
            )
        
        with col5:
            # Tendance
            trend = "📈 Hausse" if (avg_audience - prev_avg_audience) > 0 else "📉 Baisse"
            st.metric(
                label="Tendance",
                value=trend
            )

    def get_radio_ranking(self, year):
        """Retourne le classement des radios pour une année donnée"""
        year_data = self.df[self.df['annee'] == year]
        avg_audience = year_data.groupby('radio')['audience_millions'].mean()
        return avg_audience.sort_values(ascending=False).index.tolist()

    def create_evolution_charts(self):
        """Crée les graphiques d'évolution temporelle"""
        st.markdown('<h3 class="section-header">📈 Évolution de l\'Audience</h3>', 
                   unsafe_allow_html=True)
        
        # Préparation des données agrégées
        monthly_avg = self.df.groupby(['date', 'radio'])['audience_millions'].mean().reset_index()
        yearly_avg = self.df.groupby(['annee', 'radio'])['audience_millions'].mean().reset_index()
        market_share_avg = self.df.groupby(['annee', 'radio'])['part_marche_pourcent'].mean().reset_index()
        
        tab1, tab2, tab3 = st.tabs(["Évolution Mensuelle", "Évolution Annuelle", "Parts de Marché"])
        
        with tab1:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Graphique d'évolution mensuelle
                selected_radios = st.multiselect(
                    "Sélectionnez les radios à afficher",
                    self.radios,
                    default=['Skyrock', 'NRJ', 'Fun Radio', 'France Inter'],
                    key="monthly_radios"
                )
                
                filtered_data = monthly_avg[monthly_avg['radio'].isin(selected_radios)]
                
                fig = px.line(filtered_data, x='date', y='audience_millions', color='radio',
                             title="Évolution Mensuelle de l'Audience (2015-2024)",
                             labels={'audience_millions': 'Audience (Millions)', 'date': 'Date'},
                             color_discrete_map={'Skyrock': '#FF6B00'})
                
                fig.update_layout(height=500, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 📊 Points Clés")
                skyrock_data = monthly_avg[monthly_avg['radio'] == 'Skyrock']
                
                # Calcul de quelques indicateurs
                max_audience = skyrock_data['audience_millions'].max()
                min_audience = skyrock_data['audience_millions'].min()
                current_audience = skyrock_data[skyrock_data['date'] == skyrock_data['date'].max()]['audience_millions'].values[0]
                
                st.metric("Audience actuelle", f"{current_audience:.2f}M")
                st.metric("Maximum historique", f"{max_audience:.2f}M")
                st.metric("Minimum historique", f"{min_audience:.2f}M")
                
                # Tendance sur les 12 derniers mois
                last_year = skyrock_data.tail(12)
                trend = (last_year['audience_millions'].iloc[-1] - last_year['audience_millions'].iloc[0]) / last_year['audience_millions'].iloc[0] * 100
                st.metric("Tendance 12 mois", f"{trend:+.1f}%")
        
        with tab2:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Graphique d'évolution annuelle
                fig = px.line(yearly_avg, x='annee', y='audience_millions', color='radio',
                             title="Évolution Annuelle Moyenne de l'Audience",
                             labels={'audience_millions': 'Audience Moyenne (Millions)', 'annee': 'Année'},
                             color_discrete_map={'Skyrock': '#FF6B00'})
                
                fig.update_layout(height=500, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 🏆 Classement 2024")
                current_year_rank = yearly_avg[yearly_avg['annee'] == 2024].sort_values('audience_millions', ascending=False)
                
                for i, (_, row) in enumerate(current_year_rank.iterrows()):
                    emoji = "🎯" if row['radio'] == 'Skyrock' else "📻"
                    st.write(f"{i+1}. {emoji} {row['radio']}: {row['audience_millions']:.2f}M")
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Parts de marché par année
                fig = px.line(market_share_avg, x='annee', y='part_marche_pourcent', color='radio',
                             title="Évolution des Parts de Marché (%)",
                             labels={'part_marche_pourcent': 'Part de Marché (%)', 'annee': 'Année'},
                             color_discrete_map={'Skyrock': '#FF6B00'})
                
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Parts de marché actuelles (camembert)
                current_data = market_share_avg[market_share_avg['annee'] == 2024]
                
                fig = px.pie(current_data, values='part_marche_pourcent', names='radio',
                            title="Parts de Marché 2024",
                            color_discrete_sequence=px.colors.qualitative.Set3)
                
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)

    def create_comparison_analysis(self):
        """Crée l'analyse comparative entre les radios"""
        st.markdown('<h3 class="section-header">🔍 Analyse Comparative</h3>', 
                   unsafe_allow_html=True)
        
        # Données pour l'année courante
        current_year = 2024
        current_data = self.df[self.df['annee'] == current_year]
        
        tab1, tab2, tab3 = st.tabs(["Performance Relative", "Analyse Concurrentielle", "Positionnement"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Radar chart des performances
                performance_data = current_data.groupby('radio').agg({
                    'audience_millions': 'mean',
                    'part_marche_pourcent': 'mean'
                }).reset_index()
                
                # Normalisation pour le radar chart
                performance_data['audience_norm'] = (performance_data['audience_millions'] - performance_data['audience_millions'].min()) / (performance_data['audience_millions'].max() - performance_data['audience_millions'].min()) * 100
                performance_data['market_share_norm'] = (performance_data['part_marche_pourcent'] - performance_data['part_marche_pourcent'].min()) / (performance_data['part_marche_pourcent'].max() - performance_data['part_marche_pourcent'].min()) * 100
                
                fig = go.Figure()
                
                for radio in ['Skyrock', 'NRJ', 'Fun Radio']:
                    radio_data = performance_data[performance_data['radio'] == radio]
                    fig.add_trace(go.Scatterpolar(
                        r=[radio_data['audience_norm'].values[0], radio_data['market_share_norm'].values[0], 70, 60, 80],
                        theta=['Audience', 'Part Marché', 'Jeunesse', 'Innovation', 'Digital'],
                        fill='toself',
                        name=radio
                    ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 100])
                    ),
                    showlegend=True,
                    title="Profil de Performance - Radios Jeunes"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Heatmap de corrélation entre radios
                pivot_data = self.df.pivot_table(index='date', columns='radio', values='audience_millions')
                correlation_matrix = pivot_data.corr()
                
                fig = px.imshow(correlation_matrix,
                               title="Corrélation des Audiences entre Radios",
                               color_continuous_scale='RdBu_r',
                               aspect="auto")
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("""
                **Analyse des corrélations :**
                - 🔴 Corrélation positive : audiences qui évoluent ensemble
                - 🔵 Corrélation négative : audiences en opposition
                """)
        
        with tab2:
            st.subheader("Analyse Concurrentielle - Skyrock vs Concurrents")
            
            # Focus sur les radios jeunes
            young_radios = ['Skyrock', 'NRJ', 'Fun Radio', 'Virgin Radio']
            young_data = current_data[current_data['radio'].isin(young_radios)]
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Audience comparée
                fig = px.bar(young_data.groupby('radio')['audience_millions'].mean().reset_index(),
                            x='radio', y='audience_millions',
                            title="Audience Moyenne - Radios Jeunes",
                            color='radio',
                            color_discrete_map={'Skyrock': '#FF6B00'})
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Croissance annuelle
                growth_data = []
                for radio in young_radios:
                    current_avg = current_data[current_data['radio'] == radio]['audience_millions'].mean()
                    previous_avg = self.df[(self.df['radio'] == radio) & (self.df['annee'] == current_year-1)]['audience_millions'].mean()
                    growth = ((current_avg - previous_avg) / previous_avg) * 100
                    growth_data.append({'radio': radio, 'croissance': growth})
                
                growth_df = pd.DataFrame(growth_data)
                
                fig = px.bar(growth_df, x='radio', y='croissance',
                            title="Taux de Croissance Annuel (%)",
                            color='radio',
                            color_discrete_map={'Skyrock': '#FF6B00'})
                
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Positionnement Stratégique")
            
            # Graphique de positionnement (Audience vs Jeunesse)
            demographic_data = self.generate_demographic_data()
            youth_share = demographic_data[demographic_data['tranche_age'].isin(['13-17', '18-24'])].groupby('radio')['part_audience'].sum().reset_index()
            
            positioning_data = current_data.groupby('radio')['audience_millions'].mean().reset_index()
            positioning_data = positioning_data.merge(youth_share, on='radio')
            positioning_data['taille'] = positioning_data['audience_millions'] * 10  # Pour la taille des bulles
            
            fig = px.scatter(positioning_data, x='audience_millions', y='part_audience',
                           size='taille', color='radio', hover_name='radio',
                           title="Positionnement Stratégique des Radios",
                           labels={'audience_millions': 'Audience (Millions)', 'part_audience': 'Part Jeune Audience (%)'},
                           color_discrete_map={'Skyrock': '#FF6B00'})
            
            st.plotly_chart(fig, use_container_width=True)

    def create_demographic_analysis(self):
        """Analyse démographique de l'audience"""
        st.markdown('<h3 class="section-header">👥 Analyse Démographique</h3>', 
                   unsafe_allow_html=True)
        
        demographic_data = self.generate_demographic_data()
        time_slot_data = self.generate_time_slot_data()
        
        tab1, tab2, tab3 = st.tabs(["Pyramide des Âges", "Comportement d'Écoute", "Profil Typique"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Focus Skyrock
                skyrock_demo = demographic_data[demographic_data['radio'] == 'Skyrock']
                
                fig = px.bar(skyrock_demo, x='part_audience', y='tranche_age', orientation='h',
                            title="Répartition par Âge - Skyrock",
                            labels={'part_audience': 'Part d\'Audience (%)', 'tranche_age': 'Tranche d\'Âge'})
                
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Comparaison avec autres radios jeunes
                young_radios = ['Skyrock', 'NRJ', 'Fun Radio']
                young_demo = demographic_data[demographic_data['radio'].isin(young_radios)]
                
                fig = px.bar(young_demo, x='tranche_age', y='part_audience', color='radio',
                            title="Comparaison Démographique - Radios Jeunes",
                            labels={'part_audience': 'Part d\'Audience (%)', 'tranche_age': 'Tranche d\'Âge'},
                            barmode='group',
                            color_discrete_map={'Skyrock': '#FF6B00'})
                
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Audience par créneau horaire - Skyrock
                skyrock_time = time_slot_data[time_slot_data['radio'] == 'Skyrock']
                
                fig = px.bar(skyrock_time, x='creneau_horaire', y='part_audience',
                            title="Audience par Créneau Horaire - Skyrock",
                            labels={'part_audience': 'Part d\'Audience (%)', 'creneau_horaire': 'Créneau'})
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Heatmap des créneaux
                time_pivot = time_slot_data.pivot_table(index='radio', columns='creneau_horaire', values='part_audience')
                
                fig = px.imshow(time_pivot,
                               title="Audience par Créneau Horaire - Toutes Radios",
                               color_continuous_scale='Viridis',
                               aspect="auto")
                
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("👤 Profil Type de l'Auditeur Skyrock")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                **🎯 Profil Démographique :**
                - Âge médian : 22 ans
                - 60% d'hommes, 40% de femmes
                - CSP+ : 35%
                - Étudiants : 45%
                """)
            
            with col2:
                st.markdown("""
                **📱 Comportement d'Écoute :**
                - Écoute moyenne : 2h30/jour
                - Pic d'écoute : 20h-24h
                - Mobile : 65%
                - Voiture : 25%
                """)
            
            with col3:
                st.markdown("""
                **🎵 Préférences :**
                - Hip-Hop/Rap : 70%
                - Musique urbaine : 85%
                - Actualités jeunes : 60%
                - Émissions interactives : 75%
                """)
            
            # Graphique de profil complet
            profile_metrics = {
                'Catégorie': ['Fidélité', 'Engagement Digital', 'Activation Sociale', 'Recommandation'],
                'Score': [78, 65, 72, 68]
            }
            profile_df = pd.DataFrame(profile_metrics)
            
            fig = px.bar(profile_df, x='Score', y='Catégorie', orientation='h',
                        title="Score d'Engagement - Audience Skyrock",
                        color='Score', color_continuous_scale='Viridis')
            
            st.plotly_chart(fig, use_container_width=True)

    def create_strategic_recommendations(self):
        """Recommandations stratégiques basées sur l'analyse"""
        st.markdown('<h3 class="section-header">💡 Recommandations Stratégiques</h3>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Opportunités pour Skyrock")
            
            st.markdown("""
            <div class="metric-card">
            <h4>📱 Renforcement Digital</h4>
            <ul>
            <li>Développer l'application mobile avec fonctionnalités sociales</li>
            <li>Créer du contenu exclusif pour les plateformes numériques</li>
            <li>Optimiser le streaming pour la mobilité</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="metric-card">
            <h4>🎵 Contenu Musical</h4>
            <ul>
            <li>Diversifier légèrement la programmation musicale</li>
            <li>Mettre en avant les artistes émergents français</li>
            <li>Créer des partenariats avec l'industrie musicale</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="metric-card">
            <h4>👥 Engagement Communautaire</h4>
            <ul>
            <li>Développer les émissions interactives</li>
            <li>Créer des événements live avec l'audience</li>
            <li>Renforcer la présence sur les réseaux sociaux</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("📊 Analyse SWOT")
            
            swot_data = {
                'Catégorie': ['Forces', 'Faiblesses', 'Opportunités', 'Menaces'],
                'Éléments': [
                    "Image jeune et dynamique\nAudience très fidèle\nSpécialisation hip-hop\nFort engagement digital",
                    "Audience trop jeune\nDépendance à un style musical\nConcurrence numérique forte\nRessources limitées",
                    "Croissance du streaming\nNouvelles technologies audio\nPartenariats artistiques\nExpansion internationale",
                    "Concurrence des plateformes\nÉvolution des goûts musicaux\nRéglementation publicitaire\nÉrosion de l'audience jeune"
                ]
            }
            
            swot_df = pd.DataFrame(swot_data)
            
            # Affichage stylisé du SWOT
            for _, row in swot_df.iterrows():
                if row['Catégorie'] == 'Forces':
                    color = '#4CAF50'
                elif row['Catégorie'] == 'Faiblesses':
                    color = '#F44336'
                elif row['Catégorie'] == 'Opportunités':
                    color = '#2196F3'
                else:
                    color = '#FF9800'
                
                st.markdown(f"""
                <div style="border-left: 4px solid {color}; padding: 10px; margin: 10px 0; background-color: #f8f9fa;">
                <h4 style="color: {color}; margin: 0;">{row['Catégorie']}</h4>
                <p style="margin: 5px 0; white-space: pre-line;">{row['Éléments']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # KPI de performance recommandés
            st.subheader("🎯 Objectifs Recommandés")
            
            kpis = {
                'KPI': ['Audience 13-24 ans', 'Part de marché digitale', 'Taux d\'engagement mobile', 'Croissance annuelle'],
                'Actuel': ['2.8M', '15%', '65%', '-2%'],
                'Cible': ['3.2M', '22%', '80%', '+3%']
            }
            
            kpi_df = pd.DataFrame(kpis)
            st.dataframe(kpi_df, use_container_width=True)

    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ Contrôles d'Analyse")
        
        # Sélecteur d'année
        selected_year = st.sidebar.slider(
            "Année d'analyse principale",
            2015, 2024, 2024
        )
        
        # Filtre des radios à afficher
        st.sidebar.markdown("### 📻 Sélection des Radios")
        selected_radios = st.sidebar.multiselect(
            "Radios à inclure dans l'analyse",
            self.radios,
            default=['Skyrock', 'NRJ', 'Fun Radio', 'Virgin Radio', 'France Inter']
        )
        
        # Métriques rapides Skyrock
        st.sidebar.markdown("### 🎯 Snapshots Skyrock")
        skyrock_current = self.df[(self.df['radio'] == 'Skyrock') & (self.df['annee'] == selected_year)]
        
        if not skyrock_current.empty:
            avg_audience = skyrock_current['audience_millions'].mean()
            market_share = skyrock_current['part_marche_pourcent'].mean()
            
            st.sidebar.metric("Audience moyenne", f"{avg_audience:.2f}M")
            st.sidebar.metric("Part de marché", f"{market_share:.1f}%")
            
            # Classement
            ranking = self.get_radio_ranking(selected_year)
            position = ranking.index('Skyrock') + 1
            st.sidebar.metric("Position", f"{position}ème/8")
        
        # Liens rapides
        st.sidebar.markdown("### 🔗 Navigation Rapide")
        if st.sidebar.button("📈 Évolution"):
            st.session_state.active_tab = 0
        if st.sidebar.button("🔍 Comparaison"):
            st.session_state.active_tab = 1
        if st.sidebar.button("👥 Démographie"):
            st.session_state.active_tab = 2
        if st.sidebar.button("💡 Recommandations"):
            st.session_state.active_tab = 3
        
        return {
            'selected_year': selected_year,
            'selected_radios': selected_radios
        }

    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Initialisation de l'état de session
        if 'active_tab' not in st.session_state:
            st.session_state.active_tab = 0
        
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Évolution Temporelle", 
            "🔍 Analyse Comparative", 
            "👥 Analyse Démographique", 
            "💡 Recommandations"
        ])
        
        with tab1:
            self.create_evolution_charts()
        
        with tab2:
            self.create_comparison_analysis()
        
        with tab3:
            self.create_demographic_analysis()
        
        with tab4:
            self.create_strategic_recommendations()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        **Sources:** Données d'audience radio simulées 2015-2024  
        **Framework:** Streamlit • Plotly • Pandas  
        **Focus:** Analyse stratégique de l'audience Skyrock  
        *Données représentatives pour démonstration*
        """)

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = RadioAudienceDashboard()
    dashboard.run_dashboard()