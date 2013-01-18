$(document).ready(function(){
    function update(){
        if ($('#refresh').hasClass('r_enabled')){
            $.get("update", {}, function(data){
                $('#background').html(data); 
            });
        }
    }

    setInterval(update, 10000);

    $('#refresh').click(function(){
        $(this).toggleClass('r_enabled');
    });
});
