<template>
  <BarreDeNavigation />
  <main>
    <h1>Comments</h1>
    <div class="comments">
      <Comment v-for="(comment, index) in comments" :key="index" v-bind="comment.content" />
    </div>
  </main>
</template>

<script>
import BarreDeNavigation from '../components/BarreDeNavigation.vue'
import Comment from '../components/comment.vue'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    Comment,
    BarreDeNavigation,
  },
  data() {
    return {
      threadId: null,
      comments: [],
    }
  },
  methods: {
    getComments() {
      axios.get('http://127.0.0.1:5000/api/thread/' + this.threadId)
        .then(response => {
          this.comments = response.data
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
