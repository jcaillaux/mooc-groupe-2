<template>
  <div class="list-group reponses">
    <a
      href="#"
      class="list-group-item list-group-item-action"
      v-for="(thread, index) in threads"
      :key="index"
    >
      <div class="d-flex w-100 justify-content-between">
        <router-link :to="`/fil-de-discussion/${thread.thread_id}`"><h5 class="mb-1">{{ thread.thread_title }}</h5></router-link>
        <!-- <small>Réponses : 4</small> -->
      </div>
    </a>
  </div>
</template>

<script>
export default {
  props: {
    threads: Array
  }
};
</script>

<style scoped>
/* Réponses */
        .reponses h5{
            color: rgb(21, 31, 101)!important;
            font-weight: 600;
        }
        .reponses p{
            color: rgb(31, 31, 31)!important;
            font-size: 12px;
        }
        
</style>