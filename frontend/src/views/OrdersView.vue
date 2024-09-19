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
            <div class="col-md-12 mb-0"><a href="index.html"></a> <span class="mx-2 mb-0"></span> <strong class="text-black">YOUR ORDERS</strong></div>
          </div>
        </div>
      </div>

      <div v-if="userLoggedIn" class="site-section">
    <div class="container" style="align: center;">
      <div v-if="orders.length === 0" class="site-section">
        <div class="container">
          <div class="row mb-5">
            <h3 class="text-black h4 text-uppercase">It's Lonely here, No Orders Yet ☹️</h3>
          </div>
          <div class="row mb-5">
            <router-link to="/shop">
              <button class="btn btn-outline-primary btn-block">Continue Shopping</button>
            </router-link>
          </div>
        </div>
      </div>

      <div v-else class="row">
        <div class="col-md-12"></div>
        <div class="col-md-12">
          <div class="col-md-12 ml-auto">
            <ul v-for="order in orders" :key="order.order_id">
              <li>
                <span class="d-block text-primary h6 text-uppercase" style="text-align: left;">Order Number: #{{ order.order_id }}</span>
              </li>
              <span class="d-block text-primary h6 text-uppercase" style="text-align: left;">Order Date: {{ order.created_at }}</span>
              <div class="col-md-18">
                <form></form>
                <div class="p-1 p-lg-1 border">
                  <strong><p class="text-black font-weight-bold">Order Status: <span class="text-warning">{{ order.status }}</span></p></strong>
                </div>
                <div class="p-1 p-lg-1 border">
                  <p class="text-black"><span class="font-weight-bold">Contact No:</span> {{ order.mobile }}</p>
                  <p class="text-black"><span class="font-weight-bold">Delivery Address:</span> {{ order.address }}</p>
                </div>
                <div class="p-1 p-lg-1 border">
                  <p class="text-black"><span class="font-weight-bold">Subtotal: </span> Rs. {{ order.subtotal }}</p>
                  <p class="text-black"><span class="font-weight-bold">GST&#40;18%&#41;: </span>Rs. {{ order.gst }}</p>
                  <p class="text-black"><span class="font-weight-bold">grandtotal: </span>Rs. {{ order.grandtotal }}</p>
                  <template v-if="order.discount !== '0'">
                    <p class="text-black"><span class="font-weight-bold">Coupon Discount: </span><span class="text-success"> - Rs. {{ order.discount }}</span></p>
                    <p class="text-black"><span class="font-weight-bold">Order amount: </span>Rs. {{ order.payable }}</p>
                  </template>
                </div>

                <br>
              </div>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else>
    <br><br>
    <div class="container" style="align: center;">
      <h3 class="text-danger">Please login to view and manage your Orders!</h3>
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
      userLoggedIn: false, // Set this to the actual condition for user login
      orders: [],
    };
  },
  mounted() {
    this.getOrder();
  },
  methods: {

    async getOrder(){
      const user_id = store.state.currentUser
      if(user_id){
        this.userLoggedIn=true
      }
      const response = await fetchUtil({
          endpoint: "order",
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          user_id: user_id
        });
      this.orders = response
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
  