<template>
  <h2>LOGIN</h2>
    <form @submit.prevent="login">
  <div class="form-group">
    <label for="email">Email address</label>
    <input type="text" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Enter email">

  </div>
  <div class="form-group">
    <label for="exampleInputPassword1">Password</label>
    <input type="password" class="form-control" id="password" placeholder="Password">
  </div>

  <button type="submit" class="btn btn-dark" :onclick=login >Submit</button>
</form>
</template>
<script>
import { useCounterStore } from '../stores/data.js' // Importation du store Pinia
import { useAuthStore } from '@/stores/auth.js';
//import axios from 'axios';

export default{
  data(){
    return{

    }
  },
  methods:{
    async login(){
        let id = document.getElementById("email").value;
        let password = document.getElementById("password").value;
        console.log(id);
        console.log(password);
        let data = {
            username: id,
            password: password
        }
      /*axios.post('/api/login', data, {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(response => {
            this.$router.push({ name: 'home' });
            console.log(response.data);
            const store = useCounterStore();
            store.connected = true;

            this.$router.push({ name: 'home' });
        })
        .catch(error => {
            console.error('There was an error!', error);
        });*/
      const authStore = useAuthStore()
      const success = await authStore.login(id, password)
      if (success){
        this.$router.push({ name: 'home' });
      }
    }
  },
  computed: {
    is_connected(){
      const authStore = useAuthStore()
      return authStore.isAuthenticated
    }
  },
  // Redirect if already logged in
  beforeMount() {
    if (this.is_connected) {
      this.$router.push({ name: 'home' })
    }else{
       this.$router.push({ name: 'landing-page' })
    }
  }
}
</script>
<style>



</style>
