/*
This is the JavaScript file that contains the logic for your 
*/



// Create an app instance
const app = Vue.createApp({

    //  ██████╗   █████╗  ████████╗  █████╗  
    //  ██╔══██╗ ██╔══██╗ ╚══██╔══╝ ██╔══██╗ 
    //  ██║  ██║ ███████║    ██║    ███████║ 
    //  ██║  ██║ ██╔══██║    ██║    ██╔══██║ 
    //  ██████╔╝ ██║  ██║    ██║    ██║  ██║ 
    //  ╚═════╝  ╚═╝  ╚═╝    ╚═╝    ╚═╝  ╚═╝ 
    //  
    data() {
      return {
        // accounts
        account_names: null,
        current_account: null,
        movement_types: null,
        current_movement_type: null,

        // description
        description_levels: {
          level1: null,
          level2: null
        },
        selected_code: [null],
        selected_levels: [null],
        
        // tags
        description_tag: {tag: null, name: null},

        // transactions
        transaction_index: 0,
        current_transaction: null,
        short_description: '',

        // are you sure
        are_you_sure_flag: null,
      };
    },

    
    //   ██████╗  ██████╗  ███╗   ███╗ ██████╗  ██╗   ██╗ ████████╗ ███████╗ ██████╗  
    //  ██╔════╝ ██╔═══██╗ ████╗ ████║ ██╔══██╗ ██║   ██║ ╚══██╔══╝ ██╔════╝ ██╔══██╗ 
    //  ██║      ██║   ██║ ██╔████╔██║ ██████╔╝ ██║   ██║    ██║    █████╗   ██║  ██║ 
    //  ██║      ██║   ██║ ██║╚██╔╝██║ ██╔═══╝  ██║   ██║    ██║    ██╔══╝   ██║  ██║ 
    //  ╚██████╗ ╚██████╔╝ ██║ ╚═╝ ██║ ██║      ╚██████╔╝    ██║    ███████╗ ██████╔╝ 
    //   ╚═════╝  ╚═════╝  ╚═╝     ╚═╝ ╚═╝       ╚═════╝     ╚═╝    ╚══════╝ ╚═════╝  
    //  
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
            code += '='
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

      //  █ █ █▀█ █▀▄ ▄▀█ ▀█▀ █▀▀    █▀▀ █ █ █▀█ █▀█ █▀▀ █▄ █ ▀█▀    ▀█▀ █▀█ ▄▀█ █▄ █ █▀ ▄▀█ █▀▀ ▀█▀ █ █▀█ █▄ █ 
      //  █▄█ █▀▀ █▄▀ █▀█  █  ██▄ ▄▄ █▄▄ █▄█ █▀▄ █▀▄ ██▄ █ ▀█  █  ▄▄  █  █▀▄ █▀█ █ ▀█ ▄█ █▀█ █▄▄  █  █ █▄█ █ ▀█ 
      //  
      // calculates current transaction
      async get_current_transaction(){
        //update are you sure
        if(this.current_account){
          try{
            const response = await fetch("/data/statement/" + this.current_account + '?transaction=' + this.transaction_index, {method:'GET'})
            const returned = await response.json()  
            console.log('new update transaction')
            this.current_transaction = returned.data.transaction
            this.deal_with_prediction(returned.data.prediction)
            return returned.data
          }catch(error){
            throw error
          }
        }else{
          return null
        }
      },


    },

    
    //  ███╗   ███╗ ███████╗ ████████╗ ██╗  ██╗  ██████╗  ██████╗  ███████╗ 
    //  ████╗ ████║ ██╔════╝ ╚══██╔══╝ ██║  ██║ ██╔═══██╗ ██╔══██╗ ██╔════╝ 
    //  ██╔████╔██║ █████╗      ██║    ███████║ ██║   ██║ ██║  ██║ ███████╗ 
    //  ██║╚██╔╝██║ ██╔══╝      ██║    ██╔══██║ ██║   ██║ ██║  ██║ ╚════██║ 
    //  ██║ ╚═╝ ██║ ███████╗    ██║    ██║  ██║ ╚██████╔╝ ██████╔╝ ███████║ 
    //  ╚═╝     ╚═╝ ╚══════╝    ╚═╝    ╚═╝  ╚═╝  ╚═════╝  ╚═════╝  ╚══════╝ 
    //  
    methods: {


      //  ▄▀▀▀▀ █▀▀▀ █▄    █ █▀▀▀ █▀▀▀▄ ▄▀▀▀▄ █    
      //  █  ▄▄ █▄▄  █ ▀▄  █ █▄▄  █▄▄▄▀ █▄▄▄█ █    
      //  █   █ █    █   ▀▄█ █    █  ▀█ █   █ █    
      //   ▀▀▀▀ ▀▀▀▀ ▀     ▀ ▀▀▀▀ ▀   ▀ ▀   ▀ ▀▀▀▀ 
      //  
      //  █▀█ █▀█ █ █▄ █ ▀█▀ █ █ ▄▀█ █   █ █ █▀▀ 
      //  █▀▀ █▀▄ █ █ ▀█  █  ▀▄▀ █▀█ █▄▄ █▄█ ██▄ 
      //  
      printValue(value){
        console.log(value);
        this.result_1 = value;
      },

      
      update_are_you_sure(){
        console.log(this.are_you_sure_flag)
        this.are_you_sure_flag = false
        return this.are_you_sure_flag
      },
      
      //  █▀▀▀▄ █▀▀▀ ▄▀▀▀▀ ▄▀▀▀ █▀▀▀▄ ▀▀█▀▀ █▀▀▄ ▀▀█▀▀ ▀▀█▀▀ ▄▀▀▀▀▄ █▄    █ 
      //  █   █ █▄▄  ▀▄▄▄  █    █▄▄▄▀   █   █▄▄▀   █     █   █    █ █ ▀▄  █ 
      //  █   █ █        █ █    █  ▀█   █   █      █     █   █    █ █   ▀▄█ 
      //  ▀▀▀▀  ▀▀▀▀ ▀▀▀▀   ▀▀▀ ▀   ▀ ▀▀▀▀▀ ▀      ▀   ▀▀▀▀▀  ▀▀▀▀  ▀     ▀ 
      //  
      //  █▀ █▀▀ ▀█▀    █▀▄ █▀▀ █▀ █▀▀ █▀█ █ █▀█ ▀█▀ █ █▀█ █▄ █ 
      //  ▄█ ██▄  █  ▄▄ █▄▀ ██▄ ▄█ █▄▄ █▀▄ █ █▀▀  █  █ █▄█ █ ▀█ 
      //  
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

        this.calculate_selected_levels_all(level)

        console.log('selected levels is \\\|/')
        console.log(this.selected_levels)

      },

      calculate_selected_levels_all(min_level = 1){

        for(let recalc_level = min_level + 1; recalc_level < this.selected_code.length; recalc_level ++){
          // console.log('calculating levels for ' + recalc_level)
          this.selected_levels[recalc_level] = this.calculate_selected_level(recalc_level)
        }
      },

      //  █▀▀ ▄▀█ █   █▀▀ █ █ █   ▄▀█ ▀█▀ █▀▀    █▀ █▀▀ █   █▀▀ █▀▀ ▀█▀ █▀▀ █▀▄    █   █▀▀ █ █ █▀▀ █   
      //  █▄▄ █▀█ █▄▄ █▄▄ █▄█ █▄▄ █▀█  █  ██▄ ▄▄ ▄█ ██▄ █▄▄ ██▄ █▄▄  █  ██▄ █▄▀ ▄▄ █▄▄ ██▄ ▀▄▀ ██▄ █▄▄ 
      //  
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

      //  █▀█ █▀▀ █▀ █▀▀ ▀█▀    █▀▀ █▀█ █▀▄ █▀▀ 
      //  █▀▄ ██▄ ▄█ ██▄  █  ▄▄ █▄▄ █▄█ █▄▀ ██▄ 
      //  
      // resets code
      reset_code(){
        this.selected_code = [null]
        this.selected_levels = [this.description_levels.level_1]
      },

      //  ▀▀█▀▀ █▀▀▀▄ ▄▀▀▀▄ █▄    █ ▄▀▀▀▀ ▄▀▀▀▄ ▄▀▀▀ ▀▀█▀▀ ▀▀█▀▀ ▄▀▀▀▀▄ █▄    █ 
      //    █   █▄▄▄▀ █▄▄▄█ █ ▀▄  █ ▀▄▄▄  █▄▄▄█ █      █     █   █    █ █ ▀▄  █ 
      //    █   █  ▀█ █   █ █   ▀▄█     █ █   █ █      █     █   █    █ █   ▀▄█ 
      //    ▀   ▀   ▀ ▀   ▀ ▀     ▀ ▀▀▀▀  ▀   ▀  ▀▀▀   ▀   ▀▀▀▀▀  ▀▀▀▀  ▀     ▀ 
      //  
      //  █▀█ █▀█ █▀▀ █ █    ▀█▀ █▀█ ▄▀█ █▄ █ █▀ ▄▀█ █▀▀ ▀█▀ █ █▀█ █▄ █ 
      //  █▀▀ █▀▄ ██▄ ▀▄▀ ▄▄  █  █▀▄ █▀█ █ ▀█ ▄█ █▀█ █▄▄  █  █ █▄█ █ ▀█ 
      //  
      prev_transaction(distance){
        if(this.transaction_index - distance < 0){
          console.log('far enough')
          return
        }
        this.transaction_index -= distance
      },

      
      //  █▄ █ █▀▀ ▀▄▀ ▀█▀    ▀█▀ █▀█ ▄▀█ █▄ █ █▀ ▄▀█ █▀▀ ▀█▀ █ █▀█ █▄ █ 
      //  █ ▀█ ██▄ █ █  █  ▄▄  █  █▀▄ █▀█ █ ▀█ ▄█ █▀█ █▄▄  █  █ █▄█ █ ▀█ 
      //  
      next_transaction(distance){
        this.transaction_index += distance
      },

      deal_with_prediction(prediction){
        if(prediction == null){
          return
        }else{
          console.log("prediction: ")
          // not dealing with tags atm
          // console.log(prediction.description_tag)

          console.log(prediction.selected_levels)
          console.log(this.selected_levels)
          this.selected_levels = prediction.selected_levels
          console.log(this.selected_levels)

          console.log(prediction.short_description)
          console.log(prediction.current_movement_type)
          // selected_levels
          // short_description
          // current_movement_type
          this.calculate_selected_levels_all()

        }


      },
      //  █▀ █ █ █▄▄ █▀▄▀█ █ ▀█▀    ▀█▀ █▀█ ▄▀█ █▄ █ █▀ ▄▀█ █▀▀ ▀█▀ █ █▀█ █▄ █ 
      //  ▄█ █▄█ █▄█ █ ▀ █ █  █  ▄▄  █  █▀▄ █▀█ █ ▀█ ▄█ █▀█ █▄▄  █  █ █▄█ █ ▀█ 
      //  
      submit_transaction(are_you_sure = false){
        
        if(!are_you_sure){
          if(
            this.current_transaction == null | 
            this.movement_types == null | 
            this.selected_code[0] == null 
            ){
              this.are_you_sure_flag = true
              return
          }
        }
        this.are_you_sure_flag = null


        if(this.current_account){
          fetch(
            "/data/statement/" + this.current_account + '?transaction=' + this.transaction_index, 
            {
              method:'POST',
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ 
                movement: this.current_movement_type,
                amount: clean_price(this.current_transaction.amount), 
                where: this.current_account, 
                code: this.calculate_initial_code,
                description_short: this.short_description,
                description_full: this.current_transaction.description,
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
    
    //  ███    ███  ██████  ██    ██ ███    ██ ████████ ███████ ██████  
    //  ████  ████ ██    ██ ██    ██ ████   ██    ██    ██      ██   ██ 
    //  ██ ████ ██ ██    ██ ██    ██ ██ ██  ██    ██    █████   ██   ██ 
    //  ██  ██  ██ ██    ██ ██    ██ ██  ██ ██    ██    ██      ██   ██ 
    //  ██      ██  ██████   ██████  ██   ████    ██    ███████ ██████  
    //  
    mounted() {
      //  █   █▀▀ █ █ █▀▀ █   █▀ 
      //  █▄▄ ██▄ ▀▄▀ ██▄ █▄▄ ▄█ 
      //  
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

      //  █▀ ▀█▀ ▄▀█ ▀█▀ █▀▀ █▀▄▀█ █▀▀ █▄ █ ▀█▀   ▄▀█ █▀▀ █▀▀ █▀█ █ █ █▄ █ ▀█▀ █▀ 
      //  ▄█  █  █▀█  █  ██▄ █ ▀ █ ██▄ █ ▀█  █    █▀█ █▄▄ █▄▄ █▄█ █▄█ █ ▀█  █  ▄█ 
      //  
      fetch("/data/config/accounts", {method:'GET'})
        .then((response) => response.json())
        .then((returned) => {
          this.account_names = returned.data;
        });

        
      //  █▀▄▀█ █▀█ █ █ █▀▀ █▀▄▀█ █▀▀ █▄ █ ▀█▀    ▀█▀ █▄█ █▀█ █▀▀ █▀ 
      //  █ ▀ █ █▄█ ▀▄▀ ██▄ █ ▀ █ ██▄ █ ▀█  █  ▄▄  █   █  █▀▀ ██▄ ▄█ 
      //  
      fetch("/data/config/movement_types", {method:'GET'})
        .then((response) => response.json())
        .then((returned) => {
          this.movement_types = returned.data;
        });

      //  █▀█ ▀█▀ █ █ █▀▀ █▀█ 
      //  █▄█  █  █▀█ ██▄ █▀▄ 
      //  
      // console.log(movement_types)
      
    },
    

  });


//  ███████╗ ██╗  ██╗ ████████╗ 
//  ██╔════╝ ╚██╗██╔╝ ╚══██╔══╝ 
//  █████╗    ╚███╔╝     ██║    
//  ██╔══╝    ██╔██╗     ██║    
//  ███████╗ ██╔╝ ██╗    ██║    
//  ╚══════╝ ╚═╝  ╚═╝    ╚═╝    
//  
  // Mount it to an element with id="app"
app.config.compilerOptions.delimiters = ['[[', ']]'];
app.mount('#app');

// Print to console
console.log("This is a message"); // Print a string
console.log(app); // Print a data property from vue instance
console.log(app.result_1, app.result_2, app.result_3); // Print multiple data properties from vue instance

console.log('starting mounted')



function clean_price(price) {
  return parseFloat(price.replace(/[^0-9.]+/g,""));
}