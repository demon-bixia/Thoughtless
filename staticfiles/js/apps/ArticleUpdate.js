$(function(){
    let first_input = $("#id_text_area_1");
    let input_counter = $("#input_counter");
    let paragraph_container = $("#paragraphs");
    let next_input_number = 1 + parseInt(input_counter.val());
    let ORIGINAL_COUNT = parseInt(input_counter.val());
    let counter = parseInt(input_counter.val());


    $("#add").on('click', function(){
        let id = "id_text_area_" + next_input_number;
        let name = "text_area_" + next_input_number;
        let placeholder = "paragraph";
        next_input_number += 1;
        paragraph_container.append($('<textarea></textarea>' )
            .attr({id:id, col:30, rows:5, placeholder:placeholder, name:name})
            .addClass("form-input")
        );
        counter += 1;
        input_counter.val(counter.toString())
    });

    $("#remove").on('click', function(){
        if (counter <= ORIGINAL_COUNT){
            return null;
        } else{
            let id = "id_text_area_" + counter;
            let element = $("#" + id);
            element.remove();
            counter -= 1;
            next_input_number -= 1;
            input_counter.val(counter.toString())
        }
    });
        $("#split").on('click', function(){
        let id = "id_text_area_" + next_input_number;
        let name = "text_area_split_" + next_input_number;
        let placeholder = "split paragraph";
        next_input_number += 1;
        paragraph_container.append($('<textarea></textarea>' )
            .attr({id:id, col:30, rows:5, placeholder:placeholder, name:name})
            .addClass("form-input")
        );
        counter += 1;
        input_counter.val(counter.toString())
    });
});