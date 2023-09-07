/*
This is the JavaScript file that contains the logic for your 
*/


// Create a vue instance
var app = new Vue({
    // Bind it to an element with id="app"
    el: '#app',
    // Define the data for your app
    delimiters: ['[[', ']]'],
    data: {
        message: 'Hello Vue!',
        result_1: js_result_1,//document.getElementById("data_result_1").innerHTML,
        result_2: js_result_2,
        result_3: "This is result 3" // Define result_3 variable
    }
});

// Print to console
console.log("This is a message"); // Print a string
console.log(app.message); // Print a data property from vue instance
console.log(app.result_1, app.result_2, app.result_3); // Print multiple data properties from vue instance

console.log(js_result_1)


// export default {
//   data() {
//     return {
//       data: null,
//     };
//   },
//   mounted() {
//     fetch("/data/level/1")
//       .then((response) => response.json())
//       .then((data) => {
//         this.data = data;
//       });
//   },
// };