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