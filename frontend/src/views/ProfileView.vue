<script setup>
import { RouterLink, RouterView } from 'vue-router'
import FooterItem from '../components/FooterItem.vue'
import store from '../store'
import fetchUtil from '../FetchUtil.js';
</script>

<template>
      <div class="bg-light py-3">
        <div class="container">
          <div class="row">
            <div class="col-md-12 mb-0"><a href="index.html"></a> <span class="mx-2 mb-0"></span> <strong class="text-black">PROFILE</strong></div>
          </div>
        </div>
      </div>

      <div v-if="userLoggedIn" class="site-section">
    <div class="container" style="align: center;">
      <div class="row">
        <div class="col-md-12"></div>
        <div class="col-md-6">
          <span class="d-block text-primary h6 text-uppercase" style="text-align: center;">Your Profile</span>
          <form @submit.prevent="updateUserProfile">
            <div class="p-3 p-lg-5 border">
              <div class="form-group row">
                <div class="col-md-12">
                  <label for="firstname" class="text-black">Firstname<span class="text-danger"></span></label>
                  <input type="text" class="form-control" id="firstname" v-model="user.firstname" required readonly>
                </div>
              </div>
              <div class="form-group row">
                <div class="col-md-12">
                  <label for="lastname" class="text-black">Lastname<span class="text-danger"></span></label>
                  <input type="text" class="form-control" id="lastname" v-model="user.lastname" readonly>
                </div>
              </div>
              <div class="form-group row">
                <div class="col-md-12">
                  <label for="username" class="text-black">Email (This will be your username)<span class="text-danger">*</span></label>
                  <input type="text" class="form-control" id="username" v-model="user.email" readonly>
                </div>
              </div>
              <!-- <div class="form-group row">
                <div class="col-md-12">
                  <label for="pw" class="text-black">Password<span class="text-danger">*</span></label>
                  <input type="password" class="form-control" id="pw" v-model="user.password" required placeholder="Enter new password here">
                </div>
              </div> -->
              <div class="form-group row">
                <div class="col-md-12">
                  <label for="mobile" class="text-black">Mobile Number (10 digit - Indian)<span class="text-danger"></span></label>
                  <input type="text" pattern="[789][0-9]{9}" class="form-control" id="mobile1" v-model="user.mobile" required readonly>
                </div>
              </div>
              <div class="form-group row">
                <!-- <div class="col-lg-12">
                  <button type="submit" class="btn btn-primary btn-lg btn-block">Update Profile and Password</button>
                </div> -->
                <div style="margin-left: auto; margin-right: auto; margin-top:20px;">
                  <button @click="signOut" type="button" class="btn btn-primary btn-lg btn-block">Sign Out</button>
                </div>
              </div>
            </div>
          </form>
        </div>
        <div class="col-md-5 ml-auto">
          <span class="d-block text-primary h6 text-uppercase" style="text-align: center;">Address List</span>
          <div class="col-md-18">
            <div v-for="address in addresses" :key="address.address_id" class="p-1 p-lg-1 border">
              <b>{{ address.mobile }}<p></p>{{ address.Address }}</b>
              <input type="hidden" :value="address.address_id">
            </div>
            <br><br>
            <span class="d-block text-primary h6 text-uppercase" style="text-align: center;">Add Address</span>
            <form @submit.prevent="addAddress">
              <input type="hidden" id="user_id" v-model="user.user_id">
              <div class="p-3 p-lg-5 border">
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="address1" class="text-black">Address Line 1<span class="text-danger">*</span></label>
                    <input type="text" class="form-control" id="address1" v-model="newAddress.address1" required>
                  </div>
                </div>
                <div class="form-group row">
                <div class="col-md-12">
                  <label for="mobile" class="text-black">Mobile Number (10 digit - Indian)<span class="text-danger">*</span></label>
                  <input type="text" pattern="[789][0-9]{9}" class="form-control" id="mobile" v-model="newAddress.mobile" required>
                </div>
              </div>
                <!-- Rest of the form fields -->
                <div class="form-group row">
                  <div class="col-lg-12">
                    <button type="submit" class="btn btn-primary btn-lg btn-block">Add Address</button>
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <br><br>
    <div class="container" style="align: center;">
      <h3 class="text-danger">Please login to view and manage your profile!</h3>
      <br>
      <router-link to="/login" style="margin-left: auto; margin-right: auto; margin-top:50px;">
        <button type="button" class="btn btn-primary">Click here to login</button>
      </router-link>
    </div>
    <br><br>
  </div>

    <FooterItem />
  </template>

<script>
export default {
  data() {
    return {
      userLoggedIn: true, // Set this to the actual condition for user login
      user: null,
      addresses: null,
      newAddress: {
        address1: "",
        mobile: "",
      },
    };
  },
  beforeMount(){
    this.checkCurrentUser();
  },
  watch: {
    $route: 'checkCurrentUser',
    '$store.state.currentUser': 'checkCurrentUser',
  },
  methods: {
    updateUserProfile() {
      // Implement the logic to update user profile
    },
    async addAddress() {
      // Implement the logic to add a new address
      const user_id = store.state.currentUser
      console.log(user_id);
      const addr = this.newAddress.address1
      const mobile = this.newAddress.mobile
      const response = await fetchUtil({
          endpoint: "address",
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          data: {"user_id": user_id, "address":addr, "mobile": mobile},
          user_id: user_id
        });
      console.log(response);
      location.reload();
    },
    signOut() {
      // Implement the logic to sign out the user
      const user_id = store.state.currentUser
      store.commit('clearUserTokens', {
      userId: user_id,
      });

      store.commit('clearUserData', {
      userId: user_id,
      });

      this.$router.push({ path: '/login' });
    },
    async checkCurrentUser(){
      const user_id = store.state.currentUser
      console.log("Profile Page: ", user_id)
      if(user_id !== null) {
        const storedUserData = store.state.users[user_id].userData
        // console.log(storedUserData)
        this.user = storedUserData
        // console.log(this.user.firstname);
        const response = await fetchUtil({
          endpoint: "address",
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          data: user_id,
          user_id: user_id
        });
        this.addresses = response
        // console.log(response);
      } 
    }
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
  