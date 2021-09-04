
    $.ajax({
        method: 'GET',
        url : "usale_save",
        success: function(response){
            // console.log(response.data)
            const us_m_t = response.data
            us_m_t.map(item =>{
                $('#usfm_id').append(`<option value="${item.id}">
                                       ${item.id}
                                  </option>`);
            })
        }
    })
    var ua_s_t = document.getElementById('usfm_id');
    const us_m_grad = document.getElementById('us_m_type');
    ua_s_t.addEventListener('change', function() {
        // console.log('jdsjd')
        var selected_id = this.value;
        us_m_grad.textContent = "Select"
        // console.log(selected_id);
        $.ajax({
            method: 'GET',
            url : `get_us_type/${selected_id}/`,
            success : function(response){
                var us_m_data = response.data
                // console.log(response.data);
                us_m_data.map(item =>{
                    $('#us_m_type').val(item.UFM_type);
                })
            }

        })
    }, false);















    $("#btnsave-usale").click("#usale-form",function(){
    // $("#btnsave").click(function(){
        output_uf = "";
        let ufmsale_id= $("#usfm_id").val();
        let sale_date = $("#usale_date").val();
        let usale_sold = $("#usale_sold").val()
        let usale_type = $("#us_m_type").val();
        let sale_quantity = $("#usale_quantity").val();
        let sale_weight = $("#usale_weight").val();
        let csr = $("input[name=csrfmiddlewaretoken").val();
        // console.log(uf_date)
        // console.log(sale_weight)
        // console.log(sale_quantity)
        sale_data = {
            us_m_type : usale_type,
            ufmsales_id : ufmsale_id,
            sales_date : sale_date,
            sales_quantity: sale_quantity,
            sales_weight: sale_weight,
            usale_sold: usale_sold,
            csrfmiddlewaretoken: csr,
        };
        if(ufmsale_id == ''){
            // console.log('input')
            $("#toast4_id").html(alert_msg('Error!','Please input field', 'toast-div-danger'))
        }else if(usale_sold == ''){
            $("#toast4_id").html(alert_msg('Error!','Please input Sold To', 'toast-div-danger'))
        }
        else if(sale_date == ''){
            $("#toast4_id").html(alert_msg('Error!','Please input field', 'toast-div-danger'))
        }else if(sale_quantity == '') {
            $("#toast4_id").html(alert_msg('Error!','Please input field', 'toast-div-danger'))
        }else if(sale_weight == '') {
            $("#toast4_id").html(alert_msg('Error!','Please input field', 'toast-div-danger'))
        }    
        else{
        $.ajax({
            url : "usale_save", //
            method: "POST",
            data: sale_data,
            dataType: "json",
            success: function (data) {
                x = data.sale_data;
                if (data.status == 1) {
            $("#toast4_id").html(alert_msg('Error!','Not enough Weight in stock', 'toast-div-danger'))
                };
                if (data.status == 2) {
            $("#toast4_id").html(alert_msg('Error!','Not enough Quantity in stock', 'toast-div-danger'))
                }
                if (data.status == "Save") {
                    for (i = 0; i < x.length; i++) {
                        output_uf +=
                            "<tr><td>" +
                            x[i].id +
                            "</td><td>" +
                            x[i].register_id +
                            "</td><td>" +
                            x[i].To +
                            "</td><td>" +
                            x[i].UFcoilID_id  +
                            "</td><td>" +
                            x[i].Sale_date +
                            "</td><td>" +
                            x[i].Sale_Type +
                            "</td><td>" +
                            x[i].Sale_Quantity +
                            "</td><td>" +
                            x[i].Sale_Weight +
                            "</td>" +
                            "<td class='text-center d-flex justify-content-around'><a class='btn btn-danger btn-sm btn-del-usale' title='delet' id='del' data-sid = "+
                            x[i].id +"><i class='fa fa-trash'></i> </a></td></tr>";
                        // console.log(output_uf)
                        $("#toast4_id").html(alert_msg('Success!','Entry Added', 'toast-div-success'))
                    };
                    // $("#usfm_id").val("");
                    // $("#usale_date").val("");
                    $("#usale_sold").val("");
                    $("#us_m_type").val("");
                    $("#usale_quantity").val("");
                    $("#usale_weight").val("");
                    $("#tbody-usale").html(output_uf);
                    // $("#usale-form")[0].reset();
                   
                }if(data.status==0) {
                    $("#toast4_id").html(alert_msg('Error!','Unable to save data', 'toast-div-danger'))
                }
                
            },

        })
    }
    })
    
    $('#tbody-usale').on("click",".btn-del-usale",function (){
        // console.log('button selected')
        let id = $(this).attr("data-sid");
        let csr = $("input[name=csrfmiddlewaretoken").val();
        console.log(id)
        mydata = { sid: id, csrfmiddlewaretoken: csr };
        mythis = this;
        $.ajax({
            url : "usale_delete",
            method: "POST",
            data: mydata,
            success : function(data) {
                if (data.status==1){
                    $("#toast4_id").html(alert_msg('Success!','Entry deleted', 'toast-div-danger'))
                    $(mythis).closest("tr").fadeOut();
                }
            }
        })
    })

