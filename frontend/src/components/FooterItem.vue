<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
      <footer class="site-footer border-top">
    <div class="container">
      <div class="row">
        <div class="col-lg-6 mb-5 mb-lg-0">
          <div class="row">
            <div class="col-md-12">
              <h3 class="footer-heading mb-4">Navigations</h3>
            </div>
            <div class="col-md-6 col-lg-4">
              <ul class="list-unstyled">
                <li><router-link to="/">Home</router-link></li>
                <li><router-link to="/shop">Shop</router-link></li>
                <li><router-link to="/about">About</router-link></li>
                
              </ul>
            </div>
            <div class="col-md-6 col-lg-4">
              <ul class="list-unstyled">
                <li><router-link to="/profile">Your Profile</router-link></li>
                <li><router-link to="/orders">Your Orders</router-link></li>
                <li><router-link to="/cart">Your Cart</router-link></li>
              </ul>
            </div>
            <div class="col-md-6 col-lg-4">
              <ul class="list-unstyled">
                <li><router-link to="/login">Sign In</router-link></li>
                <li><router-link to="/register">Sign Up</router-link></li>
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3 mb-4 mb-lg-0">
          <h3 class="footer-heading mb-4">Promo</h3>
          <a href="#" class="block-6">
            <img src="../assets/images/hero.jpg" alt="Image placeholder" class="img-fluid rounded mb-4">
            <h3 class="font-weight-light  mb-0">Finding Your Perfect Groceries</h3>
            <p>Promo from  August 15 &mdash; 25, 2023</p>
            <p>Use code NEW10 on your first order!</p>
          </a>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="block-5 mb-5">
            <h3 class="footer-heading mb-4">Contact Info</h3>
            <ul class="list-unstyled">
              <strong><li class="name">Azfar Faheem Mustafa</li></strong>
              <li class="address">203 Fake St. Mountain View, Mumbai, Maharashtra, India</li>
              <li class="phone"><a href="tel://+917977573428">+91 7977573428</a></li>
              <li class="email">21f2000478@ds.study.iitm.ac.in</li>
            </ul>
          </div>
        </div>
      </div>
      <div class="row pt-5 mt-5 text-center">
        <div class="col-md-12">
        </div>
        
      </div>
    </div>
  </footer>
</template>