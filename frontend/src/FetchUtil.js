// FetchUtil.js
import store from './store.js';

export default function fetchUtil({ endpoint, method = 'GET', headers = {}, data = null, user_id = null }) {
  const fullUrl = `http://127.0.0.1:5000/${endpoint}`;

  return new Promise(async (resolve, reject) => {
    try {
      let jwtToken = null;

      // If the endpoint is not 'loginuser', fetch JWT token from Vuex store
      if (endpoint !== 'loginuser' && endpoint !== 'refresh' && endpoint !== 'newuser') {
        const userData = store.state.users[user_id];
        if (userData && userData.jwtToken) {
          jwtToken = userData.jwtToken;
        } else {
          throw new Error(`JWT token not available for user with ID ${user_id}`);
        }
      }

      const response = await fetch(fullUrl, {
        method,
        headers: {
          ...headers,
          Authorization: jwtToken ? `Bearer ${jwtToken}` : undefined,
        },
        body: data ? JSON.stringify(data) : undefined,
      });

      if (!response.ok) {
        // Handle token expiration and refresh
        if (response.status === 401) {
          // Token expired, attempt to refresh
          const userID = store.state.currentUser
          console.log("refreshing")
          try {
            const refreshToken = store.state.users[userID]?.refreshToken;
            if (!refreshToken) {
              throw new Error(`Refresh token not available for user with ID ${userID}`);
            }
            // Use the refresh token to get new tokens
            const refreshResponse = await fetch("http://127.0.0.1:5000/refresh", {
              method: 'GET',
              headers: {
                ...headers,
                Authorization: refreshToken ? `Bearer ${refreshToken}` : undefined,
              },
            });
            // console.log(refreshResponse);
            const refreshData = await refreshResponse.json();
            console.log(refreshData);
            // Update Vuex store with new tokens
            store.commit('setUserTokens', {
              userId: userID,
              jwtToken: refreshData.tokens[0].access,
              refresh_token: refreshData.tokens[0].refresh,
            });

            // Retry the original request with the new token
            const retryResponse = await fetchUtil({ endpoint, method, headers, data, user_id });

            resolve(retryResponse);
            return;
          } catch (refreshError) {
            reject(refreshError);
            return;
          }
        }
        
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const responseData = await response.json();
      resolve(responseData);
    } catch (error) {
      reject(error);
    }
  });
}
