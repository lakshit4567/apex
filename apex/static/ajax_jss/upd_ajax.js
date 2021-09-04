
    $.ajax({
        method: 'GET',
        url : "upd_save",
        success: function(response){
            // console.log(response.data)
            const es_data = response.data
            es_data.map(item =>{
                $('#upd_id').append(`<option value="${item.id}">
                    ${item.id}
                    </option>`);
                })
            }
        })
    var a = document.getElementById('upd_id');
    const type = document.getElementById('upd_type');
    a.addEventListener('change', function() {
        
        var selected_id = this.value;
        type.textContent = "Select"
        
        console.log(selected_id);
        $.ajax({
            method: 'GET',
            url : `get_es_type/${selected_id}/`,
            success : function(response){
                var es_data = response.data
                // console.log(response.data);
                es_data.map(item =>{
                    $('#upd_type').append(`<option value="${item.Type}">
                                       ${item.Type}
                                  </option>`);
                    $('#upd_size').val(item.ES_Size);
                })
            }

        })
    }, false);



    $("#btnsave-upd").click("#post-form-upd",function(){
    // $("#btnsave").click(function(){
        output_uf = "";
        let id = $("#upd_id").val();
        let date = $("#upd_date").val();
        let type = $("#upd_type").val();
        let quantity = $("#upd_quantity").val();
        let size = $("#upd_size").val();
        let csr = $("input[name=csrfmiddlewaretoken").val();
        // console.log(uf_date)
        // console.log(sale_weight)
        // console.log(sale_quantity)
        upd_data = {
            upd_date : date,
            upd_type : type,
            upd_quantity:quantity,
            upd_size : size,
            upd_id : id,
            csrfmiddlewaretoken: csr,
        };
        if(date == ''){
            // console.log('input')
            $("#toast5_id").html(alert_msg('Error!','Please input field', 'toast-div-danger'))
        }else if(id == ''){
            $("#toast5_id").html(alert_msg('Error!','Please input field', 'toast-div-danger'))
        }
        else if(type == ''){
            $("#toast5_id").html(alert_msg('Error!','Please input field', 'toast-div-danger'))
        }
        
        else if(quantity == '') {
            $("#toast5_id").html(alert_msg('Error!','Please input field', 'toast-div-danger'))
        }else if(size == ''){
            $("#toast5_id").html(alert_msg('Error!','Please input field', 'toast-div-danger'))
        }
        else{
        $.ajax({
            url : "upd_save", //
            method: "POST",
            data: upd_data,
            dataType: "json",
            success: function (data) {
                x = data.upd_data;
                if (data.status == 1){
                    $("#toast5_id").html(alert_msg('Error!','Not enough Quantity in stock', 'toast-div-danger'))
                };
                if (data.status == "Save") {
                    for (i = 0; i < x.length; i++) {
                        output_uf +=
                            "<tr><td>" +
                            x[i].id +
                            "</td><td>" +
                            x[i].register_id +
                            "</td><td>" +
                            x[i].EPD_Date +
                            "</td><td>" +
                            x[i].EPD_UID_id  +
                            "</td><td>" +
                            x[i].EPD_Type +
                            "</td><td>" +
                            x[i].EPD_Quantity +
                            "</td><td>" +
                            x[i].EPD_Size +
                            "</td>" +
                            "<td class='text-center d-flex justify-content-around'><a class='btn btn-danger btn-sm btn-del-upd' title='delet' id='del' data-sid = "+
                            x[i].id +"><i class='fa fa-trash'></i> </a></td></tr>";
                        // console.log(output_uf)
                        $("#toast5_id").html(alert_msg('Success!','Entry Added', 'toast-div-success'))
                    };
                    $("#tbody-upd").html(output_uf);
                    $("#post-form-upd")[0].reset();
                   
                }else if(data.status==0) {
                    $("#toast5_id").html(alert_msg('Error!','Unable to save data', 'toast-div-danger'))
                }
                
            },

        })
    }
    })
    
    $('#tbody-upd').on("click",".btn-del-upd",function (){
        // console.log('button selected')
        let id = $(this).attr("data-sid");
        let csr = $("input[name=csrfmiddlewaretoken").val();
        console.log(id)
        mydata = { sid: id, csrfmiddlewaretoken: csr };
        mythis = this;
        $.ajax({
            url : "upd_delete",
            method: "POST",
            data: mydata,
            success : function(data) {
                if (data.status==1){
                    $("#toast5_id").html(alert_msg('Success!','Entry Deleted', 'toast-div-danger'))
                    $(mythis).closest("tr").fadeOut();
                }
            }
        })
    })


    // toast function
    const alert3_msg = (head,msg, boot_class) => {
        return `
        <div class="toast-div" data-delay="1000">
            <div class="toast-header ${boot_class}">
            <strong class="mr-auto text-dark">${head}</strong>
            <button class=" btn btn-lg pr-lg-2 m-0 py-0 float-right" onclick='this.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode); return false;'>
                                &times;</button>
            </div>
            <div class="toast-body ${boot_class} px-lg-5 text-center">
                ${msg}
                </div>
        </div>
        `

    }


    $("#btnsave-es").click("#post-form-es",function(){
    // $("#btnsave").click(function(){
        output_uf = "";
        let date = $("#es_date").val();
        let type = $("#es_type").val();
        let quantity = $("#es_quantity").val();
        let size = $("#es_size").val();
        let csr = $("input[name=csrfmiddlewaretoken").val();
        // console.log(uf_date)
        // console.log(sale_weight)
        // console.log(sale_quantity)
        es_data = {
            es_date : date,
            es_type : type,
            es_quantity:quantity,
            es_size : size,
            csrfmiddlewaretoken: csr,
        };
        if(date == ''){
            // console.log('input')
            $("#toast3_id").html(alert3_msg('Error!','Please input field', 'toast-div-danger'))
        }else if(type == ''){
            $("#toast3_id").html(alert3_msg('Error!','Please input field', 'toast-div-danger'))
        }else if(quantity == '') {
            $("#toast3_id").html(alert3_msg('Error!','Please input field', 'toast-div-danger'))
        }else if(size == ''){
            $("#toast3_id").html(alert3_msg('Error!','Please input field', 'toast-div-danger'))
        }
        else{
        $.ajax({
            url : "es_save", //
            method: "POST",
            data: es_data,
            dataType: "json",
            success: function (data) {
                x = data.es_data;
                if (data.status == "Save") {
                    for (i = 0; i < x.length; i++) {
                        output_uf +=
                            "<tr><td>" +
                            x[i].id +
                            "</td><td>" +
                            x[i].register_id +
                            "</td><td>" +
                            x[i].ES_Date  +
                            "</td><td>" +
                            x[i].Type +
                            "</td><td>" +
                            x[i].ES_Quantity +
                            "</td><td>" +
                            x[i].ES_Size +
                            "</td>" +
                            "<td class='text-center d-flex justify-content-around'><a class='btn btn-danger btn-sm btn-del-es' title='delet' id='del' data-sid = "+
                          x[i].id +"><i class='fa fa-trash'></i> </a></td></tr>";
                        // console.log(output_uf)
                        $("#toast3_id").html(alert3_msg('Success!','Entry Added', 'toast-div-success'))
                    };
                    $("#es_date").val("");
                    $("#es_type").val("");
                    $("#es_quantity").val("");
                    $("#es_size").val("");
                    $("#tbody-es").html(output_uf);
                    // $("#post-form-es")[0].reset();
                    // // $(document).ready(function () {
                    //         setTimeout(function () {
                    //             // alert('Reloading Page');
                    //             location.reload(true);
                    //         }, 1000);
                            // });
                   
                }else if(data.status==0) {
                    $("#toast3_id").html(alert3_msg('Error!','Unable to save data', 'toast-div-danger'))
                }
                
            },

        })
    }
    })
    
    $('#tbody-es').on("click",".btn-del-es",function (){
        // console.log('button selected')
        let id = $(this).attr("data-sid");
        let csr = $("input[name=csrfmiddlewaretoken").val();
        console.log(id)
        mydata = { sid: id, csrfmiddlewaretoken: csr };
        mythis = this;
        $.ajax({
            url : "es_delete",
            method: "POST",
            data: mydata,
            success : function(data) {
                if (data.status==1){
                    $("#toast3_id").html(alert3_msg('Success!','Entry Deleted', 'toast-div-danger'))
                    $(mythis).closest("tr").fadeOut();
                }
            }
        })
    })

