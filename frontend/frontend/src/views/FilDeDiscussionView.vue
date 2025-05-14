<template>
  <div id="app">
    <h1>Comments</h1>
    <div class="comments">
      <Comment v-for="comment in comments" :key="comment.id" v-bind="comment" />
    </div>
  </div>
</template>

<script>
import commentsData from '../data/comments.js';

import Comment from '../components/comment.vue';

export default {
  name: 'App',
  components: {
    Comment,
  },
  computed: {
    comments() {
      return [...commentsData];
    },
  },
};
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
</style>
