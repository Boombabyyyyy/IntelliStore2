<script setup>
import { RouterLink, RouterView } from 'vue-router'
import store from '../store'
import FooterItem from '../components/FooterItem.vue'
import Request from '../components/RequestItem.vue';
import fetchUtil from '../FetchUtil.js';

</script>

<template>
  <div>
    <div class="bg-light py-3">
      <div class="container">
        <div class="row">
          <div class="col-md-12 mb-0"><router-link to="/">Home</router-link> <span class="mx-2 mb-0">/</span> <strong class="text-black">Cart</strong></div>
        </div>
      </div>
    </div>

    <div v-if="cartLength === 0 & !user_id" class="site-section">
      <div class="container" style="align: center;">
      <h3 class="text-danger">Please login to view and manage your Cart!</h3>
      <br>
      <router-link to="/login" style="margin-left: auto; margin-right: auto; margin-top:50px;">
        <button type="button" class="btn btn-primary">Click here to login</button>
      </router-link>
    </div>
    </div>

    <div v-if="cartLength === 0 & user_id" class="site-section">
      <div class="container">
        <div class="row mb-5">
          <h3 class="text-black h4 text-uppercase">It's Lonely here, No products added ☹️</h3>
        </div>
        <div class="row mb-5">
          <router-link to="/shop">
            <button class="btn btn-outline-primary btn-block">Continue Shopping</button>
          </router-link>
        </div>
      </div>
    </div>

    <div  v-if="cartLength !== 0 & user_id" class="site-section">
      <div class="container">
        <div class="row mb-5">
          <form class="col-md-12" @submit.prevent="goToCheckout" name="checkout" id="checkout">
            <div class="form-group row">
              <div class="col-md-12">
                <span class="icon icon-map-marker text-primary" style="font-size: 30px;">
                  <label class="text-black h4" for="address">SELECT DELIVERY ADDRESS and mobile</label>
                </span>
                <select v-model="selectedAddress" name="address" id="address" class="form-control" required>
                  <option v-for="address in addresses" :key="address.address_id" :value="address.Address">
                    {{ address.Address }}
                  </option>
                </select>
                <select v-model="selectedMobile" name="address" id="address" class="form-control" required>
                  <option v-for="address in addresses" :key="address.address_id" :value="address.mobile">
                    {{ address.mobile }}
                  </option>
                </select>
                <router-link to="/profile">Add new address</router-link>
              </div>
            </div>

            <div class="site-blocks-table">
              <table class="table table-bordered">
                <thead>
                  <tr>
                    <th class="product-thumbnail">Image</th>
                    <th class="product-name">Product</th>
                    <th class="product-price">Price</th>
                    <th class="product-quantity">Quantity</th>
                    <th class="product-total">Total</th>
                    <th class="product-remove">Remove</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="product in cartProducts" :key="product.product_id">
                    <td class="product-thumbnail">
                      <a :href="'/shop_single?product_id=' + product.product_id">
                        <img :src="'data:;base64,' + product.image" width="150" height="150" alt="Product Image" class="img-fluid">
                      </a>
                    </td>
                    <td class="product-name">
                      <h2 class="h5 text-black">{{ product.name }}</h2>
                    </td>
                    <td><b>{{ product.price }} {{ product.unit }}</b></td>
                    <td>
                      <div class="input-group mb-3" style="max-width: 120px; text-align: center; margin-left: auto; margin-right: auto;" align="center">
                        <p></p>
                        <input type="number" disabled id="qty" name="qty" class="form-control text-center" :value="product.qty" onkeydown="return false" placeholder="" aria-label="Example text with button addon" aria-describedby="button-addon1">
                      </div>
                    </td>
                    <td><b>{{ product.total }} Rs</b></td>
                    <td><a @click="deleteprod(product.product_id)" class="btn btn-danger btn-sm">X</a></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </form>
        </div>

        <div class="row">
          <div class="col-md-6">
            <div class="row mb-5">
              <div class="col-md-6">
                <router-link to="/shop">
                  <button class="btn btn-outline-primary btn-block">Continue Shopping</button>
                </router-link>
              </div>
            </div>

            <!-- Coupon form goes here -->


          </div>

            <!-- Cart totals and checkout button goes here -->
            <div class="col-md-6 pl-5">
          <div class="row justify-content-end">
            <div class="col-md-7">
              <div class="row">
                <div class="col-md-12 text-right border-bottom mb-5">
                  <h3 class="text-black h4 text-uppercase">Cart Totals</h3>
                </div>
              </div>
              <div class="row mb-3">
                <div class="col-md-6">
                  <span class="text-black">Subtotal</span>
                </div>
                <div class="col-md-6 text-right">
                  <strong class="text-black">Rs. {{ subtotal }}</strong>
                </div>
              </div>
              <div class="row mb-3">
                <div class="col-md-6">
                  <span class="text-black">GST (18%)</span>
                </div>
                <div class="col-md-6 text-right">
                  <strong class="text-black">Rs. {{ gst }}</strong>
                </div>
              </div>
              <div class="row mb-3">
                <div class="col-md-6">
                  <span class="text-black">Shipping</span>
                </div>
                <div class="col-md-6 text-right">
                  <strong class="text-success">FREE</strong>
                </div>
              </div>
              <div class="row mb-5">
                <div class="col-md-6">
                  <span class="text-black">Total</span>
                </div>
                <div class="col-md-6 text-right">
                  <strong class="text-black">Rs. {{ Total }}</strong>
                </div>
              </div>
              <div v-if="discount !== 0" class="row mb-5">
                <div class="col-md-6">
                  <span class="text-black">Coupon discount</span>
                </div>
                <div class="col-md-6 text-right">
                  <strong class="text-success">-Rs. {{ discount }}</strong>
                </div>
              </div>
              <div v-if="discount !== 0" class="row mb-5">
                <div class="col-md-6">
                  <span class="text-black">Total Payable</span>
                </div>
                <div class="col-md-6 text-right">
                  <strong class="text-black">Rs. {{ newtotal }}</strong>
                </div>
              </div>
              <div class="row">
                <div class="col-md-12">
                  <button type="submit" form="checkout" class="btn btn-primary btn-lg py-3 btn-block">Place Order and Pay</button>
                </div>
              </div>
            </div>
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
      user_id: store.state.currentUser,
      subtotal: null,
      gst: null,
      Total: null,
      discount: 0,
      cartLength: 0,
      selectedAddress: null,
      selectedMobile: null,
      addresses: [],
      cartProducts: [],
      messages: [],
    };
  },
  mounted() {
    this.getCart();
  },
  methods: {
    async goToCheckout() {
      console.log("Proceed to checkout");
      const user_id = store.state.currentUser
      const response = await fetchUtil({
          endpoint: "order",
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          data: {"user_id": user_id, "subtotal": this.subtotal, "gst": Number(this.gst), "grandtotal": Number(this.Total), "discount": 0, "address": this.selectedAddress, "mobile": this.selectedMobile, "payable": Number(this.grandtotal) },
          user_id: user_id
        });
        console.log(response);
    },
    async getproddetails(product_id){
      const endpoint="product/"+product_id
      const user_id = store.state.currentUser
      const response = await fetchUtil({
          endpoint: endpoint,
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          user_id: user_id
        });
      return response
    },
    async deleteprod(product_id){
      const user_id = store.state.currentUser
      const response = await fetchUtil({
          endpoint: "cartapi",
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
          data: product_id,
          user_id: user_id
        });
        console.log(response);
        location.reload();
    },
    async getCart(){
      const user_id = store.state.currentUser

      const response2 = await fetchUtil({
          endpoint: "address",
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          data: user_id,
          user_id: user_id
        });
      this.addresses = response2
      
      const response = await fetchUtil({
          endpoint: "cartapi",
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          user_id: user_id
        });
        this.cartLength = response.length
        console.log("length:",this.cartLength);
        console.log(response);

        const combinedData = [];
        let subt = 0;
        if(response.length >= 0) {
        for (const item of response) {
          const { product_id, qty } = item;
          const productData = await this.getproddetails(product_id);

          if (productData) {
              // Combine product details with quantity
              const combinedItem = {
                  ...productData,
                  qty: qty,
                  total: productData.price*qty
              };

              // Add the combined item to the result array
              combinedData.push(combinedItem);

              subt += combinedItem.total;
          }
        }
        this.cartProducts = combinedData;
        this.subtotal = subt;
        this.gst = 0.18*subt;
        this.gst =  this.gst.toFixed(2);
        this.Total = Number(subt) + Number(this.gst)
        this.Total = this.Total.toFixed(2);
    
      }
      
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
  