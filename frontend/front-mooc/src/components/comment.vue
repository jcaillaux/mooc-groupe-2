<template>
  <div>
    <div class="comment" :class="{ reply: type === 'reply' }">
      <header>
        <h3>{{ username }}</h3> <!-- changé de author à username -->
       
      </header>
      <div v-html="body" class="comment-body" />
      <p class="timestamp"></p>
    </div>
    <div v-if="children.length" class="comment-replies">
      <Comment
        v-for="reply in children"
        :key="reply.id"
        v-bind="reply"
        type="reply"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'Comment',
  props: {
    username: { type: String, required: true },
    body: { type: String, required: true },
    children: { type: Array, required: true },
    
    type: { type: String, required: false, default: 'comment' },
  }
};
</script>

<style lang="css" scoped>
.comment {
  border: 1px solid DodgerBlue;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  padding: 1.5rem;
}

.comment.reply {
  position: relative;
}

.comment.reply:before {
  background-color: Silver;
  content: '';
  height: 1px;
  left: -2.5rem;
  position: absolute;
  top: 50%;
  width: 0.75rem;
}

h3,
p {
  margin: 0;
}

header {
  align-items: center;
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

svg {
  fill: SlateGray;
}

.comment-body {
  margin-bottom: 0.375rem;
}

.timestamp {
  color: DimGray;
  font-size: 0.8rem;
}

.comment-replies {
  padding-left: 3.5rem;
  position: relative;
}

.comment-replies:before {
  background-color: SlateGray;
  content: '';
  height: calc(100% + 1rem);
  left: 1rem;
  position: absolute;
  top: 0;
  width: 1px;
}

.comment-replies:last-child:before {
  height: calc(100% - 1rem);
}
</style>
