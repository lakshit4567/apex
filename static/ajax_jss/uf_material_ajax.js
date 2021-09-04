
    $("#btnsaveuf").click("#uf-form",function(){
    // $("#btnsave").click(function(){
        output_uf = "";
        let uf_date = $("#uf_date").val();
        let uf_weight = $("#uf_weight").val();
        let uf_quantity = $("#uf_quantity").val();
        let fm_id = $("#fm_id").val();
        let csr = $("input[name=csrfmiddlewaretoken").val();
        console.log(uf_date)
        console.log(uf_weight)
        console.log(uf_quantity)
        uf_data = {
            uf_date : uf_date,
            uf_weight: uf_weight,
            uf_quantity: uf_quantity,
            f_id: fm_id,
            csrfmiddlewaretoken: csr,
        };
        if(uf_date == ''){
            $("#toast1_id").html(alert_msg('Error!','Please input field', 'toast-div-danger'))
        }else if(uf_weight == ''){
            $("#toast1_id").html(alert_msg('Error!','Please input field', 'toast-div-danger'))
        }else if(uf_quantity == '') {
            $("#toast1_id").html(alert_msg('Error!','Please input field', 'toast-div-danger'))
        }    
        else{
        $.ajax({
            url : "uf_save",
            method: "POST",
            data: uf_data,
            dataType: "json",
            success: function (data) {
                x = data.uf_data;
                if (data.status == "Save") {
                    for (i = 0; i < x.length; i++) {
                        output_uf +=
                            "<tr><td>" +
                            x[i].id +
                            "</td><td>" +
                            x[i].register_id +
                            "</td><td>" +
                            x[i].UFM_date +
                            "</td><td>" +
                            x[i].FMid_id  +
                            "</td><td>" +
                            x[i].UFM_Quantity +
                            "</td><td>" +
                            x[i].UFM_Weight +
                            "</td>" +
                            "<td class='text-center d-flex justify-content-around'><a class='btn btn-danger btn-sm btn-del-ufm' title='delet' id='del' data-sid = "+
                            x[i].id +"><i class='fa fa-trash'></i> </a></td></tr>";
                        console.log(output_uf)
                        $("#toast1_id").html(alert_msg('Success!','Entry Added Successfully', 'toast'))
                    };
                    $("#tbodyufm").html(output_uf);
                    // $("form")[0].reset();
                    if (data.status==0){
                        $("#toast1_id").html(alert_msg('Error!','Unable to Save Data', 'toast-div-danger'))
                        
                        // $("#tbodyufm")[0].reset();
                    }
                }
                
            },

        })
    }
    })
    $('#tbodyufm').on("click",'.btn-del-ufm',function (){
        // console.log('button selected')
        let id = $(this).attr("data-sid");
        let csr = $("input[name=csrfmiddlewaretoken").val();
        console.log(id)
        mydata = { sid: id, csrfmiddlewaretoken: csr };
        mythis = this;
        $.ajax({
            url : "ufm_delete",
            method: "POST",
            data: mydata,
            success : function(data) {
                if (data.status==1){
                    $("#toast1_id").html(alert_msg('Success!','Entry Deleted', 'toast-div-danger'))
                    $(mythis).closest("tr").fadeOut();
                }
            }
        })
    })


