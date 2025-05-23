<template>
    <iframe
  :src="iframeUrl"
  width="100%"
  height="500px"
  style="border:none;"
></iframe>

</template>
<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const iframeUrl = computed(() => {
  return `/api/users/all?token=${authStore.token}`
})
</script>
<style scoped>
</style>