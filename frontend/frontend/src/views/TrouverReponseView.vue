<template>
    <BarreDeNavigation />
    <main>
        <!-- Input pour poser une question -->
        <div class="mb-3 question-form">
            <label for="exampleFormControlTextarea1" class="form-label">Posez votre question :</label>
            <div>
                <input type="text"  class="form-control" id="exampleFormControlInput1" placeholder="">
                <button type="button" class="btn btn-dark">Valider</button>
            </div>
        </div>
        <!-- Liste des résultats -->
        <ResultatsFils/>
    </main>
</template>
<script scoped>
import BarreDeNavigation from "../components/BarreDeNavigation.vue";
import ResultatsFils from "../components/ResultatsFils.vue";
export default {
    components: {
        BarreDeNavigation,
        ResultatsFils
    }
}
</script>

<style scoped>
/* Input pour poser une question */
        main{
            padding: 50px;
        }
        .question-form{
            max-width: 500px;
        }
        .question-form div{
            display: flex;
            gap: 10px;
        }
</style>