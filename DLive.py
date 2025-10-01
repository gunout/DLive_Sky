# dashboard_skyrock_live.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
import random
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Skyrock Live - Dashboard Audience Temps Réel",
    page_icon="📻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avec les couleurs Skyrock
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(45deg, #FF6B00, #FF8C00, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .live-badge {
        background: linear-gradient(45deg, #FF6B00, #FF8C00);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .metric-card {
        background: rgba(255, 107, 0, 0.1);
        padding: 1.2rem;
        border-radius: 15px;
        border-left: 5px solid #FF6B00;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    .section-header {
        color: #FF6B00;
        border-bottom: 3px solid #FF6B00;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .skyrock-gradient {
        background: linear-gradient(135deg, #FF6B00, #FF8C00);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

class SkyrockLiveDashboard:
    def __init__(self):
        self.current_time = datetime.now()
        self.initialize_data()
        
    def initialize_data(self):
        """Initialise les données de base"""
        # Données historiques récentes (dernières 48h)
        self.historical_data = self.generate_historical_data()
        
        # Données en temps réel
        self.live_data = {
            'current_listeners': 2850000,
            'peak_today': 3120000,
            'trend': 'up',
            'mobile_listeners': 65,
            'car_listeners': 22,
            'home_listeners': 13
        }
        
        # Programme actuel
        self.current_show = {
            'name': 'Le 6-9 avec Ali',
            'host': 'Ali',
            'start_time': '06:00',
            'end_time': '09:00',
            'listeners': 2850000,
            'engagement': 78
        }
        
        # Top titres en cours
        self.top_tracks = [
            {'artist': 'Gazo', 'title': 'MAMI WATA', 'plays': 42, 'trend': 'up'},
            {'artist': 'Ninho', 'title': 'DÉSOLÉ', 'plays': 38, 'trend': 'stable'},
            {'artist': 'Tiakola', 'title': 'PAS BÊTE', 'plays': 35, 'trend': 'up'},
            {'artist': 'SDM', 'title': 'BÉNÉFICE', 'plays': 32, 'trend': 'down'},
            {'artist': 'Fresh', 'title': 'CELINE 3X', 'plays': 29, 'trend': 'up'}
        ]
        
        # Données géographiques
        self.geo_data = {
            'Île-de-France': 850000,
            'Auvergne-Rhône-Alpes': 420000,
            'Provence-Alpes-Côte d\'Azur': 380000,
            'Occitanie': 320000,
            'Hauts-de-France': 280000,
            'Nouvelle-Aquitaine': 250000,
            'Grand Est': 220000,
            'Normandie': 180000,
            'Pays de la Loire': 160000,
            'Bretagne': 140000,
            'Bourgogne-Franche-Comté': 120000,
            'Centre-Val de Loire': 110000,
            'Corse': 40000,
            'Outre-Mer': 90000
        }

    def generate_historical_data(self):
        """Génère des données historiques pour les dernières 48 heures"""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=48)
        
        data = []
        current_time = start_time
        
        while current_time <= end_time:
            # Variation circadienne réaliste
            hour = current_time.hour
            if 6 <= hour <= 9:  # Morning show
                base_listeners = 2800000 + random.randint(-100000, 200000)
            elif 16 <= hour <= 19:  # Afternoon/evening
                base_listeners = 2600000 + random.randint(-150000, 150000)
            elif 20 <= hour <= 23:  # Prime time
                base_listeners = 3000000 + random.randint(-200000, 300000)
            elif 0 <= hour <= 5:  # Night
                base_listeners = 1200000 + random.randint(-200000, 300000)
            else:  # Day time
                base_listeners = 2200000 + random.randint(-150000, 150000)
            
            # Bruit aléatoire
            listeners = max(base_listeners + random.randint(-50000, 50000), 500000)
            
            data.append({
                'timestamp': current_time,
                'listeners': listeners,
                'hour': hour,
                'mobile_percent': random.randint(60, 70),
                'engagement': random.randint(65, 85)
            })
            
            current_time += timedelta(minutes=5)
        
        return pd.DataFrame(data)

    def update_live_data(self):
        """Met à jour les données en temps réel avec des variations réalistes"""
        # Variation basée sur l'heure actuelle
        current_hour = datetime.now().hour
        
        # Facteur saisonnier basé sur l'heure
        if 6 <= current_hour <= 9:  # Morning peak
            base_factor = 1.0
            volatility = 0.1
        elif 16 <= current_hour <= 19:  # Evening commute
            base_factor = 0.9
            volatility = 0.08
        elif 20 <= current_hour <= 23:  # Prime time
            base_factor = 1.1
            volatility = 0.12
        elif 0 <= current_hour <= 5:  # Night
            base_factor = 0.5
            volatility = 0.15
        else:  # Day time
            base_factor = 0.8
            volatility = 0.06
        
        # Mise à jour des auditeurs
        current_listeners = self.live_data['current_listeners']
        change = random.randint(-int(current_listeners * volatility), int(current_listeners * volatility))
        new_listeners = max(int(current_listeners * base_factor + change), 500000)
        
        self.live_data['current_listeners'] = new_listeners
        
        # Mise à jour du pic
        if new_listeners > self.live_data['peak_today']:
            self.live_data['peak_today'] = new_listeners
        
        # Mise à jour de la tendance
        if change > 0:
            self.live_data['trend'] = 'up'
        elif change < 0:
            self.live_data['trend'] = 'down'
        else:
            self.live_data['trend'] = 'stable'
        
        # Mise à jour des données géographiques (légères variations)
        for region in self.geo_data:
            current = self.geo_data[region]
            variation = random.randint(-int(current * 0.05), int(current * 0.05))
            self.geo_data[region] = max(current + variation, 10000)
        
        # Mise à jour du programme si nécessaire
        current_hour_minute = datetime.now().strftime('%H:%M')
        if current_hour_minute >= '09:00' and self.current_show['name'] == 'Le 6-9 avec Ali':
            self.current_show = {
                'name': 'Skyrock Non Stop',
                'host': 'Playlist Automatisée',
                'start_time': '09:00',
                'end_time': '12:00',
                'listeners': new_listeners,
                'engagement': random.randint(60, 75)
            }

    def display_live_header(self):
        """Affiche l'en-tête en temps réel"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.image("https://upload.wikimedia.org/wikipedia/fr/thumb/6/6b/Skyrock_logo.svg/1200px-Skyrock_logo.svg.png", 
                    width=150)
        
        with col2:
            st.markdown('<h1 class="main-header">SKYROCK LIVE</h1>', unsafe_allow_html=True)
            st.markdown('<div class="live-badge">🔴 EN DIRECT - MISES À JOUR TEMPS RÉEL</div>', 
                       unsafe_allow_html=True)
        
        with col3:
            current_time = datetime.now().strftime('%H:%M:%S')
            st.markdown(f"**🕐 {current_time}**")
            st.markdown(f"**📅 {datetime.now().strftime('%d/%m/%Y')}**")

    def display_live_metrics(self):
        """Affiche les métriques en temps réel"""
        st.markdown('<h3 class="section-header">📊 AUDIENCE LIVE</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            trend_icon = "📈" if self.live_data['trend'] == 'up' else "📉" if self.live_data['trend'] == 'down' else "➡️"
            st.metric(
                label=f"AUDITEURS ACTUELS {trend_icon}",
                value=f"{self.live_data['current_listeners']:,}".replace(',', ' '),
                delta=f"{random.randint(-50000, 50000):+,}" if self.live_data['trend'] != 'stable' else None
            )
        
        with col2:
            st.metric(
                label="PIC DU JOUR",
                value=f"{self.live_data['peak_today']:,}".replace(',', ' '),
                delta=None
            )
        
        with col3:
            st.metric(
                label="ÉCOUTE MOBILE",
                value=f"{self.live_data['mobile_listeners']}%",
                delta=f"{random.randint(-2, 2):+}%"
            )
        
        with col4:
            st.metric(
                label="ENGAGEMENT",
                value=f"{self.current_show['engagement']}%",
                delta=f"{random.randint(-3, 3):+}%"
            )
        
        with col5:
            # Estimation du classement en temps réel
            rank = random.randint(2, 4)  # Skyrock généralement 2ème-4ème
            st.metric(
                label="CLASSEMENT LIVE",
                value=f"{rank}ème",
                delta=f"{random.randint(-1, 1):+}" if random.random() > 0.7 else None
            )

    def create_live_charts(self):
        """Crée les graphiques en temps réel"""
        tab1, tab2, tab3 = st.tabs(["📈 Évolution Temps Réel", "🗺️ Audience Géographique", "🎵 Programme Actuel"])
        
        with tab1:
            self.create_realtime_chart()
        
        with tab2:
            self.create_geographic_chart()
        
        with tab3:
            self.create_current_show_dashboard()

    def create_realtime_chart(self):
        """Graphique d'évolution en temps réel"""
        # Données des dernières 6 heures
        six_hours_ago = datetime.now() - timedelta(hours=6)
        recent_data = self.historical_data[self.historical_data['timestamp'] >= six_hours_ago].copy()
        
        # Ajouter le point actuel
        current_point = {
            'timestamp': datetime.now(),
            'listeners': self.live_data['current_listeners'],
            'hour': datetime.now().hour,
            'mobile_percent': self.live_data['mobile_listeners'],
            'engagement': self.current_show['engagement']
        }
        recent_data = pd.concat([recent_data, pd.DataFrame([current_point])], ignore_index=True)
        
        # Créer le graphique
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Évolution des Auditeurs (6 dernières heures)', 'Taux d\'Engagement'),
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3]
        )
        
        # Graphique des auditeurs
        fig.add_trace(
            go.Scatter(
                x=recent_data['timestamp'],
                y=recent_data['listeners'],
                mode='lines+markers',
                name='Auditeurs',
                line=dict(color='#FF6B00', width=3),
                marker=dict(size=4)
            ),
            row=1, col=1
        )
        
        # Graphique d'engagement
        fig.add_trace(
            go.Scatter(
                x=recent_data['timestamp'],
                y=recent_data['engagement'],
                mode='lines',
                name='Engagement',
                line=dict(color='#00C851', width=2),
                fill='tozeroy',
                fillcolor='rgba(0, 200, 81, 0.1)'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            height=500,
            showlegend=True,
            hovermode='x unified'
        )
        
        fig.update_xaxes(title_text="Heure", row=2, col=1)
        fig.update_yaxes(title_text="Auditeurs", row=1, col=1)
        fig.update_yaxes(title_text="Engagement (%)", range=[50, 100], row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True)

    def create_geographic_chart(self):
        """Carte de l'audience géographique"""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Préparation des données pour la carte de France
            regions_data = {
                'Région': list(self.geo_data.keys()),
                'Auditeurs': list(self.geo_data.values()),
                'Part (%)': [round((count / sum(self.geo_data.values())) * 100, 1) for count in self.geo_data.values()]
            }
            
            df_regions = pd.DataFrame(regions_data)
            
            # Carte choroplèthe (simplifiée)
            fig = px.choropleth(
                df_regions,
                geojson=None,  # Normalement on utiliserait un GeoJSON de la France
                locations='Région',
                color='Auditeurs',
                hover_name='Région',
                hover_data={'Auditeurs': True, 'Part (%)': True},
                color_continuous_scale='Oranges',
                title="Audience par Région"
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🏆 Top 5 Régions")
            top_regions = sorted(self.geo_data.items(), key=lambda x: x[1], reverse=True)[:5]
            
            for i, (region, count) in enumerate(top_regions, 1):
                percentage = (count / sum(self.geo_data.values())) * 100
                st.markdown(f"""
                <div class="metric-card">
                    <h4>#{i} {region}</h4>
                    <h3>{count:,}</h3>
                    <p>{percentage:.1f}% du total</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Répartition par type d'écoute
            st.subheader("📱 Support d'Écoute")
            listen_types = {
                'Mobile': self.live_data['mobile_listeners'],
                'Voiture': self.live_data['car_listeners'],
                'Domicile': self.live_data['home_listeners']
            }
            
            fig_pie = px.pie(
                values=list(listen_types.values()),
                names=list(listen_types.keys()),
                color_discrete_sequence=['#FF6B00', '#FF8C00', '#FFA500']
            )
            fig_pie.update_layout(height=250)
            st.plotly_chart(fig_pie, use_container_width=True)

    def create_current_show_dashboard(self):
        """Dashboard de l'émission en cours"""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Informations sur l'émission en cours
            st.markdown(f"""
            <div class="skyrock-gradient">
                <h2>🎙️ {self.current_show['name']}</h2>
                <h3>Animateur: {self.current_show['host']}</h3>
                <p>🕐 {self.current_show['start_time']} - {self.current_show['end_time']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Graphique d'engagement de l'émission
            engagement_data = []
            show_start = datetime.now().replace(hour=int(self.current_show['start_time'].split(':')[0]), 
                                              minute=0, second=0, microsecond=0)
            
            for i in range(12):  # 12 segments de 15 minutes
                time_point = show_start + timedelta(minutes=i*15)
                engagement = random.randint(65, 85)
                engagement_data.append({'time': time_point, 'engagement': engagement})
            
            df_engagement = pd.DataFrame(engagement_data)
            
            fig = px.area(df_engagement, x='time', y='engagement',
                         title="Engagement pendant l'émission",
                         labels={'engagement': 'Taux d\'Engagement (%)', 'time': 'Heure'})
            
            fig.update_traces(fillcolor='rgba(255, 107, 0, 0.3)', line_color='#FF6B00')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎵 TOP 5 EN COURS")
            
            for i, track in enumerate(self.top_tracks[:5], 1):
                trend_icon = "🔺" if track['trend'] == 'up' else "🔻" if track['trend'] == 'down' else "➡️"
                st.markdown(f"""
                <div style="background: rgba(255,107,0,0.1); padding: 0.8rem; border-radius: 10px; margin: 0.5rem 0;">
                    <strong>#{i} {trend_icon}</strong><br>
                    <strong>{track['artist']}</strong><br>
                    <small>{track['title']}</small><br>
                    <small>📻 {track['plays']} diffusions</small>
                </div>
                """, unsafe_allow_html=True)
            
            # Statistiques sociales
            st.subheader("📱 ACTIVITÉ SOCIALE")
            social_metrics = {
                'Instagram': f"{random.randint(500, 2000):,}",
                'Twitter': f"{random.randint(300, 1500):,}",
                'TikTok': f"{random.randint(1000, 5000):,}",
                'Skyrock App': f"{random.randint(5000, 15000):,}"
            }
            
            for platform, count in social_metrics.items():
                st.metric(label=platform, value=count)

    def create_social_feed(self):
        """Flux social en temps réel"""
        st.markdown('<h3 class="section-header">💬 FLUX SOCIAL LIVE</h3>', unsafe_allow_html=True)
        
        # Messages simulés
        messages = [
            {"user": "Sarah_23", "message": "🔥🔥 Gazo qui passe en boucle sur Skyrock ! #MamiWata", "time": "2 min", "likes": 42},
            {"user": "Mike_THE_GOAT", "message": "Le 6-9 avec Ali c'est le meilleur réveil 🎧", "time": "4 min", "likes": 38},
            {"user": "LéaFromParis", "message": "Qui écoute Skyrock en cours ? 🙋‍♀️", "time": "7 min", "likes": 29},
            {"user": "RapAddict", "message": "SDM qui cartonne en ce moment sur Skyrock 💯", "time": "12 min", "likes": 51},
            {"user": "SkyrockFan93", "message": "Le son de Tiakola passe trop en ce moment !", "time": "15 min", "likes": 33}
        ]
        
        # Ajouter un nouveau message aléatoire
        if random.random() > 0.7:
            new_users = ["Mathis_75", "Clara_Love", "RapEnForce", "Skyrock4Ever", "UrbanMusic"]
            new_messages = [
                "Skyrock meilleure radio sans discussion 🎯",
                "Ali trop drôle ce matin 😂",
                "Qui va au concert de Ninho ?",
                "Skyrock devrait passer plus de Fresh !",
                "Le mix de ce matin est incroyable 🎧"
            ]
            
            messages.insert(0, {
                "user": random.choice(new_users),
                "message": random.choice(new_messages),
                "time": "Maintenant",
                "likes": random.randint(10, 50)
            })
        
        # Afficher le flux
        for msg in messages[:8]:  # Afficher les 8 premiers messages
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"""
                    **{msg['user']}** · {msg['time']}  
                    {msg['message']}  
                    ❤️ {msg['likes']}
                    """)
                
                with col2:
                    if st.button("❤️", key=msg['user']):
                        msg['likes'] += 1
                        st.rerun()
                
                st.markdown("---")

    def create_technical_monitoring(self):
        """Monitoring technique en temps réel"""
        st.markdown('<h3 class="section-header">⚙️ MONITORING TECHNIQUE</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Qualité du stream
            stream_quality = random.randint(95, 100)
            st.metric(
                label="QUALITÉ STREAM",
                value=f"{stream_quality}%",
                delta=None
            )
            st.progress(stream_quality / 100)
        
        with col2:
            # Latence
            latency = random.randint(50, 200)
            status = "🟢 Bon" if latency < 100 else "🟡 Moyen" if latency < 150 else "🔴 Élevé"
            st.metric(
                label="LATENCE MOYENNE",
                value=f"{latency}ms",
                delta=status
            )
        
        with col3:
            # Serveurs
            servers_online = random.randint(18, 20)
            st.metric(
                label="SERVEURS ONLINE",
                value=f"{servers_online}/20",
                delta=None
            )
        
        with col4:
            # Bandwidth
            bandwidth = random.randint(800, 1200)
            st.metric(
                label="BANDE PASSANTE",
                value=f"{bandwidth} Mbps",
                delta=None
            )
        
        # Graphique de charge serveur
        server_load = [random.randint(40, 90) for _ in range(10)]
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = server_load[-1],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "CHARGE SERVEUR"},
            delta = {'reference': server_load[-2]},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#FF6B00"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    def run_dashboard(self):
        """Exécute le dashboard en temps réel"""
        # Mise à jour des données live
        self.update_live_data()
        
        # Header
        self.display_live_header()
        
        # Métriques principales
        self.display_live_metrics()
        
        # Graphiques principaux
        self.create_live_charts()
        
        # Sections supplémentaires
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.create_social_feed()
        
        with col2:
            self.create_technical_monitoring()
        
        # Auto-refresh
        st.markdown("---")
        refresh_rate = st.slider("Fréquence de rafraîchissement (secondes)", 5, 60, 30)
        
        if st.button("🔄 Rafraîchir Maintenant"):
            st.rerun()
        
        # Simulation de mise à jour automatique
        time.sleep(refresh_rate)
        st.rerun()

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = SkyrockLiveDashboard()
    dashboard.run_dashboard()