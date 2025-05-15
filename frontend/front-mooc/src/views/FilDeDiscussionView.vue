<template>
  <div id="app">
    <h1>Comments</h1>
    <div class="comments">
      <Comment v-for="(comment, index) in comments" :key="index" v-bind="comment.content" />
    </div>
  </div>
</template>

<script>
import commentsData from '../data/mooc.sample.json';

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
