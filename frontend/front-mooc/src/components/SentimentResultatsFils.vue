<template>
  <div class="list-group reponses">
    <a
      href="#"
      class="list-group-item list-group-item-action"
      v-for="(thread, index) in threads"
      :key="index"
    >
      <div class="d-flex w-100 justify-content-between thread">
        <router-link :to="`/analyse-fil/${thread.thread_id}`" ><h5 class="mb-1">{{ thread.thread_title }}</h5></router-link>
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
            font-size: 16px;
        }
        .reponses p{
            color: rgb(31, 31, 31)!important;
            font-size: 12px;
        }
        .thread{
            padding: 5px 10px;
            border-radius: 5px;
            background-color: rgb(255, 255, 255);
            margin-bottom: 3px;
            text-decoration: none;
        }
        .thread * {
            text-decoration: none;
        }
        
</style>