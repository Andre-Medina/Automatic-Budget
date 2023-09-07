/*
This is the JavaScript file that contains the logic for your 
*/


// Create an app instance
const app = Vue.createApp({
    // Define the data for your app
    data() {
      return {
        message: 'Hello Vue!',
        result_1: js_result_1,
        result_2: js_result_2,
        result_3: "This is result 3"
      };
    }
  });
  // Mount it to an element with id="app"
app.config.compilerOptions.delimiters = ['[[', ']]'];
app.mount('#app');

// Print to console
console.log("This is a message"); // Print a string
console.log(app); // Print a data property from vue instance
console.log(app.result_1, app.result_2, app.result_3); // Print multiple data properties from vue instance

console.log('heading to export')

// Export your component options as a module
export default {
    data() {
      console.log(data);
      return {
        data: null,
      };
    },
    mounted() {
      fetch("/data/level/1")
        .then((response) => response.json())
        .then((data) => {
          this.data = data;
        });
    },
  };


console.log(data)