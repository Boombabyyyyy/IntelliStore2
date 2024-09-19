// import './assets/main.css'

// import 'https://fonts.googleapis.com/css?family=Mukta:300,400,700'
import './assets/fonts/icomoon/style.css'
import './assets/css/bootstrap.min.css'
import './assets/css/magnific-popup.css'
import './assets/css/jquery-ui.css'
import './assets/css/owl.carousel.min.css'
import './assets/css/owl.theme.default.min.css'


import './assets/css/aos.css'

import './assets/css/style.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import store from './store'; // Import the Vuex store

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(store)

app.mount('#app')
