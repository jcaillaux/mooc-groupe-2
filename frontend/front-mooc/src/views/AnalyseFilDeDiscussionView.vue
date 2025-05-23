<template>
  <BarreDeNavigation />
  <main>
    <h1>Fil</h1>
    <div class="comments" v-if="comments">
      <h4>{{ comments?.course_id }} / {{ comments?.title }}</h4>
      <Comment v-bind="comments" :key="index" />
    </div>
  </main>
</template>

<script>
import BarreDeNavigation from '../components/BarreDeNavigation.vue'
import Comment from '../components/comment.vue'
//import axios from 'axios'
import apiClient from '@/api/axios'

export default {
  name: 'App',
  components: {
    Comment,
    BarreDeNavigation,
  },
  data() {
    return {
      threadId: null,
      comments: null,
      index : 0,
    }
  },
  methods: {
    getComments() {
      console.log(this.threadId);
      apiClient.get('/api/analyzethreads/' + this.threadId)
        .then(response => {
          this.comments = response.data
          console.log(response.data)
        })
    },
  },
  mounted() {
    this.threadId = this.$route.params.id
    this.getComments()
  },
}
</script>


<style lang="css">
html {
  box-sizing: border-box;
}

*,
*:before,
*:after {
  box-sizing: inherit;
}

body {
  font-family: sans-serif;
}

main{
  margin: 50px;
}
</style>
