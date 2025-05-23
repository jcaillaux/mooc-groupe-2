<template>
    <BarreDeNavigation/>
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
h1 {
    display: flex;
    flex-direction: column;
    align-items: center;
    color: rgb(21, 31, 101)!important;
}
</style>