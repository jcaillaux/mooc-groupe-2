<template>
    <!-- Barre de navigation -->
    <header class="navbar-header">
        <div class="navbar-container">
            <h1 class="navbar-title">Mooc</h1>
            <nav>
                <ul>
                        <li><router-link to="/">Questions/Réponses</router-link></li>
                        <li><router-link to="/sentiment">Analyse de sentiments</router-link></li>
                        <li><router-link to="/threads-clusts">Topics</router-link></li>
                        <li><router-link to="/users-clusts">Utilisateurs</router-link></li>
                        
                    </ul>
                <div class="deconnexion" >
                    
                    <svg :onclick="deconnexion" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-box-arrow-right" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0z"/>
                        <path fill-rule="evenodd" d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708z"/>
                    </svg>
                </div>
            </nav>
        </div>
    </header>
</template>

<script>
import { useCounterStore } from '../stores/data.js'
import { useAuthStore } from '@/stores/auth.js';
export default{
    methods:{
        deconnexion(){
            console.log("Vous êtes déconnecté");
            /*
            const store = useCounterStore();
            store.connected = false;
            */
            const authStore = useAuthStore()
            authStore.logout()
            this.$router.push({ name: 'landing-page' });
            console.log("Vous êtes déconnecté");
        }
    }
}
</script>

<style scoped>

header.navbar-header {
    background: #15171a;
    color: #fff;
    box-shadow: 0 2px 8px 0 rgba(20, 20, 35, 0.09);
    padding: 0;
    width: 100%;
}

.navbar-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 40px;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 32px;
}

.navbar-title {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -1px;
    margin: 0;
    color: #fff;
    /* Option: police monospace ou personnalisée pour le style tech */
    /* font-family: 'Fira Mono', 'Consolas', monospace; */
}
a {
    color:#fff;
    text-decoration: none;
}
a:hover{
    color: antiquewhite;
}
.deconnexion {
    cursor: pointer;
    
}

nav ul{
    display: flex;
    list-style: none;
    gap: 20px;
    margin: 0 50px;

}

nav ul li{
    text-decoration: none!important;
}
nav {
    display: flex;
}
</style>