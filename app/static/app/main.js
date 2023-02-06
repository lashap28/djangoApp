$(document).ready(function(){

    const video = document.getElementById("img_f");
    var csrf = $("input[name=csrfmiddlewaretoken]").val();

    $('#selfie_btn').click(function(){
        let canvas = document.createElement("canvas");
        canvas.width = 640;
        canvas.height = 480;
        canvas.getContext('2d').drawImage(video, 0, 0);
        let canvasDataUrl = canvas.toDataURL('image/png');

        $.ajax({
           url: '',
           type: 'POST',
            data:{
                imgTagHtml: canvasDataUrl,
                csrfmiddlewaretoken:csrf
            },
            xhrFields: {
                withCredentials: true
            },
            success: function(response){
                $("#selfie_btn").attr('disabled',true)
                $("#doc_btn").attr('disabled',false);
            }
        });
    });

 $('#doc_btn').click(function(){
        let canvas = document.createElement("canvas");
        canvas.width = 640;
        canvas.height = 480;
        canvas.getContext('2d').drawImage(video, 0, 0);
        let canvasDataUrl = canvas.toDataURL('image/png');

        $.ajax({
           url: '',
           type: 'POST',
            data:{
                docTagHtml: canvasDataUrl,
                csrfmiddlewaretoken:csrf
            },
            xhrFields: {
                withCredentials: true
            },
            success: function(response){
                $("#doc_btn").attr('disabled',true);
                $("#next_btn").attr('disabled',false);
            }
        });
    });

 $('#next_btn').click(function(){
        $.ajax({
           url: "json_response",
           type: 'get',
            data:{
                calculate: '1',
            },
            success: function(response){
            }
        });
    });


    
});