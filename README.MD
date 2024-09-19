## Description
A grocery store app using the Flask framework as a server, SQLite database and Vue.JS frontend was created. The app allows users to browse products by section/category, add
products to their cart, checkout and complete their order. The store manager can add/edit/delete products that will then instantaneously reflect in the shop. Each function of the app was carefully understood and the wireframe analyzed in depth before
implementation to avoid any logical errors.
## Technologies used
- Flask, vueJS and SQLite: Flask is a microframework for Python web development, VueJS
	is an amazing Javascript framework for UI and frontend and SQLite is a lightweight
	database engine that is embedded in Python all three are lightweight and easy to use,
	making it the perfect choice for this project.

- Flask-RESTful: Flask-RESTful is an extension for Flask that was used because it makes it
	easy to create RESTful APIs.

- CORS: CORS is a mechanism that allows web applications to make cross-origin requests.
	This will allow users to access the API’s from other domains.

- Requests: It was used to make HTTP requests to the CRUD API’s in the application to get the sections/products to display and for various other purposes.

- JSON: A lightweight data-interchange format which was used to serialize and deserialize
	data in the application, making it easy to pass data to and receive data from the API.
 
- OS: Part of the Python standard library, It provides access to operating system functionality used primarily to generate the app secret key, so that sessions can be enabled to make the app multiuser compatible.

- base64: A standard encoding scheme that was used to encode binary data into ASCII
	characters in order to handle the SQLite blob data type in product image fetch & display.

- datetime: Part of the Python standard library, it provides classes for representing dates
	and times so that they can be stored in the database during order creation and updation.

#### Video: [Click Here](https://youtu.be/IngXbmWWplw "Click Here")