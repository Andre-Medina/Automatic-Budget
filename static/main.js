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
        result_3: "This is result 3",
        description_levels: {
          level1: null,
          level2: null
        },
        selected_index: [null],
        selected_levels: [null]
      };
    },
    computed: {
      level_depth(){
        console.log('Depth is now ' + this.selected_index.length)
        return this.selected_index.length
      }      
    },
    methods: {
      printValue(value){
        console.log(value);
        this.result_1 = value;
      },
      
      // sets the desction to selected index
      set_description(index, level){
        console.log('setting ' + level + " to a index of " + index);
        while(this.selected_index.length < level + 2){
          this.selected_levels.push(null)
          this.selected_index.push(null)
        }
        console.log(this.selected_levels)
        console.log(this.selected_levels[level])
        setTimeout({},10)
        this.selected_index[level] = index

        console.log('description is \\\|/')
        console.log(this.selected_index)

        for(let recalc_level = level + 1; recalc_level < this.selected_index.length; recalc_level ++){
          console.log('calculating levels for ' + recalc_level)
          this.selected_levels[recalc_level] = this.calculate_selected_level(recalc_level)
        }
        console.log(this.selected_levels)
      },

      // returns the list for the correct level
      calculate_selected_level(calc_level){
    
        //console.log('WORKING OUT LEVEL: ' + calc_level)

        // copys the description levels
        let selected = JSON.parse(JSON.stringify(this.description_levels.level_2));


        for(let [level, index] of this.selected_index.entries()){
          
          // console.log('level: ' + level)
          // console.log('index: ' + index)

          // if level doesnt exist, breaks
          if(index == null){
            break
          }
          // if the level is root, skips
          if(level == 0){
            continue
          }
          // if the level is greater than whats needed, skips it
          if(level >= calc_level){
            break
          }
          // if the next level is null, sets it as null
          if(selected[index] == null){
            selected = null
            break
          }
          
          // otherwise good to use index to move to next selection
          selected = selected[index].next
        }
        
        // returns and prints selected
        // console.log(selected)

        return selected
      }
    },
    mounted() {
      fetch("/data/level/1", {method:'GET'})
        .then((response) => response.json())
        .then((returned) => {
          console.log('initial reponse:');
          console.log(returned);
          this.description_levels.level_1 = returned.data;
          this.selected_levels[0] = this.description_levels.level_1;
        });
      fetch("/data/level/2", {method:'GET'})
        .then((response) => response.json())
        .then((returned) => {
          this.description_levels.level_2 = returned.data;
        });

    },
    

  });
  // Mount it to an element with id="app"
app.config.compilerOptions.delimiters = ['[[', ']]'];
app.mount('#app');

// Print to console
console.log("This is a message"); // Print a string
console.log(app); // Print a data property from vue instance
console.log(app.result_1, app.result_2, app.result_3); // Print multiple data properties from vue instance

console.log('starting mounted')
