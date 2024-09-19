<script setup>
import { RouterLink, RouterView } from 'vue-router'
import FooterItem from '../components/FooterItem.vue'
</script>


<template>
  <div class="site-wrap">
  
  <div class="bg-light py-3">
    <div class="container">
      <div class="row">
        <div class="col-md-12 mb-0"><a href="index.html">Home</a> <span class="mx-2 mb-0">/</span> <strong class="text-black">About</strong></div>
      </div>
    </div>
  </div>  

  <div class="site-section border-bottom">
    <div class="container">
      <div class="row mb-5">
        <div class="col-md-6">
          <div class="block-16">
            <figure>
              <img src="../assets/images/blog_1.jpg" alt="Image placeholder" class="img-fluid rounded">
              <a href="https://www.youtube.com/watch?v=CiklAyGrmcc" class="play-button popup-vimeo"><span class="ion-md-play"></span></a>

            </figure>
          </div>
        </div>
        <div class="col-md-1"></div>
        <div class="col-md-5">
          
          
          <div class="site-section-heading pt-3 mb-4">
            <h2 class="text-black">How We Started</h2>
          </div>
          <p>Our story began with a simple idea: to make it easier for people to get the groceries they need, without having to leave their homes. We started out as a small, family-owned business, but we quickly grew to become one of the leading online grocery retailers in the country.

            We believe that everyone deserves access to fresh, healthy food, regardless of their location or income. That's why we offer a wide variety of products at affordable prices. We also offer free shipping on all orders, and we deliver to most parts of the country.
            
            We're committed to providing our customers with the best possible experience. That's why we have a team of dedicated customer service representatives who are available 24/7 to answer your questions and help you with your orders.
            
            We're also committed to giving back to our community. We donate a portion of our profits to local food banks and charities. We also partner with local farmers to support sustainable agriculture.</p>
            
            <p>We're proud of the company we've built, and we're excited to continue growing and serving our customers. Thank you for choosing us</p>
          
        </div>
      </div>
    </div>
  </div>

  <div class="site-section border-bottom">
    <div class="container">
      <div class="row justify-content-center mb-5">
        <div class="col-md-7 site-section-heading text-center pt-4">
          <h2>The Team</h2>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6 col-lg-3">

          <div class="block-38 text-center">
            <div class="block-38-img">
              <div class="block-38-header">
                <img src="../assets/images/me.png" alt="Image placeholder" class="mb-4">
                <h3 class="block-38-heading h4">Azfar Faheem Mustafa</h3>
                <p class="block-38-subheading">CEO/Co-Founder</p>
              </div>
              <div class="block-38-body">
                <p>The only real one.</p>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="block-38 text-center">
            <div class="block-38-img">
              <div class="block-38-header">
                <img src="../assets/images/person_2.jpg" alt="Image placeholder" class="mb-4">
                <h3 class="block-38-heading h4">Jennifer Greive</h3>
                <p class="block-38-subheading">Co-Founder</p>
              </div>
              <div class="block-38-body">
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Vitae aut minima nihil sit distinctio recusandae doloribus.</p>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="block-38 text-center">
            <div class="block-38-img">
              <div class="block-38-header">
                <img src="../assets/images/person_3.jpg" alt="Image placeholder" class="mb-4">
                <h3 class="block-38-heading h4">John Reese</h3>
                <p class="block-38-subheading">Marketing</p>
              </div>
              <div class="block-38-body">
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Vitae aut minima nihil sit distinctio recusandae doloribus ut fugit officia voluptate soluta. </p>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="block-38 text-center">
            <div class="block-38-img">
              <div class="block-38-header">
                <img src="../assets/images/person_4.jpg" alt="Image placeholder" class="mb-4">
                <h3 class="block-38-heading h4">Mike Coolbert</h3>
                <p class="block-38-subheading">Sales Manager</p>
              </div>
              <div class="block-38-body">
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Vitae aut minima nihil sit distinctio recusandae doloribus ut fugit officia voluptate soluta. </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>


  <div class="site-section site-section-sm site-blocks-1 border-0" >
    <div class="container">
      <div class="row">
        <div class="col-md-6 col-lg-4 d-lg-flex mb-4 mb-lg-0 pl-4">
          <div class="icon mr-4 align-self-start">
            <span class="icon-truck"></span>
          </div>
          <div class="text">
            <h2 class="text-uppercase">Free Shipping</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus at iaculis quam. Integer accumsan tincidunt fringilla.</p>
          </div>
        </div>
        <div class="col-md-6 col-lg-4 d-lg-flex mb-4 mb-lg-0 pl-4">
          <div class="icon mr-4 align-self-start">
            <span class="icon-refresh2"></span>
          </div>
          <div class="text">
            <h2 class="text-uppercase">Free Returns</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus at iaculis quam. Integer accumsan tincidunt fringilla.</p>
          </div>
        </div>
        <div class="col-md-6 col-lg-4 d-lg-flex mb-4 mb-lg-0 pl-4">
          <div class="icon mr-4 align-self-start">
            <span class="icon-help"></span>
          </div>
          <div class="text">
            <h2 class="text-uppercase">Customer Support</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus at iaculis quam. Integer accumsan tincidunt fringilla.</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <FooterItem />
</div>
</template>


<!-- <style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style> -->
