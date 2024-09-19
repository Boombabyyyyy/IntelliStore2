<script setup>
import { RouterLink, RouterView } from 'vue-router'
import FooterItem from '../components/FooterItem.vue'
import Request from '../components/RequestItem.vue';
import store from '../store'
import fetchUtil from '../FetchUtil.js';
</script>

<template>
    <div class="bg-light py-3">
      <div class="container">
        <div class="row">
          <div class="col-md-12 mb-0"><a href="index.html">Home</a> <span class="mx-2 mb-0">/</span> <strong class="text-black">Edit Product</strong></div>
        </div>
      </div>
    </div>  

    <div class="site-section">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <form @submit.prevent="updateProduct" method="post" enctype="multipart/form-data">
            <h2 class="h3 mb-3 text-black">Update Product</h2>
            <div class="p-3 p-lg-5 border">
              <div class="form-group row">
                <div class="col-md-12">
                  <label for="name" class="text-black">Product name <span class="text-danger">*</span></label>
                  <input v-model="newProduct.name" type="name" class="form-control" id="name" name="name" required>
                </div>
              </div>
              <div class="form-group row">
                <div class="col-md-6">
                  <label for="price" class="text-black">Price <span class="text-danger">*</span></label>
                  <input v-model="newProduct.price" type="number" class="form-control" id="price" name="price" required>
                </div>
                <div class="col-md-6">
                  <label for="unit" class="text-black">Unit <span class="text-danger">*</span></label>
                  <select v-model="newProduct.unit" class="form-control" id="unit" name="unit" required>
                    <option v-for="unit in units" :value="unit">{{ unit }}</option>
                  </select>
                </div>
              </div>
              <div class="form-group row">
                <div class="col-md-12">
                  <label for="mfg" class="text-black">Date of manufacturing<span class="text-danger"></span></label>
                  <input v-model="newProduct.mfg" type="text" class="form-control" id="mfg" name="mfg" placeholder="">
                </div>
              </div>
              <div class="form-group row">
                <div class="col-md-12">
                  <label for="exp" class="text-black">Date of Expiry</label>
                  <input v-model="newProduct.exp" type="text" class="form-control" id="exp" name="exp">
                </div>
              </div>
              <div class="form-group row">
                <div class="col-md-12">
                  <label for="description" class="text-black">Description</label>
                  <textarea v-model="newProduct.description" name="description" id="description" cols="30" rows="4" class="form-control"></textarea>
                </div>
              </div>
              <div class="form-group row">
                <div class="col-md-12">
                  <label for="category_id" class="text-black">Category: </label><span class="text-danger">*</span>
                  <select v-model="newProduct.category_id" name="category_id" id="category_id" class="form-control">
                    <option v-for="category in categories" :value="category.category_id">{{ category.name }}</option>
                  </select>
                </div>
              </div>
              <div class="form-group row">
                <div class="col-md-12">
                  <label for="image" class="text-black">Product Image</label><span class="text-danger">* (Do not choose a file if you wish to keep same image)</span>
                  <input accept=".jpg, .jpeg, .png, .gif" @change="onFileChange" type="file" name="image" class="form-control" id="image">
                </div>
              </div>
              <div class="form-group row">
                <div class="col-md-12">
                  <label for="stock" class="text-black">Current Available Stock <span class="text-danger">*</span></label>
                  <input v-model="newProduct.stock" type="number" class="form-control" id="stock" name="stock" required>
                </div>
              </div>
              <div class="form-group row">
                <div class="col-lg-12">
                  <input type="submit" class="btn btn-primary btn-lg btn-block" value="Update Product">
                </div>
              </div>
            </div>
          </form>
        </div>
    </div>
    </div>
    <!-- Rest of your code... -->
      </div>
      <Request
          endpoint="category"
          method="GET"
          :headers="{ 'Content-Type': 'application/json' }"
          @response="handleCats"
        />
  <FooterItem />
</template>

<script>
export default {
  data() {
    return {
      user_id: store.state.currentUser,
      newProduct: {
        name: '',
        price: '',
        unit: '',
        mfg: '',
        exp: '',
        description: '',
        category_id: '',
        stock: '',
        image: null, // File will be stored here
      },
      categories: [],
      units: ['Rs/Unit', 'Rs/Kg', 'Rs/Dozen', 'Rs/Litre'],
    };
  },
  beforeMount(){
    this.getproduct();
  },
  methods: {
   async getproduct(){
    if(this.$route.query.product_id) {
      const ep = "product/" + this.$route.query.product_id
      const response = await fetchUtil({
            endpoint: ep,
            method: 'GET',
            user_id: this.user_id
          });
      this.newProduct = response
    }
   },
  onFileChange(event) {
    const reader = new FileReader();
    // console.log(event.target.files[0]);
    reader.readAsDataURL(event.target.files[0]);
    reader.onload = (e) => {
    // Update the imageData with the base64 representation of the image
    const imageData = e.target.result.replace(/^data:image\/(png|jpg|jpeg);base64,/, '');
    // console.log(imageData)
    this.newProduct.image=imageData
    };
  },
   async updateProduct(){
    const response = await fetchUtil({
          endpoint: "product",
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          data: this.newProduct,
          user_id: this.user_id
        });
      console.log(response);
      const keyword = this.newProduct.name
      this.$router.push({
        path: 'shopbycategory',
        query: { keyword: keyword }
      });
      // location.reload();
   },
   handleCats(responseData) {
      // Handle the response data here
      // this.categories=responseData;
      this.categories = responseData.map(category => ({ ...category, editMode: false }));
      console.log(responseData);
    },
  },
}
</script>

<style scoped>
/* Add your component-specific styles here */
</style>


  
  <style>
  @media (min-width: 1024px) {
    .about {
      min-height: 100vh;
      display: flex;
      align-items: center;
    }
  }
  </style>
  