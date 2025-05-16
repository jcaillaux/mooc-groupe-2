import { defineStore } from 'pinia'
export const useCounterStore = defineStore('counter', {
  state: () => ({ 
    connected: false,
}),
persist: true // <-- C'est ça la magie !
})