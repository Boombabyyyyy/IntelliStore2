<script setup>
import { RouterLink, RouterView } from 'vue-router'
import store from '../store'
import FooterItem from '../components/FooterItem.vue'
import Request from '../components/RequestItem.vue';
import fetchUtil from '../FetchUtil.js';
</script>

<template>
    <div class="bg-light py-3">
      <div class="container">
        <div class="row">
          <div class="col-md-12 mb-0"><router-link to="/">Home</router-link> <span class="mx-2 mb-0">/</span> <strong class="text-black">Shop</strong></div>
        </div>
      </div>
    </div>

    <div class="site-section">
  <div class="container">

    <div class="row mb-5">
      <div class="col-md-9 order-2">

        <div class="row">
          <div class="col-md-12 mb-5">
            <div class="float-md-center mb-4"><h2 class="text-black h5">
              <!-- Vue.js messages placeholder -->
            </h2></div>
            <div class="float-md-left mb-4"><h2 class="text-black h5">{{ shoptitle }}</h2></div>
            <div class="d-flex">
              <div class="btn-group mr-1 ml-md-auto">
                <button type="button" class="btn btn-secondary btn-sm dropdown-toggle" id="dropdownMenuReference" data-toggle="dropdown">CATEGORIES</button>
                <div class="dropdown-menu" aria-labelledby="dropdownMenuReference">
                  <a class="dropdown-item" href="/shop">All</a>
                  <!-- Vue.js categories loop placeholder -->
                </div>
              </div>
              <div class="btn-group">
                <button type="button" class="btn btn-secondary btn-sm dropdown-toggle" id="dropdownMenuReference" data-toggle="dropdown">SORT BY</button>
                <div class="dropdown-menu" aria-labelledby="dropdownMenuReference">
                  <a class="dropdown-item" href="#">Relevance</a>
                  <a class="dropdown-item" href="#">Name, A to Z</a>
                  <a class="dropdown-item" href="#">Name, Z to A</a>
                  <div class="dropdown-divider"></div>
                  <a class="dropdown-item" href="#">Price, low to high</a>
                  <a class="dropdown-item" href="#">Price, high to low</a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row mb-5">
          <!-- Vue.js products loop placeholder -->
          <!-- Each product should have its own Vue.js form -->
          <div v-for="product in products" :key="product.product_id" class="col-sm-6 col-lg-4 mb-4">
            <div class="block-4 text-center border">
              <form @submit.prevent="addtocart(product.product_id, product.qty)" :id="product.product_id" :name="product.product_id">
                <input type="hidden" id="product_id" name="product_id" :value="product.product_id">
                <input type="hidden" id="category_id" name="category_id" :value="product.category_id">
                <input type="hidden" id="stock" name="stock" :value="product.stock">
                <input type="hidden" id="name" name="name" :value="product.name">
                <figure class="block-4-image">
                  <router-link :to="'/shopsingle?product_id=' + product.product_id">
                    <img :src="'data:;base64,' + product.image" width="150" height="150" alt="Product Image" class="img-fluid">
                  </router-link>
                </figure>
                <div class="block-4-text p-4">
                  <h3><router-link :to="'/shopsingle?product_id=' + product.product_id">{{ product.name }}</router-link></h3>
                  <p class="mb-0">{{ product.description }}</p>
                  <p class="text-primary font-weight-bold">{{ product.price }} {{ product.unit }}</p>
                  <!-- Vue.js stock and quantity logic placeholder -->
                </div>
                <div v-if="product.stock != 0" class="input-group mb-3" style="max-width: 120px; text-align: center; margin-left: auto; margin-right: auto;" align="center">
                <p></p>
                <input v-model="product.qty" type="number" id="qty" name="qty" :max="product.stock" min="1" class="form-control " value="1" onkeydown="return false" placeholder="" aria-label="Example text with button addon" aria-describedby="button-addon1">
                <button type="submit" class="btn btn-primary btn-sm">ADD<span class="icon icon-cart-plus"></span></button>
                </div>
                <div v-if="product.stock == 0"  class="input-group mb-3" style="max-width: 120px; text-align: center; margin-left: auto; margin-right: auto;" align="center">
                <h6 class="text-danger">OUT OF STOCK!</h6>
                <p class="text-danger mb-0">Check back later!</p>
                </div>

              </form>
            </div>
          </div>
          <!-- End Vue.js products loop placeholder -->
        </div>
        <div v-if="products.length === 0" class="float-md-left mb-4"><h2 class="text-danger h5">No Results found!</h2></div>
      </div>

      <div class="col-md-3 order-1 mb-5 mb-md-0">
        <div class="border p-4 rounded mb-4">
          <h3 class="mb-3 h6 text-uppercase text-black d-block">Categories</h3>
          <ul class="list-unstyled mb-0">
            <li class="mb-1"><router-link to="/shop" class="d-flex"><span>View All</span> <span class="text-black ml-auto"></span></router-link></li>
            <li v-for="category in cats" :key="category.category_id" class="mb-1">
              <router-link :to="'/shopbycategory?category_id=' + category.category_id" class="d-flex">
                <span>{{ category.name }}</span>
                <span class="text-black ml-auto"></span>
              </router-link>
            </li>
          </ul>
        </div>
        <ul class="list-unstyled mb-0" v-if="messages.length > 0">
            <h5 v-for="(message, index) in messages" :key="index" class="text-success">{{ message }}</h5>
        </ul>
      </div>
    </div>

    <div class="row">
      <div class="col-md-12">
        <div class="site-section site-blocks-2">
          <div class="row justify-content-center text-center mb-5">
            <!-- Pagination or additional content goes here -->
          </div>
        </div>
      </div>
    </div>

  </div>
</div>
      <Request
      endpoint="product"
      method="GET"
      :headers="{ 'Content-Type': 'application/json' }"
      @response="handleProducts"
    />

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
      messages: [],
      shoptitle: "My Shop",
      products: [],
      user_id: store.state.currentUser,
      cats: [],
    };
  },
  mounted() {
    // Add any additional logic that should run after the component is mounted
  },
  components: {
    Request,
    FooterItem,
  },
  methods: {
    async addtocart(product_id, qty){
      const response = await fetchUtil({
          endpoint: "cartapi",
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          data: {"product_id": product_id.toString(), "qty": qty.toString()},
          user_id: this.user_id
        });
        console.log(response);
        this.messages = [response]
    },
    handleProducts(responseData) {
      // Handle the response data here
      // this.products=responseData;
      this.products = responseData.map(product => ({ ...product, qty: 1 }));
      console.log(responseData);
    },
    handleCats(responseData) {
      // Handle the response data here
      this.cats=responseData;
      console.log(responseData);
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
  