/*
This is the JavaScript file that contains the logic for your 
*/

const account_names = {
  'pink_card': 'bd',
  'blue_card': 'be',
  'loan': '2=-l',
}


// Create an app instance
const app = Vue.createApp({
    // Define the data for your app
    data() {
      return {
        // accounts
        account_names: account_names,
        current_account: null,


        // description
        description_levels: {
          level1: null,
          level2: null
        },
        selected_code: [null],
        selected_levels: [null],
        
        // transactions
        transaction_index: 0,
        current_transaction: null,
        short_description: '',
      };
    },
    computed: {

      // calculates depth
      level_depth(){
        console.log('Depth is now ' + this.selected_code.length)
        return this.selected_code.length
      },
      
      // calculates level code
      calculate_initial_code(){
        console.log('calculating code')

        let code = ""
        
        // for each level selected
        for(let level in this.selected_levels){
          
          // adds a dash 
          if(level == 1){
            code += '-'
          }

          // if the level exists, and the level includes the seleceted value
          if(this.selected_levels[level] && Object.keys(this.selected_levels[level]).includes(this.selected_code[level])){

            // adds it, otherwise breaks
            code += this.selected_code[level]
          }else{
            break
          }
        }
        
        // returns code
        // console.log(code)
        return code
      },


    },
    methods: {


      printValue(value){
        console.log(value);
        this.result_1 = value;
      },
      
      // sets the desction to selected code
      set_description(code, level){
        console.log('setting ' + level + " to a code of " + code);
        while(this.selected_code.length < level + 2){
          this.selected_levels.push(null)
          this.selected_code.push(null)
        }
        // console.log('selected levels is \\\|/')
        // console.log(this.selected_levels)
        // console.log(this.selected_levels[level])
        
        this.selected_code[level] = code

        console.log('selected code is \\\|/')
        console.log(this.selected_code)

        for(let recalc_level = level + 1; recalc_level < this.selected_code.length; recalc_level ++){
          // console.log('calculating levels for ' + recalc_level)
          this.selected_levels[recalc_level] = this.calculate_selected_level(recalc_level)
        }
        console.log('selected levels is \\\|/')
        console.log(this.selected_levels)

      },

      // returns the list for the correct level
      calculate_selected_level(calc_level){
    
        //console.log('WORKING OUT LEVEL: ' + calc_level)

        // copys the description levels
        let selected = JSON.parse(JSON.stringify(this.description_levels.level_2));


        for(let [level, code] of this.selected_code.entries()){
          
          // console.log('level: ' + level)
          // console.log('code: ' + code)

          // if level doesnt exist, breaks
          if(code == null){
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
          if(selected[code] == null){
            selected = null
            break
          }
          
          // otherwise good to use code to move to next selection
          selected = selected[code].next
        }
        
        // returns and prints selected
        // console.log(selected)

        return selected
      },

      // resets code
      reset_code(){
        this.selected_code = [null]
        this.selected_levels = [this.description_levels.level_1]
      },

      // statements

      prev_transaction(){
        if(this.transaction_index <= 0){
          console.log('far enough')
          return
        }
        this.transaction_index --
        this.update_current_transaction()
      },
      next_transaction(){
        this.transaction_index ++
        this.update_current_transaction()
      },
      // calculates current transaction
      update_current_transaction(){
        if(this.current_account){
          fetch("/data/statement/" + this.current_account + '?transaction=' + this.transaction_index, {method:'GET'})
          .then((response) => response.json())
          .then((returned) => {
            console.log('data: for index ' + this.transaction_index);
            console.log(returned);
            this.current_transaction = returned.data
          });
        }
      },

      submit_transaction(){
        if(this.current_account){
          fetch(
            "/data/statement/" + this.current_account + '?transaction=' + this.transaction_index, 
            {
              method:'POST',
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ 
                amount: this.current_transaction.amount, 
                where: this.current_account, 
                code: this.calculate_initial_code,
                desc: this.short_description,
                date: this.current_transaction.date              
              })            
            })
            .then((response) => response.json())
            .then((returned) => {
              console.log(returned);
            });
        }
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
      this.update_current_transaction();
      
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
