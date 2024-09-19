<script setup>
import FooterItem from '../components/FooterItem.vue'
import Request from '../components/RequestItem.vue';
</script>

<template>
  <main>
    <div class="site-wrap">
<div style="
    background-image: url('https://i.postimg.cc/9fytN8Qk/hero.jpg');
    height: 400px;"
    class="site-blocks-cover">
  <div class="container">
    <div class="row align-items-start align-items-md-center justify-content-end">
      <div class="col-md-5 text-center text-md-left pt-5 pt-md-0">
        <h1 class="mb-2">Find everything on your grocery list!</h1>
        <div class="intro-text text-center text-md-left">
          <p class="mb-4">Welcome to IntelliStore! We're here to make your grocery shopping experience as easy and convenient as possible.</p>
          <p>
            <router-link v-if="userLoggedIn" to="/shop" class="btn btn-primary">Shop Now</router-link>
            <router-link v-else to="/shop" class="btn btn-primary" style="margin-right: 10px">Shop Now</router-link>
            <!-- <router-link v-else to="/login" class="btn btn-primary" style="margin-right: 10px">Sign in</router-link>
            <router-link v-else to="/register" class="btn btn-primary">Sign Up</router-link> -->
          </p>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="site-section site-section-sm site-blocks-1">
  <div class="container">
    <div class="row">
      <div class="col-md-6 col-lg-4 d-lg-flex mb-4 mb-lg-0 pl-4">
        <div class="icon mr-4 align-self-start">
          <span class="icon-truck"></span>
        </div>
        <div class="text">
          <h2 class="text-uppercase">Free Shipping</h2>
          <p>We offer a wide variety of fresh, affordable groceries, and we deliver right to your door. COMPLETELY FREE OF COST!</p>
        </div>
      </div>
      <div class="col-md-6 col-lg-4 d-lg-flex mb-4 mb-lg-0 pl-4">
        <div class="icon mr-4 align-self-start">
          <span class="icon-refresh2"></span>
        </div>
        <div class="text">
          <h2 class="text-uppercase">Easy Returns</h2>
          <p>We understand that sometimes things don't go as planned. If you're not happy with your purchase, you can return it for a full refund within 30 days of purchase.</p>
        </div>
      </div>
      <div class="col-md-6 col-lg-4 d-lg-flex mb-4 mb-lg-0 pl-4">
        <div class="icon mr-4 align-self-start">
          <span class="icon-help"></span>
        </div>
        <div class="text">
          <h2 class="text-uppercase">Customer Support</h2>
          <p>We're here to help! Our customer support team is available 24/7 to answer your questions and help you with any issues you may have.</p>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="site-section block-3 site-blocks-2 bg-light">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-7 site-section-heading text-center pt-4">
          <h2>Featured Products</h2>
        </div>
      </div>
  <br>
  <div class="container">
    <div class="row">
      <div v-for="(product, i) in products.slice(0,3)" :key="product.product_id" class="col-md-6 col-lg-4 d-lg-flex mb-4 mb-lg-0 pl-6 nonloop-block-3 owl-carousel">
        <figure>
          <router-link :to="'/shopsingle?product_id=' + product.product_id">
            <img :src="'data:;base64,' + product.image" width="150" height="150" alt="Product Image" class="img-fluid">
        </router-link>
        </figure>
        <div class="block-4-text p-4">
          <h3><router-link :to="'/shopsingle?product_id={{product.product_id}}'">{{ product.name }}</router-link></h3>
          <p class="mb-0">{{ product.description }}</p>
          <p class="text-primary font-weight-bold">{{ product.price }} {{ product.unit }}</p>
        </div>
      </div>
    </div>
  </div>
    </div>
  </div>

<div class="site-section block-8">
  <div class="container">
    <div class="row justify-content-center  mb-5">
      <div class="col-md-7 site-section-heading text-center pt-4">
        <h2>Big Sale!</h2>
      </div>
    </div>
    <div class="row align-items-center">
      <div class="col-md-12 col-lg-7 mb-5">
        <a href="#"><img src="../assets/images/blog_1.jpg" alt="Image placeholder" class="img-fluid rounded"></a>
      </div>
      <div class="col-md-12 col-lg-5 text-center pl-md-5">
        <h2><a href="#"> FLAT 10% OFF</a></h2>
        <h5><a href="#"> use code NEW10 during checkout</a></h5>
        <p class="post-meta mb-4"><span class="block-8-sep">&bullet;</span>Valid only for new users.</p>
        <p>you can get flat 10% off on your entire order amount using code NEW10, hurry, order now!</p>
        <p><a href="#" class="btn btn-primary">Shop Now</a></p>
      </div>
    </div>
  </div>
</div>

</div>
    <FooterItem />
    <Request
      endpoint="product"
      method="GET"
      :headers="{ 'Content-Type': 'application/json' }"
      @response="handleProducts"
    />
  </main>
</template>

<script>
export default {
  data() {
    return {
      userLoggedIn: false, // Replace with your actual user login status
      imageurl: '../assets/images/hero.jpg',
      products: [],
      // ... Add other data properties as needed
    };
  },
  components: {
    Request,
    FooterItem,
  },
  methods: {
    handleProducts(responseData) {
      // Handle the response data here
      this.products=responseData;
      console.log(responseData);
    },
    getRandomInt(max) {
      return Math.floor(Math.random() * max);
    },
  }
  // ... Add methods, computed properties, etc., as needed
};
</script>