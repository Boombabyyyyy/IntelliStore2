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
          <div class="col-md-12 mb-0"><a href="index.html">Home</a> <span class="mx-2 mb-0">/</span> <strong class="text-black">Admin Panel</strong></div>
        </div>
      </div>
    </div>  

    <div v-if="isadmin == 2" class="site-section">
    <div class="container">
      <div class="row">
        <div class="col-md-7">
          <form @submit.prevent="addProduct" method="post" enctype="multipart/form-data">
            <h2 class="h3 mb-3 text-black">Add Product</h2>
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
                  <select v-model="newProduct.unit" class="form-control" id="unit" name="unit">
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
                  <label for="image" class="text-black">Product Image</label><span class="text-danger">*</span>
                  <input accept=".jpg, .jpeg, .png, .gif" @change="onFileChange" type="file" name="image" class="form-control" id="image" required>
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
                  <input type="submit" class="btn btn-primary btn-lg btn-block" value="Add Product">
                </div>
              </div>
            </div>
          </form>
        </div>
        <div class="col-md-5 ml-auto">
          <form @submit.prevent="addCategory" method="post">
            <h2 class="h3 mb-3 text-black">Add Category</h2>
            <div class="p-3 p-lg-5 border">
              <div class="form-group row">
                <ul class="flashes" v-if="catmessages.length > 0">
                    <li v-for="(message, index) in catmessages" :key="index" class="text-success">{{ message }}</li>
                </ul>

                <div class="col-md-12">
                  <label for="name" class="text-black">Category name <span class="text-danger">*</span></label>
                  <input v-model="newCategory.name" type="text" class="form-control" id="name" name="name" required>
                </div>
              </div>
              <div class="form-group row">
                <div class="col-lg-12">
                  <input type="submit" class="btn btn-primary btn-lg btn-block" value="Add Category">
                </div>
              </div>
            </div>
          </form>
          <br>
          <h2 class="h3 mb-3 text-black">Category List</h2>
          <div class="col-md-18">
      <ul class="flashes" v-if="catmessages2.length > 0">
              <li v-for="(message, index) in catmessages2" :key="index" class="text-success">{{ message }}</li>
      </ul>
      <div v-for="category in categories" :key="category.category_id">
        <div v-if="category.editMode">
          <!-- Edit mode -->
          <form @submit.prevent="saveCategory(category)">
            <input v-model="category.name" class="form-control" />
            <button type="submit" class="btn btn-success btn-sm">Save</button>
            <button @click="cancelEdit(category)" class="btn btn-secondary btn-sm">Cancel</button>
          </form>
        </div>
        <div v-else>
          <!-- View mode -->
          <div class="p-1 p-lg-1 border">
            {{ category.name }}
            <button @click="editCategory(category)" class="btn btn-primary btn-sm" style="float:right;"><span class="icon icon-edit"> </span></button>
            <button @click="confirmDeletecat(category.category_id, category.name)" class="btn btn-danger btn-sm" style="float:right; margin-right:10px;"><span class="icon icon-delete"> </span></button>
          </div>
        </div>
        <br />
      </div>
    </div>
          <!-- <div class="col-md-18">
            <div v-for="category in categories" :key="category.category_id">
              <div class="p-1 p-lg-1 border">
                {{ category.name }}
                <button @click="editCategory(category.category_id)" class="btn btn-primary btn-sm" value="" style="float:right;"><span class="icon icon-edit"> </span></button>
                <button @click="confirmDeletecat(category.category_id)" class="btn btn-danger btn-sm" value="" style="float:right; margin-right:10px;"><span class="icon icon-delete"> </span></button>
              </div>
              <br>
            </div>
          </div> -->
        </div>
      </div>
    </div>
    <div class="container">
    <div class="row mb-5">
      <form class="col-md-12" method="post">
        <div class="site-blocks-table">
          <h2 class="h3 mb-3 text-black">Product List</h2>
          <div class="float-md-center mb-4">
            <div class="btn-group mr-1 ml-md-auto">
              <button type="button" class="btn btn-secondary btn-sm dropdown-toggle" id="dropdownMenuReference" data-toggle="dropdown">CATEGORIES</button>
              <div class="dropdown-menu" aria-labelledby="dropdownMenuReference">
                <a v-for="category in cats" :key="category.category_id" class="dropdown-item" :href="'/adminbycategory?category_id=' + category.category_id">{{ category.name }}</a>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item" href="/admin">ALL</a>
              </div>
            </div>
          </div>
          <table class="table table-bordered">
            <thead>
              <tr>
                <th class="product-thumbnail">Image {{ user }}</th>
                <th class="product-name">Product Name</th>
                <th class="product-price">Price</th>
                <th class="product-quantity">Stock</th>
                <th class="product-remove">mfg</th>
                <th class="product-remove">exp</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in products" :key="product.product_id">
                <td class="product-thumbnail">
                  <img :src="'data:;base64,' + product.image" width="150" height="150" alt="Product Image" class="img-fluid">
                  <!-- <img src="..\assets\images\bajaj.jpg" alt="Image placeholder" class="img-fluid rounded"> -->
                </td>
                <td class="product-name">
                  <strong>{{ product.name }}</strong>
                </td>
                <td>{{ product.price }} {{ product.unit }}</td>
                <td>
                  <form :action="'/updatestock/' + product.name" method="post">
                    <input type="hidden" name="product_id" :value="product.product_id">
                    <div class="input-group mb-3" style="max-width: 120px; float: center;">
                      <input type="text" readonly class="form-control text-center" name="stock" :value="product.stock" placeholder="" aria-label="Example text with button addon" aria-describedby="button-addon1">
                    </div>
                  </form>
                </td>
                <td>{{ product.mfg }}</td>
                <td>{{ product.exp }}</td>
                <td>
                  <button type="button"  @click="confirmDeleteprod(product.product_id, product.name)" class="btn btn-danger btn-sm" value=""><span class="icon icon-delete"></span></button>
                </td>
                <td>
                  <router-link :to="'/editproduct?product_id=' + product.product_id" class="d-flex">
                  <button type="button" class="btn btn-primary btn-sm" value=""><span class="icon icon-edit"></span></button>
                  </router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </form>
    </div>
    </div>

      <div class="container">
      <div class="row">
        <div class="col-md-7">
    <h2 class="h3 mb-3 text-black">Category Approval List</h2>
    <div class="col-md-18">
        <div class="col-md-18">
          <table class="table table-bordered">
            <thead>
              <tr>
                <th class="product-thumbnail">Name</th>
                <th class="product-name">Request Type</th>
                <th class="product-price">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="approval in catapprovals" :key="approval.approval_id">
                <td class="product-name">
                  <strong>{{ approval.name }}</strong>
                </td>
                <td class="product-name">
                  <strong>{{ approval.request_type }}</strong>
                </td>
                <td class="product-name">
                  <strong>{{ approval.status }}</strong>
                </td>
              </tr>
            </tbody>
            </table>
          </div>
    </div>
    </div>
    <div class="col-md-5 ml-auto">
            <h4 class="h3 mb-3 text-danger">Note:</h4>
            <div class="p-3 p-lg-5 border">
              <table class="table table-bordered">
            <thead>
              <tr>
                <th class="product-thumbnail">Request Type</th>
                <th class="product-name">operation</th>

              </tr>
            </thead>
            <tbody>
              <tr>
                <td>1</td>
                <td>Category Addition</td>
              </tr>
              <tr>
                <td>2</td>
                <td>Category Updation</td>
              </tr>
              <tr>
                <td>2</td>
                <td>Category Deletion</td>
              </tr>
            </tbody>
            </table>
            </div>
    </div>
    </div>
    <!-- Rest of your code... -->
      </div>
  </div>
  <div v-if="isadmin != 2" class="site-section">
    <h1 class="h3 mb-3 text-danger"><strong>Unauthorized Access, only managers can access this page.</strong></h1>
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
      catmessages: [],
      catmessages2: [],
      isadmin: null,
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
      products: [],
      units: ['Rs/Unit', 'Rs/Kg', 'Rs/Dozen', 'Rs/Litre'],
      newCategory: {
        name: '',
      },
      categories: [],
      catapprovals: [],
    };
  },
  beforeMount(){
    this.getisadmin();
    this.getcatapprovals();
  },
  methods: {
    getisadmin(){
      const user_id = store.state.currentUser
      const storedUserData = store.state.users[user_id].userData
      const isAdmin = storedUserData.isadmin
      this.isadmin = isAdmin
    },
    async getcatapprovals(){
      const response = await fetchUtil({
          endpoint: "catapprovals",
          method: 'GET',
          user_id: this.user_id
        });
        this.catapprovals = response
        console.log(this.catapprovals);
    },
    editCategory(category) {
      // Set edit mode to true for the selected category
      console.log(category);
      this.categories.forEach((c) => {
      c.editMode = (c === category);
    });
    },
    cancelEdit() {
    // Set edit mode to false for the selected category to cancel editing
    this.categories.forEach((c) => {
      c.editMode = false;
    });
    },
    confirmDeletecat(cat_id, name){
      const isConfirmed = window.confirm(`Are you sure you want to send deletion request to admin for the ${name} category?`);

      // Check if the user clicked "OK" in the confirmation dialog
      if (isConfirmed) {
        // Call your delete function or perform the delete action here
        this.deleteCategory(cat_id);
      }
    },
    confirmDeleteprod(prod_id, name){
      const isConfirmed = window.confirm(`Are you sure you want to delete this product: ${name} ?`);

      // Check if the user clicked "OK" in the confirmation dialog
      if (isConfirmed) {
        // Call your delete function or perform the delete action here
        this.deleteProduct(prod_id);
      }
    },
    handleProducts(responseData) {
      // Handle the response data here
      this.products=responseData;
      console.log(responseData);
    },
    handleCats(responseData) {
      // Handle the response data here
      // this.categories=responseData;
      this.categories = responseData.map(category => ({ ...category, editMode: false }));
      console.log(responseData);
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
    async addProduct() {
      const response = await fetchUtil({
          endpoint: "product",
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          data: this.newProduct,
          user_id: this.user_id
        });
        console.log(response);
        location.reload();
      // Implement the logic to add a product
      // Access the necessary data from this.newProduct
    },
    async addCategory() {
      const name = this.newCategory.name
      const storedUserData = store.state.users[this.user_id].userData
      const isadmin = storedUserData.isadmin
      const response = await fetchUtil({
          endpoint: "category",
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          data: {"name": name},
          user_id: this.user_id
        });
      this.catmessages = [response];
      console.log(response, isadmin);
      if(isadmin == 1) {
        location.reload();
      }
      
      // Implement the logic to add a category
      // Access the necessary data from this.newCategory
    },
    async saveCategory(category) {
      const name = category.name
      const storedUserData = store.state.users[this.user_id].userData
      const isadmin = storedUserData.isadmin
      const category_id = category.category_id
      const response = await fetchUtil({
          endpoint: "category",
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          data: {"name": name, "category_id": category_id},
          user_id: this.user_id
        });
      console.log(response, isadmin);
      if(isadmin == 1) {
        location.reload();
      } else {
        this.cancelEdit()
        this.catmessages2 = [response];
      }
      // Implement the logic to edit a category
      // Access the necessary data from the provided category object
    },
    async deleteCategory(category_id) {
      const storedUserData = store.state.users[this.user_id].userData
      const isadmin = storedUserData.isadmin
      console.log(category_id);
      const response = await fetchUtil({
          endpoint: "category",
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
          data: Number(category_id),
          user_id: this.user_id
        });
      this.catmessages2 = [response[0].status];
      console.log(response[0], isadmin);
      if(isadmin == 1) {
        location.reload();
      }
    },

    async deleteProduct(product_id) {
      const response = await fetchUtil({
          endpoint: "product",
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
          data: Number(product_id),
          user_id: this.user_id
        });
      console.log(response);
      location.reload();
    },
    // Add other methods as needed
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
  