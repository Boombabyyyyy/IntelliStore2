import { createApp } from 'vue'
import { createStore } from 'vuex'

const savedState = JSON.parse(localStorage.getItem('vuexState'));

const store = createStore({
  state () {
    return savedState || {
      users: {},
      currentUser: null,
    }
  },
  mutations: {
    setUserTokens(state, { userId, jwtToken, refresh_token }) {
      // Create a user object if it doesn't exist
      if (!state.users[userId]) {
        state.users[userId] = {};
      }
      
      // Set user tokens
      state.users[userId].jwtToken = jwtToken;
      state.users[userId].refreshToken = refresh_token;

      // Set the currently logged-in user
      state.currentUser = userId;
    },
    clearUserTokens(state, userId) {
      // Clear user tokens
      if (state.users[userId]) {
        state.users[userId].jwtToken = null;
        state.users[userId].refreshToken = null;
      }

      if (state.currentUser === userId) {
        state.currentUser = null;
      }
      localStorage.setItem('vuexState', null);
    },
    setUserData(state, { userId, userData }) {
      // Set user data
      if (!state.users[userId]) {
        state.users[userId] = {};
      }
      state.users[userId].userData = userData;
    },
    clearUserData(state, userId) {
      // Clear user data
      if (state.users[userId]) {
        state.users[userId].userData = null;
      }
      state.currentUser = null;
      localStorage.setItem('vuexState', null);
    },
  },
  actions: {
    // You can define actions to handle token refresh or other user-related logic here
  },
  plugins: [
    (store) => {
      // Subscribe to store updates
      store.subscribe((mutation, state) => {
        // Save the state to local storage
        localStorage.setItem('vuexState', JSON.stringify(state));
      });
    },
  ],
})

export default store
