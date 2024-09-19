<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import FooterItem from '../components/FooterItem.vue'
import fetchUtil from '../FetchUtil.js';
import store from '../store.js';
const router = useRouter();
</script>

<template>
  <div>
    <div class="bg-light py-3">
      <div class="container">
        <div class="row">
          <div class="col-md-12 mb-0"><router-link to="/">Home</router-link> <span class="mx-2 mb-0">/</span> <strong class="text-black">LOGIN</strong></div>
        </div>
      </div>
    </div>

    <div class="site-section">
      <div class="container" style="align: center;">
        <div class="row">
          <div class="col-md-12"></div>
          <div class="col-md-6">
            <form @submit.prevent="loginUser">
              <div class="p-3 p-lg-5 border">
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="username" class="text-black">Username (email)<span class="text-danger">*</span></label>
                    <input v-model="username" type="text" class="form-control" id="username" name="username">
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="pw" class="text-black">Password<span class="text-danger">*</span></label>
                    <input v-model="password" type="password" class="form-control" id="pw" name="pw">
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-lg-12">
                    <button type="submit" class="btn btn-primary btn-lg btn-block">Sign in</button>
                  </div>
                  <ul class="flashes" v-if="messages.length > 0">
                    <li v-for="(message, index) in messages" :key="index" class="text-danger">{{ message }}</li>
                  </ul>
                  <router-link to="/register" style="margin-left: auto; margin-right: auto; margin-top:20px;"><button type="button" class="btn btn-link btn-sm">Not a user yet? Sign Up Now!</button></router-link>
                </div>
              </div>
            </form>
          </div>

          <div class="col-md-5 ml-auto">
            <div class="p-4 border mb-3">
              <span class="d-block text-primary h6 text-uppercase" style="text-align: center;">Welcome to IntelliStore</span>
              <img src="../assets/images/store.jpg" class="img-thumbnail" alt="Grocery store">
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <FooterItem />
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      messages: [],
    };
  },
  mounted() {
    // Add any additional logic that should run after the component is mounted
    
    if(this.$route.query.message) {
      this.messages = [this.$route.query.message];
    }
    
  },
  methods: {
    async loginUser() {
      try {
    // Make a request to the 'loginuser' endpoint
    const response = await fetchUtil({
      endpoint: 'loginuser',
      method: 'POST',
      data: { username: this.username, password: this.password },
      headers: { 'Content-Type': 'application/json' }
    });

    // console.log(response.user_id, response.tokens[0].access, response.tokens[0].refresh);

    // Update Vuex store with user tokens
    store.commit('setUserTokens', {
      userId: response.user_id,
      jwtToken: response.tokens[0].access,
      refresh_token: response.tokens[0].refresh,
    });

    const storedUserData = store.state.users[response.user_id];
    console.log('JWT tokens set for User ID:', response.user_id);
    // console.log('JWT Token:', storedUserData.jwtToken);
    // console.log('Refresh Token:', storedUserData.refreshToken);
    
    const userendpoint = 'user/' + response.user_id

    const response2 = await fetchUtil({
      endpoint: userendpoint,
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      user_id: response.user_id
    });

    console.log(response2);

    store.commit('setUserData', {
      userId: response.user_id,
      userData: response2
    });

    const storedUserData2 = store.state.users[response.user_id];

    console.log(`${storedUserData2.userData.firstname} ${storedUserData2.userData.lastname} - user ID: ${storedUserData2.userData.user_id} successfully logged in`);

    // Redirect to a different route (e.g., home) after successful login
    this.$router.push({ path: '/' });
  } catch (error) {
    // Handle login failure, update messages or show an error to the user
    this.messages = ['Login failed. Please check your credentials.'];
    console.log(error);
  }

    },
    components: {
    FooterItem,
  },
  },

};
</script>

  <style>
  @media (min-width: 1024px) {
    .about {
      min-height: 100vh;
      display: flex;
      align-items: center;
    }
  }
  </style>
  