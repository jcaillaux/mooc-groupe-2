import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useGetAnswers = defineStore('GetAnswers', () => {
  const selectedAnswer = ref("")  // ⬅️ ceci est réactif

  return {
    selectedAnswer
  }
})
