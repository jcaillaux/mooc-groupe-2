<template>
    <BarreDeNavigation/>
    <fieldset>
        <legend>Clusterings :</legend>
        <div>
        <label for="FDD">Fils de discussions</label>
        <input type="radio" id="FDD" value="FDD" v-model="selectedCourse">
        <label for="USERS">Users</label>
        <input type="radio" id="USERS" value="USERS" v-model="selectedCourse">
        </div>
    </fieldset>


    
    <TopicsClusts/>
    
</template>

<script>
import TopicsClusts from "../components/BertTopic.vue";
import BarreDeNavigation from "../components/BarreDeNavigation.vue";
export default{
    components:{
        TopicsClusts,
        BarreDeNavigation
    },
}
</script>

<style scoped>  
fieldset div {
    display: flex;
    flex-direction: row;
    gap: 20px
}
</style>