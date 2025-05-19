<template>
    <!-- Barre de navigation -->
    <header class="navbar-header">
        <div class="navbar-container">
            <h1 class="navbar-title">Mooc</h1>
            <!-- Tu peux ajouter ici des liens ou boutons plus tard -->
        </div>
    </header>
</template>



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
    justify-content: flex-start;
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

</style>