$(document).ready(function(){
    function update(){
        if ($('#refresh').hasClass('r_enabled')){
            $.get("update", {}, function(data){
                $('#background').html(data); 
            });
        }
    }

    setInterval(update, 10000);

    //Refresh button
    $('#refresh').live("click", function(){
        $(this).toggleClass('r_enabled');
    });


    //Torrent search
    $('#searchInput input')
      .focus(function(){
        $(this).val('');
    }).blur(function(){
        if(($.trim( $(this).val() ) == '')){
            $(this).val('Enter search here...');
        }
    }).keypress(function(key){
        if(key.which == 13){
            key.preventDefault();
            var searchText = $(this).val();
            $.ajax({url : 'torrentsearch',
                    data : {search : searchText},
                    success : function(data){
                        $('#searchResults').html(data).fadeIn(300);
                    },
                    error: function(data){
                        $('#searchResults').html('Shit, sometimes search breaks for a few minutes.').fadeIn(500);       
                    }
            });
            $('#searchResults').fadeOut(500);
        }
    });

    // Click Pirate Bay Search result -> Highlight -> Add
    $('div.torrent').live("click", function () {
        var link = $(this).attr("id");
        var name = $(this).find(".name").html();
        var $this = $(this);

        if ($(this).hasClass('selected')) {
            if (confirm("Download " + name + "?")) {
                $.ajax({
                    url : "download_any",
                    data : { link: link, name: name },
                    success : function (data) {
                        $this.remove();
                    },
                    error : function(xhr, options, error){
                        $this.animate({width : '500px'}, 300);
                    }
                });
                $this.animate({width : '0px'}, 500);
            }
        }
        else {
            $('.torrent').removeClass('selected');
            $(this).addClass('selected');
        }
    });

});
