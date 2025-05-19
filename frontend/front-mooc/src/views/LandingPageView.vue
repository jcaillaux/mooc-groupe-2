<template>
    <main>
        <section class="section-ui">
            
        </section>
        <section class="sign-or-log">
            <Connexion />
        </section>
    </main>

</template>
<script>
import Connexion from '@/components/Connexion.vue';

export default {
    components:{
        Connexion,
    }
}

</script>
<style scoped>  
main {
    display: flex;
    flex-direction: row;
    margin: 0!important;
    padding: 0!important;
}
main section.section-ui{
    height: 100vh;
    display: inline-block;
    width: 50%;
    background-image: linear-gradient(to right, #9181F4, #5038ED);
}

section.sign-or-log{
    
    margin: auto;
}
</style>