<template>
    <div></div>
  </template>
  
  <script>
  export default {
    props: {
      endpoint: {
        type: String,
        required: true,
      },
      method: {
        type: String,
        default: 'GET',
      },
      headers: {
        type: Object,
        default: () => ({}),
      },
      data: {
        type: [Object, String],
        default: null,
      },
      // Uncomment the following lines when handling JWT tokens
      jwtToken: {
        type: String,
        default: null,
      },
    },
    computed: {
      // Compute the full URL by combining the base URL and the endpoint
      fullUrl() {
        return `http://127.0.0.1:5000/${this.endpoint}`;
      },
    },
    methods: {
      async makeRequest() {
        try {
          const response = await fetch(this.fullUrl, {
            method: this.method,
            headers: {
              ...this.headers,
              // Uncomment the following lines when you want to handle JWT tokens
              Authorization: `Bearer ${this.jwtToken}`,
            },
            body: this.data ? JSON.stringify(this.data) : undefined,
          });
  
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
  
          const responseData = await response.json();
  
          // Emit the response data to the parent component
          this.$emit('response', responseData);
        } catch (error) {
          // Handle errors
          console.error(error);
        }
      },
    },
    mounted() {
      // Make the request when the component is mounted
      this.makeRequest();
    },
  };
  </script>
  
  <style scoped>
  /* Add your custom styles if needed */
  </style>
  