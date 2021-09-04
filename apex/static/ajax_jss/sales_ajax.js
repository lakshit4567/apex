
    $.ajax({
        method: 'GET',
        url : 'sale_save',
        success: function(response){
            // console.log(response.data)
            const s_m_t = response.data
            s_m_t.map(item =>{
                $('#sfm_id').append(`<option value="${item.id}">
                                       ${item.id}
                                  </option>`);
            })
        }
    })
    var a_s_t = document.getElementById('sfm_id');
    const s_m_grad = document.getElementById('s_m_type');
    a_s_t.addEventListener('change', function() {
        // console.log('jdsjd')
        var selected_id = this.value;
        s_m_grad.textContent = "Select"
        console.log(selected_id);
        $.ajax({
            method: 'GET',
            url : `get_s_type/${selected_id}/`,
            success : function(response){
                var s_m_data = response.data
                // console.log(response.data);
                s_m_data.map(item =>{
                    $('#s_m_type').val(item.materialType);
                })
            }

        })
    }, false);











    $("#btnsave-sale").click("#sale-form",function(){
    // $("#btnsave").click(function(){
        output_uf = "";
        let fmsale_id= $("#sfm_id").val();
        let sale_date = $("#sale_date").val();
        let s_m = $("#s_m_type").val();
        let sale_quantity = $("#sale_quantity").val();
        let sale_weight = $("#sale_weight").val();
        let sale_sold = $("#sale_sold").val();
        let csr = $("input[name=csrfmiddlewaretoken").val();
        // console.log(uf_date)
        // console.log(sale_weight)
        // console.log(sale_quantity)
        sale_data = {
            fmsales_id : fmsale_id,
            sale_sold: sale_sold,
            s_m_type : s_m,
            sales_date : sale_date,
            sales_quantity: sale_quantity,
            sales_weight: sale_weight,
            csrfmiddlewaretoken: csr,
        };
        if(fmsale_id == ''){
            // console.log('input')
            $("#toast2_id").html(alert_msg('Error!','Please input field', 'toast-div-danger'))
        } else if(sale_sold == ''){
            // $("#sale-form")[0].reset();
            $("#toast2_id").html(alert_msg('Error!','Please input Sold To', 'toast-div-danger'))
        }
        else if(sale_date == ''){
            // $("#sale-form")[0].reset();
            $("#toast2_id").html(alert_msg('Error!','Please input field', 'toast-div-danger'))
        }else if(sale_quantity == '') {
            $("#toast2_id").html(alert_msg('Error!','Please input field', 'toast-div-danger'))
        }else if(sale_weight == '') {
            $("#toast2_id").html(alert_msg('Error!','Please input field', 'toast-div-danger'))
        }    
        else{
        $.ajax({
            url : "sale_save",
            method: "POST",
            data: sale_data,
            dataType: "json",
            success: function (data) {
                x = data.sale_data;
                if (data.status == 1) {
            $("#toast2_id").html(alert_msg('Error!','Not enough Weight in Stock', 'toast-div-danger'))
                };
                if (data.status == 2) {
            $("#toast2_id").html(alert_msg('Error!','Not enough Quantity in Stock', 'toast-div-danger'))
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
                            x[i].FMcoilUID_id  +
                            "</td><td>" +
                            x[i].Sale_date +
                            "</td><td>" +
                             x[i].Sale_Type +   
                            "</td><td>" +
                            x[i].Sale_Quantity +
                            "</td><td>" +
                            x[i].Sale_Weight +
                            "</td>" +
                            "<td class='text-center d-flex justify-content-around'><a class='btn btn-danger btn-sm btn-del-salefm' title='delet' id='del' data-sid = "+
                            x[i].id +"><i class='fa fa-trash'></i> </a></td></tr>";
                        // console.log(output_uf)
                        $("#toast2_id").html(alert_msg('Success!','Entry Added Successfully', 'toast-div-success'))
                    };
                    // console.log("###########")
                    // $("#sale-form")[0].reset();
                    // $("#sfm_id").val("");
                    // $("#sale_date").val("");
                    $("#s_m_type").val("");
                    $("#sale_quantity").val("");
                    $("#sale_weight").val("");
                    $("#sale_sold").val("");
                    $("#tbody-sale").html(output_uf);
                    // console.log("###########");
                }if(data.status==0) {
                    $("#toast2_id").html(alert_msg('Error!','Unable to save data', 'toast-div-danger'))
                }
                
            },

        })
    }
    })
    
    $('#tbody-sale').on("click",".btn-del-salefm",function (){
        // console.log('button selected')
        let id = $(this).attr("data-sid");
        let csr = $("input[name=csrfmiddlewaretoken").val();
        console.log(id)
        mydata = { sid: id, csrfmiddlewaretoken: csr };
        mythis = this;
        $.ajax({
            url : "sale_delete",
            method: "POST",
            data: mydata,
            success : function(data) {
                if (data.status==1){
                    $("#toast2_id").html(alert_msg('Success!','Entry Deleted', 'toast-div-danger'))
                    $(mythis).closest("tr").fadeOut();
                }
            }
        })
    })

