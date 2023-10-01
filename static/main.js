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
        // general
        temp_alert: "",
        show_alert: false,
        null: null,

        // accounts
        account_names: null,
        current_account: null,
        movement_types: null,
        current_movement_type: null,

        // description
        description_levels: {
          level1: null,
          level2: null,
          level3: null
        },
        selected_code: [null],
        selected_levels: [null],
        
        // tags
        code_tag: {selected_tag: [null], extra: null},
        tag_selected_levels: [null],

        // transfer
        transfer_account: null,
        transfer_account_extra: "",

        // transactions
        transaction_index: 0,
        current_transaction: null,
        transaction_classified: false,
        short_description: '',

        // commiting
        new_data: false,
        commit_message: "",
        are_you_sure_message: "",

        // extra data
        tax: 0
      };
    },

    // routes: [
    //   {path: ''}
    // ],
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

      tag_level_depth(){
        console.log("calcing tag level depth:")
        console.log(this.code_tag)
        console.log(this.code_tag.selected_tag)
        console.log(this.tag_selected_levels[0])
        console.log(Object.keys(this.tag_selected_levels[0]).length > 0)
        console.log('Tag depth is now' + this.code_tag.selected_tag.length)
        return this.code_tag.selected_tag.length
      },
      
      // calculates level code
      calculate_initial_code(){
        console.log('calculating code')

        let code = ""
        
        // for each level selected
        for(let level in this.selected_levels){
          

          // if the level exists, and the level includes the seleceted value
          if(this.selected_levels[level] && Object.keys(this.selected_levels[level]).includes(this.selected_code[level])){

            // adds it, otherwise breaks
            code += this.selected_code[level]
          }else{
            break
          }
          // adds a dash 
          if(level == 0){
            code += '='
          }
        }

        console.log(this.code_tag.selected_tag[0])
        if(this.code_tag.selected_tag[0] && this.code_tag.selected_tag[0] != '-'){
          code += '-'

          for(let level in this.tag_selected_levels){

            // if the level exists, and the level includes the seleceted value
            if(this.tag_selected_levels[level] && Object.keys(this.tag_selected_levels[level]).includes(this.code_tag.selected_tag[level])){

              // adds it, otherwise breaks
              code += this.code_tag.selected_tag[level]
            }else{
              break
            }
          }
        }

        if(this.code_tag.extra){
          code += this.code_tag.extra
        }
        
        // returns code
        console.log(code)

        return code
      },

      //  █ █ █▀█ █▀▄ ▄▀█ ▀█▀ █▀▀    █▀▀ █ █ █▀█ █▀█ █▀▀ █▄ █ ▀█▀    ▀█▀ █▀█ ▄▀█ █▄ █ █▀ ▄▀█ █▀▀ ▀█▀ █ █▀█ █▄ █ 
      //  █▄█ █▀▀ █▄▀ █▀█  █  ██▄ ▄▄ █▄▄ █▄█ █▀▄ █▀▄ ██▄ █ ▀█  █  ▄▄  █  █▀▄ █▀█ █ ▀█ ▄█ █▀█ █▄▄  █  █ █▄█ █ ▀█ 
      //  
      // calculates current transaction
      async get_current_transaction(){
        this.reset()
        

        // this.push({query: { plan: 'private' }})

        //update are you sure
        if(this.current_account){
          try{
            const response = await fetch("/data/statement/" + this.current_account + '?transaction=' + this.transaction_index, {method:'GET'})
            if (!response.ok) { // if the status code is not 200-299
              throw new Error(response.statusText); // throw an error with the status text
            }
            console.log(response)
            const returned = await response.json()  
            console.log(returned)

            // if nothing was found (206 is for nothing found)
            if (returned.status == 206){

              this.alert('too far', 1000)

              // sets transaction index to the max
              this.transaction_index = returned.data.max_transactions - 1
              return null
            }

            // otherwise updates the with the new
            console.log('new update transaction')

            // extracts the data
            this.current_transaction = returned.data.transaction
            this.transaction_classified = returned.data.classified
            this.deal_with_prediction(returned.data.prediction)
            
            // sets flag and returns
            this.new_data = true
            return returned.data

          // otherwise if there was an error or a bad response code
          }catch(error){
            console.error(error); // log the error to the console
            this.alert(error); // show an alert with the error message
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

      
      alert(alert, timeout = 2000){
        this.temp_alert = alert;
        this.show_alert = true;
        console.log('starting timeout')
        setTimeout(() => {
          console.log('timeout reached')
          this.show_alert = false
        }, timeout);
      },

      //  █▀█ █▀█ █ █▄ █ ▀█▀ █ █ ▄▀█ █   █ █ █▀▀ 
      //  █▀▀ █▀▄ █ █ ▀█  █  ▀▄▀ █▀█ █▄▄ █▄█ ██▄ 
      //  
      printValue(value){
        console.log(value);
        this.result_1 = value;
      },

      
      change_account(account){
        this.current_account = account
        this.reset('all but account')
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
      set_description(code, level, tag = false){

        var selected_code

        if (tag){
          console.log('calculating for tag')
          selected_code = this.code_tag.selected_tag
        }else{
          console.log('calculating for normal')
          selected_code = this.selected_code
        }

        console.log('setting ' + level + " to a code of " + code);
        while(selected_code.length < level + 2){
          // selected_levels.push(null)
          selected_code.push(null)
        }
        // console.log('selected levels is \\\|/')
        // console.log(selected_levels)
        // console.log(selected_levels[level])
        
        selected_code[level] = code

        console.log('selected code is \\\|/')
        console.log(selected_code)

        this.update_selected_levels(tag, level)

        console.log('selected levels is \\\|/')
        if (tag){
          this.code_tag.selected_tag = selected_code
          console.log(this.code_tag.selected_tag)
          console.log(this.tag_selected_levels)
        }else{
          this.selected_code = selected_code
          console.log(this.selected_code)
          console.log(this.selected_levels)
        }
      },

      update_selected_levels(tag = false, min_level = 0){
        var selected_levels
        var description_levels
        var selected_code

        if (tag){
          selected_levels = this.tag_selected_levels
          description_levels = this.description_levels.level_3
          selected_code = this.code_tag.selected_tag
        }else{
          selected_levels = this.selected_levels
          description_levels = this.description_levels.level_2
          selected_code = this.selected_code
        }

        this.calculate_selected_levels_all(min_level, selected_code, selected_levels, description_levels, tag)

        if (tag){
          this.code_tag.selected_tag = selected_code
          this.tag_selected_levels = selected_levels
        }else{
          this.selected_levels = selected_levels
          this.selected_code = selected_code
        }
      },

      calculate_selected_levels_all(min_level = 0, selected_code, selected_levels, description_levels, tag = false){

        for(let recalc_level = min_level + 1; recalc_level < selected_code.length; recalc_level ++){
          // console.log('calculating levels for ' + recalc_level)
          selected_levels[recalc_level] = this.calculate_selected_level(
            recalc_level, 
            description_levels, 
            selected_code,
            tag
            )
        }
      },

      //  █▀▀ ▄▀█ █   █▀▀ █ █ █   ▄▀█ ▀█▀ █▀▀    █▀ █▀▀ █   █▀▀ █▀▀ ▀█▀ █▀▀ █▀▄    █   █▀▀ █ █ █▀▀ █   
      //  █▄▄ █▀█ █▄▄ █▄▄ █▄█ █▄▄ █▀█  █  ██▄ ▄▄ ▄█ ██▄ █▄▄ ██▄ █▄▄  █  ██▄ █▄▀ ▄▄ █▄▄ ██▄ ▀▄▀ ██▄ █▄▄ 
      //  
      // returns the list for the correct level
      calculate_selected_level(calc_level, level, selected_code, tag = false){
        //console.log('WORKING OUT LEVEL: ' + calc_level)

        // copys the description levels
        let selected = JSON.parse(JSON.stringify(level));

        for(let [level, code] of selected_code.entries()){
          
          // console.log('level: ' + level)
          // console.log('code: ' + code)

          // if level doesnt exist, breaks
          if(code == null){
            break
          }
          // if the level is root, skips
          if((level == 0) && (!tag)){
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
      reset(what = 'choices'){
        switch (what) {
          case 'are_you_sure':
            this.are_you_sure_message = ""
            this.commit_message = ""
            break;

          case 'tax':
            this.tax = 0
            break;
          
          case 'code':
            console.log('resetting code')
            this.selected_code = [null]
            this.selected_levels = [this.description_levels.level_1]
            console.log('done')
            break;
        
          case 'tag':
            this.tag_selected_levels = [this.description_levels.level_3]
            this.code_tag = {selected_tag: [null], extra: null}
            break;

          case 'index':
            this.transaction_index = 0
            this.commit_message = ""
            this.transaction_classified = false
            this.current_transaction = null
            break;
          
          case 'description':
            this.short_description = ""
            break;

          case 'movement':
            this.current_movement_type = null
            break;
            
          case 'account':
            this.current_account = null;
            break;
          
          case 'transfer':
            this.transfer_account = null;
            this.transfer_account_extra = "";
            break;

          case 'all':
            this.reset('account')
            
          case 'all but account':
            this.reset('index')
            this.reset('movement')

          case 'choices':
            this.reset('are_you_sure')
            this.reset('tag')
            this.reset('transfer')
            this.reset('description')
            this.reset('code')
            this.reset('tax')
            break;


          default:
            break;
        }

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
          this.alert('far enough', 1000)
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

      //  █▀▄ █▀▀ ▄▀█ █      █ █ █ █ ▀█▀ █ █    █▀█ █▀█ █▀▀ █▀▄ █ █▀▀ ▀█▀ █ █▀█ █▄ █ 
      //  █▄▀ ██▄ █▀█ █▄▄ ▄▄ ▀▄▀▄▀ █  █  █▀█ ▄▄ █▀▀ █▀▄ ██▄ █▄▀ █ █▄▄  █  █ █▄█ █ ▀█ 
      //  
      deal_with_prediction(prediction){

        // if there were no predictions returned
        if(prediction == null){
          
          // might add something to reset other variables?

          return
        }else{

          // otherwise deals witht he prediction
          console.log("prediction: ")
          // not dealing with tags atm
          // console.log(prediction.code_tag)

          // console.log(prediction.selected_levels)
          // console.log(this.selected_code)

          // deals with prediction tag
          if(prediction.code_tag != null){
            // have not tested this yet. unsure if working
            console.log('reading tag')
            console.log(prediction.code_tag)
            // // if singel tag
            // if(prediction.code_tag.selected_tag){
            //   this.code_tag = {
            //     selected_tag: [prediction.code_tag.selected_tag, prediction.code_tag.extra]
            //     extra: null
            //   }
            // }
            this.code_tag = prediction.code_tag
          }

          // updates the selection code
          if(prediction.selected_code != null){
            this.selected_code = prediction.selected_code.map(word => word.toLowerCase());
          }else{
            this.reset()
          }

          // updates the short_description
          if(prediction.description_short != null){
            this.short_description = prediction.description_short;
          }else{
            this.reset('description')
          }
          
          // updates movement
          if(prediction.movement != null){
            this.current_movement_type = prediction.movement
          }else{
            this.reset('movement')
          }
          
          // transfer account
          if(prediction.transfer_account != null){
            this.transfer_account = Object.keys(this.account_names).find(key => this.account_names[key] == prediction.transfer_account)
          }else{
            this.reset('transfer')
          }
          
          // tax

          if(prediction.tax != null){
            this.tax = prediction.tax
          }else{
            this.reset('tax')
          }

          // console.log(prediction.short_description)
          // console.log(prediction.current_movement_type)
          // // selected_levels
          // short_description
          // current_movement_type
          
          // recalculates the selected levels due to changing data
          this.update_selected_levels(false)
          this.update_selected_levels(true)
        }


      },
      //  █▀ █ █ █▄▄ █▀▄▀█ █ ▀█▀    ▀█▀ █▀█ ▄▀█ █▄ █ █▀ ▄▀█ █▀▀ ▀█▀ █ █▀█ █▄ █ 
      //  ▄█ █▄█ █▄█ █ ▀ █ █  █  ▄▄  █  █▀▄ █▀█ █ ▀█ ▄█ █▀█ █▄▄  █  █ █▄█ █ ▀█ 
      //  
      submit_transaction(are_you_sure = false){
        
        // resets are you sure
        this.reset('are_you_sure')

        // if not sure
        if(!are_you_sure){

          // checking description
          if(this.short_description == ""){
            this.are_you_sure_message += " There is no description."
          }

          // checking if it was classfied already
          if(this.transaction_classified){
            this.are_you_sure_message += " This transaction has already been classified."
          }
          
          // checking current transaction
          if(this.current_transaction == null){
            this.are_you_sure_message += " There is no transaction"
          }

          // checking movement type
          if(this.current_movement_type == null){
            this.are_you_sure_message += " There is no movement type"
          }
          if(this.current_movement_type == 'transfer'){
            console.log('checking transfer')

            // its transfering so checking transfer account
            if(this.transfer_account == null){
              console.log('missing transfer')
              this.are_you_sure_message += " There is no transfer account specified"
            }
          }else{

            // its not transferring so checking code
            if(this.selected_code[0] == null){
              this.are_you_sure_message += " There is no code selected"
            }
          }
          
          // if anything was missing, returns
          if(this.are_you_sure_message != ""){
            return
          }
        }
        

        if(this.current_account){
          fetch(
            "/data/statement/" + this.current_account + '?transaction=' + this.transaction_index, 
            {
              method:'POST',
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ 
                movement: this.current_movement_type,
                amount: clean_price(this.current_transaction.amount) * (this.current_movement_type == 'output' ? -1: 1), 
                tax: clean_price(this.tax),
                where: this.current_account, 
                description_short: this.short_description,
                description_full: this.current_transaction.description,
                date: this.current_transaction.date,
                code:             this.current_movement_type != 'transfer'? this.calculate_initial_code : null,
                transfer_account: this.current_movement_type != 'transfer'? null : (this.account_names[this.transfer_account] + this.transfer_account_extra),
              })            
            })
            .then((response) => {
              if (response.ok) { // if the status code is 200-299
                return response.json(); // parse the response as JSON
              } else {
                throw new Error(response.statusText); // throw an error with the status text
              }
            })
            .then((returned) => {
              console.log(returned);
              this.commit_message = returned.message
              this.new_data = false
            })
            .catch((error) => {
              console.error(error); // log the error to the console
              this.commit_message = error
              this.alert(error); // show an alert with the error message
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
        .then((response) => {
          if (response.ok) { // if the status code is 200-299
            return response.json(); // parse the response as JSON
          } else {
            throw new Error(response.statusText); // throw an error with the status text
          }
        })
        .then((returned) => {
          console.log('initial reponse:');
          console.log(returned);
          this.description_levels.level_1 = returned.data;
          this.selected_levels[0] = this.description_levels.level_1;
        })
        .catch((error) => {
          console.error(error); // log the error to the console
          this.alert(error); // show an alert with the error message
        });

      fetch("/data/level/2", {method:'GET'})
        .then((response) => {
          if (response.ok) { // if the status code is 200-299
            return response.json(); // parse the response as JSON
          } else {
            throw new Error(response.statusText); // throw an error with the status text
          }
        })
        .then((returned) => {
          this.description_levels.level_2 = returned.data; // assign the data to your state
        })
        .catch((error) => {
          console.error(error); // log the error to the console
          this.alert(error); // show an alert with the error message
        });
        
      fetch("/data/level/3", {method:'GET'})
        .then((response) => {
          if (response.ok) { // if the status code is 200-299
            return response.json(); // parse the response as JSON
          } else {
            throw new Error(response.statusText); // throw an error with the status text
          }
        })
        .then((returned) => {
          this.description_levels.level_3 = returned.data; // assign the data to your state
          this.tag_selected_levels[0] = this.description_levels.level_3;
          console.log('tag selected levels:')
          console.log(this.tag_selected_levels)
        })
        .catch((error) => {
          console.error(error); // log the error to the console
          this.alert(error); // show an alert with the error message
        });


      //  █▀ ▀█▀ ▄▀█ ▀█▀ █▀▀ █▀▄▀█ █▀▀ █▄ █ ▀█▀   ▄▀█ █▀▀ █▀▀ █▀█ █ █ █▄ █ ▀█▀ █▀ 
      //  ▄█  █  █▀█  █  ██▄ █ ▀ █ ██▄ █ ▀█  █    █▀█ █▄▄ █▄▄ █▄█ █▄█ █ ▀█  █  ▄█ 
      //  
      fetch("/data/config/accounts", {method:'GET'})
        .then((response) => {
          if (response.ok) { // if the status code is 200-299
            return response.json(); // parse the response as JSON
          } else {
            throw new Error(response.statusText); // throw an error with the status text
          }
        })
        .then((returned) => {
          this.account_names = returned.data;
        })
        .catch((error) => {
          console.error(error); // log the error to the console
          this.alert(error); // show an alert with the error message
        });

        
      //  █▀▄▀█ █▀█ █ █ █▀▀ █▀▄▀█ █▀▀ █▄ █ ▀█▀    ▀█▀ █▄█ █▀█ █▀▀ █▀ 
      //  █ ▀ █ █▄█ ▀▄▀ ██▄ █ ▀ █ ██▄ █ ▀█  █  ▄▄  █   █  █▀▀ ██▄ ▄█ 
      //  
      fetch("/data/config/movement_types", {method:'GET'})
        .then((response) => {
          if (response.ok) { // if the status code is 200-299
            return response.json(); // parse the response as JSON
          } else {
            throw new Error(response.statusText); // throw an error with the status text
          }
        })
        .then((returned) => {
          this.movement_types = returned.data;
        })
        .catch((error) => {
          console.error(error); // log the error to the console
          this.alert(error); // show an alert with the error message
        });

      //  █▀█ ▀█▀ █ █ █▀▀ █▀█ 
      //  █▄█  █  █▀█ ██▄ █▀▄ 
      //  
      // console.log(movement_types)
      
      
    
      //  █▀█ █▀▀ ▄▀█ █▀▄ █ █▄ █ █▀▀   █▀█ ▄▀█ █▀█ ▄▀█ █▀▄▀█   █ █ ▄▀█ █▀█ █▀ 
      //  █▀▄ ██▄ █▀█ █▄▀ █ █ ▀█ █▄█   █▀▀ █▀█ █▀▄ █▀█ █ ▀ █   ▀▄▀ █▀█ █▀▄ ▄█ 
      //
        // onMounted() {
          // async () => {
            // console.log("READING PARAMS")
            // await this.$router.isReady();
            // console.log("READY")
            // console.log(this.$router.currentRoute.value);  // all values have been initialized now
      console.log('before');
      var x = async () => {
        await this.$router.isReady();
        console.log('UPDATING FROM ROUTE PARAMS')
        console.log(this.$route.query)
        // this.code_tag = JSON.parse(decodeURIComponent(this.$route.query.code_tag));
        // this.selected_code = JSON.parse(decodeURIComponent(this.$route.query.selected_code));
        // if(this.$route.query.description_short){
        //   console.log(this.$route.query.description_short)
        //   this.short_description = decodeURIComponent(this.$route.query.description_short);
        // }
        // this.current_movement_type = decodeURIComponent(this.$route.query.current_movement_type);
        var temp

        temp = decodeURIComponent(this.$route.query.transaction_index)
        if(!isNaN(temp)){
          console.log('found index: ' + temp)
          this.transaction_index = parseInt(temp);
        }else{
          console.log('could not find index: ' + temp +', resetting')
          this.reset('index')
        }

        temp = decodeURIComponent(this.$route.query.current_account)
        if(!(temp == null)){   // && Object.keys(this.account_names).includes(temp)
          console.log('found account: ' + temp)
          this.current_account = temp;
        }else{
          console.log('could not find account: ' + temp +', resetting')
          this.reset('account')
        }
        
      };
      x()
      console.log('after');

    },
        
    //  ██    ██ ██████  ██████   █████  ████████ ███████ ██████  
    //  ██    ██ ██   ██ ██   ██ ██   ██    ██    ██      ██   ██ 
    //  ██    ██ ██████  ██   ██ ███████    ██    █████   ██   ██ 
    //  ██    ██ ██      ██   ██ ██   ██    ██    ██      ██   ██ 
    //   ██████  ██      ██████  ██   ██    ██    ███████ ██████  
    //  
    updated(){
      
      //  █ █ █▀█ █▀▄ ▄▀█ ▀█▀ █ █▄ █ █▀▀   █▀█ ▄▀█ █▀█ ▄▀█ █▀▄▀█   █▀█ █ █ █▀▀ █▀█ █▄█ 
      //  █▄█ █▀▀ █▄▀ █▀█  █  █ █ ▀█ █▄█   █▀▀ █▀█ █▀▄ █▀█ █ ▀ █   ▀▀█ █▄█ ██▄ █▀▄  █  
      //  
      // var query = {}
      //
      // query['transaction_index'] = encodeURIComponent(this.transaction_index)
      //
      // if(this.code_tag.selected_tag[0] && this.code_tag.selected_tag[0]){
      //   // have not tested this yet. unsure if working
      //   query['code_tag'] = encodeURIComponent(JSON.stringify(this.code_tag))
      // }
      // 
      // updates the selection code
      // if(this.selected_code != null){
      //   query['selected_code'] = encodeURIComponent(JSON.stringify(this.selected_code))
      // }
      // updates the short_description
      // query['description_short'] = encodeURIComponent(this.short_description)
      //
      // updates movement
      // query['current_movement_type'] = encodeURIComponent(this.current_movement_type)
      

      this.$router.push({query: {
        transaction_index: encodeURIComponent(this.transaction_index),
        // code_tag: encodeURIComponent(JSON.stringify(this.code_tag)),
        // selected_code: encodeURIComponent(JSON.stringify(this.selected_code)),
        // description_short: encodeURIComponent(this.short_description),
        // current_movement_type: encodeURIComponent(this.current_movement_type),
        current_account: encodeURIComponent(this.current_account),
        } //query
      });
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

const routes = [
  { path: '', component: { template: 'Home' }, props: (route) => ({ transaction_index: route.query.transaction_index }) },
]
const router = VueRouter.createRouter({
  mode: 'history', // add 'history' mode
  history: VueRouter.createWebHashHistory(),
  routes, // short for `routes: routes`
})
app.use(router)

app.mount('#app');

// Print to console
console.log("This is a message"); // Print a string
console.log(app); // Print a data property from vue instance
console.log(app.result_1, app.result_2, app.result_3); // Print multiple data properties from vue instance
console.log(app.$route)
console.log('starting mounted')



function clean_price(price) {
  return parseFloat(String(price).replace(/[^0-9.]+/g,""));
}