<script setup>
import { RouterLink, RouterView } from 'vue-router'
import FooterItem from '../components/FooterItem.vue'
import store from '../store'
import fetchUtil from '../FetchUtil.js';
</script>

<template>
  <div>
    <div class="bg-light py-3">
      <div class="container">
        <div class="row">
          <div class="col-md-12 mb-0"><router-link to="/">Home</router-link> <span class="mx-2 mb-0">/</span> <strong class="text-black">REGISTER</strong></div>
        </div>
      </div>
    </div>

    <div class="site-section">
      <div class="container" style="align: center;">
        <div class="row">
          <div class="col-md-12"></div>
          <div class="col-md-6">
            <form @submit.prevent="signUpUser">
              <div class="p-3 p-lg-5 border">
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="firstname" class="text-black">Firstname<span class="text-danger">*</span></label>
                    <input v-model="firstname" type="text" class="form-control" id="firstname" name="firstname" required>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="lastname" class="text-black">Lastname<span class="text-danger"></span></label>
                    <input v-model="lastname" type="text" class="form-control" id="lastname" name="lastname">
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="username" class="text-black">Email (This will be your username)<span class="text-danger">*</span></label>
                    <input v-model="username" type="text" class="form-control" id="username" name="username" required>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="pw" class="text-black">Password<span class="text-danger">*</span></label>
                    <input v-model="password" type="password" class="form-control" id="pw" name="pw" required>
                  </div>
                </div>
                <div class="form-group row">
                  <div class="col-md-12">
                    <label for="mobile" class="text-black">Mobile Number (10 digit - Indian)<span class="text-danger">*</span></label>
                    <input v-model="mobile" type="text" pattern="[789][0-9]{9}" class="form-control" id="mobile" name="mobile" required>
                  </div>
                </div>
                <div class="form-group row">
                <div class="col-md-12">
                  <div class="form-check">
                    <input
                      v-model="isStoreManager"
                      type="checkbox"
                      class="form-check-input"
                      id="storeManagerCheckbox"
                    />
                    <label class="form-check-label" for="storeManagerCheckbox">
                      I'm a store manager
                    </label>
                  </div>
                </div>
              </div>

              <!-- Additional field for employee ID (conditionally rendered) -->
              <div v-if="isStoreManager" class="form-group row">
                <div class="col-md-12">
                  <label for="employeeId" class="text-black">Employee ID (for verification)<span class="text-danger">*</span></label>
                  <input
                    v-model="employeeId"
                    type="text"
                    class="form-control"
                    id="employeeId"
                    name="employeeId"
                    required
                  />
                  <label for="employeeId" class="text-black"><span class="text-danger">Please note that until approval by Admin, your account will not gain access to manager panel.</span></label>
                </div>
              </div>
                <div class="form-group row">
                  <div class="col-lg-12">
                    <button type="submit" class="btn btn-primary btn-lg btn-block">Sign Up</button>
                  </div>
                  <router-link to="/login" style="margin-left: auto; margin-right: auto; margin-top:20px;"><button type="button" class="btn btn-link btn-sm">Already a User? Log in Now!</button></router-link>
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
      isStoreManager: false,
      employeeId: '',
      firstname: '',
      lastname: '',
      username: '',
      password: '',
      mobile: '',
    };
  },
  methods: {
    generateRandomString(length) {
      const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      let result = '';

      for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        result += characters.charAt(randomIndex);
      }

      return result;
    },
    async signUpUser() {
      var ismgr = 0
      if(this.isStoreManager){
        ismgr = 1
      }
      const randomString = this.generateRandomString(8);
      const response = await fetchUtil({
          endpoint: "newuser",
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          data: {"username": this.username, "mobile": this.mobile, "firstname": this.firstname, "lastname": this.lastname, "pw": this.password, "ismgrequest": ismgr, "employee_id": this.employeeId, fs_uniquifier: randomString},
        });
      console.log(response);
      this.$router.push({ path: '/login', query: { message: "Sign Up succesfull, please login!" } });
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
  