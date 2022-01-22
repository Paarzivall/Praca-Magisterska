 $(document).ready(function(){
        $('.block_of_scratch_code').mouseover(function(event){
            var id_of_block = this.id.substring(this.id.indexOf('_') + 1);
            var id_of_python_block = 'python_' + id_of_block.toString();
            var elements = document.getElementsByClassName(id_of_python_block);
            change_style(elements, 'bold', '1.5rem');
            
        });

         $('.block_of_scratch_code').mouseout(function(event){
            var id_of_block = this.id.substring(this.id.indexOf('_') + 1);
            var id_of_python_block = 'python_' + id_of_block.toString();
            var elements = document.getElementsByClassName(id_of_python_block);
            change_style(elements, 'normal', '1rem');
        });

        $('.block_of_python_code').mouseover(function(event){
            var id_of_block = this.id.substring(this.id.indexOf('_') + 1);
            var id_of_scratch_block = 'scratch_' + id_of_block.toString();
            var elements = document.getElementsByClassName(id_of_scratch_block);
            change_style(elements, 'bold', '1.5rem');
        });

            $('.block_of_python_code').mouseout(function(event){
            var id_of_block = this.id.substring(this.id.indexOf('_') + 1);
            var id_of_scratch_block = 'scratch_' + id_of_block.toString();
            var elements = document.getElementsByClassName(id_of_scratch_block);
            change_style(elements, 'normal', '1rem');
        });

        function change_style(elements, font_weight, size){
             for(var element = 0; element < elements.length; element ++){
                 $(elements[element]).css('font-weight', font_weight);
                 $(elements[element]).css('font-size', size);
             }
        }
    });