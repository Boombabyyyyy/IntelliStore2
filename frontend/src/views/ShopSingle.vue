<script setup>
import { RouterLink, RouterView } from 'vue-router'
import FooterItem from '../components/FooterItem.vue'
import Request from '../components/RequestItem.vue';
</script>


<template>

    <div class="bg-light py-3">
      <div class="container">
        <div class="row">
          <div class="col-md-12 mb-0"><router-link to="/">Shop</router-link> <span class="mx-2 mb-0">/</span> <strong class="text-black">{{ product.name }}</strong></div>
        </div>
      </div>
    </div>  

    <div class="site-section">
    <div class="container">
      <div class="row">
        <div class="col-md-6">
          <router-link :to="'/shop_single?product_id=' + product.product_id">
            <img :src="'data:;base64,' + product.image" width="400" height="400" alt="Product Image" class="img-fluid">
            <!-- <img src="..\assets\images\store.jpg" width="400" height="400" alt="Image placeholder" class="img-fluid rounded"> -->
          </router-link>
        </div>
        <div class="col-md-6">
          <form @submit.prevent="addToCart">
            <input type="hidden" v-model="product.product_id">
            <input type="hidden" v-model="product.stock">
            <input type="hidden" v-model="product.name">
            <input type="hidden" v-model="product.category_id">
            <h2 class="text-black">{{ product.name }}</h2>
            <p>{{ product.description }}</p>
            <p><strong class="text-primary h4">₹{{ product.price }}</strong></p>

            <p>Date of Manufacturing: {{ product.mfg }}</p>
            <p>Date of Expiry: {{ product.exp }}</p>
            <div class="mb-5">

              <div class="input-group mb-3" style="max-width: 120px;">
                <div v-if="product.stock < 3">
                  <div v-bind:max="product.stock"></div>
                </div>
                <div v-else>
                  <div v-bind:max="3"></div>
                </div>
                <div v-if="product.stock !== 0">
                  <div class="input-group mb-3" style="max-width: 120px; text-align: center; margin-left: auto; margin-right: auto;" align="center">
                    <p></p>
                    <input v-model="quantity" type="number" :max="max" min="1" class="form-control text-center" value="1" placeholder="" aria-label="Example text with button addon" aria-describedby="button-addon1">
                    <button type="submit" class="btn btn-primary btn-sm">ADD<span class="icon icon-cart-plus"></span></button>
                  </div>
                </div>
                <div v-else>
                  <button type="button" disabled class="btn btn-link btn-sm"><p class="text-danger font-weight-bold">Out Of Stock :&#40;<span class="icon icon-emoji-frown"></span></p></button>
                  <p class="text-primary font-weight-bold">Check back tomorrow!</p>
                </div>
              </div>

            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <Request v-if="endpoint !== null"
      :endpoint="endpoint"
      method="GET"
      :headers="{ 'Content-Type': 'application/json' }"
      @response="handleProduct"
    />

  <FooterItem />
</template>

<script>
export default {
  data() {
    return {
      productid: null,
      endpoint: null,
      product: {},
      quantity: 1,
      max: 3, // Default max value, update it based on your logic
    };
  },
  mounted() {
    // Add any additional logic that should run after the component is mounted
    this.productid = this.$route.query.product_id;
    this.endpoint = "product/" + this.productid

  },
  components: {
    Request,
    FooterItem,
  },
  methods: {
    handleProduct(responseData) {
      // Handle the response data here
      this.product=responseData;
      console.log(responseData);
    },
    addToCart() {
      // Implement the logic to add the product to the cart
      // Access the necessary data from this.product and this.quantity
    },
  },
};
</script>