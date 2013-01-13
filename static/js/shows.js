$(document).ready(function(){
    var open = false;
    var spinner = $('div#results').html();
    $('div#results').html('');

    var selectedSearchItem = null;
    var selectedShow = null;

    var seasons = new Array();
    $('#dummy').remove();

    var tooltipContent = "";

    // Click plus sign -> open search area
    $('img#searchToggle').click(function(){
        if(open){
            $(this).attr('src', '/static/img/green_plus_add.png');
            $('div#search').animate({height: '0px'}, 500);
            open = false;
        }else{
            $(this).attr('src', '/static/img/green_minus_add.png');
            $('div#search').animate({height: '100px'}, 500);   
            open = true;
        }
    });

    // Press Enter -> Search
    $('input.add').keypress(function(e) {
        if(e.which == 13){
            $('div#results').html(spinner);    
            $.get("search", {searchtext : $('input.add').val()}, function(data){
                $('div#results').html(data);    
            });
        }
    });

    // Click search result -> Highlight -> Add
    $('div.item').live("click", function() {
        //Initialize selected show
        if(selectedSearchItem == null){
            selectedSearchItem = this;
            $(this).css({"background-color": "orange"});
        }
        //Add the show
        else if(selectedSearchItem == this){
            var id = $(this).attr("id");
            var name = $.trim($(this).text());

            if (confirm("Add " + name + "?")){
                if($('div#s'+id).length){
                    alert(name + " already exists.");
                }
                else{
                    $.get("add", {id : id}, function(data){
                        location.reload(true);    
                    });
                }
            }
        }
        //Change the selected show
        else{
            $(selectedSearchItem).css({"background-color": ""});
            $(this).css({"background-color": "orange"});
            selectedSearchItem = this;
        }
    });

    // Click Pirate Bay Search result -> Highlight -> Add
    $('div.torrent').live("click", function(){
        var link = $(this).attr("id");
        var id = $(this).parent().attr("id").substring(1);

        if($(this).hasClass('selected')){
            if (confirm("Download " + $(this).find('.name').html() +"?")){
                $.get("download", {id: id, link: link}, function(data){
                    location.reload(true);
                });
            }
        }
        else{
            $('.torrent').removeClass('selected');
            $(this).addClass('selected');
        }
    });
                  
    // Click show -> Open Panel -> Change Panel
    $('div.show').live("click", function() {
        var id = $(this).attr("id");
                       
        function load_seasons(type, id){
            $.get(type, {id : id, season : 0}, function(data){
                  $('div#ep_content').html(data);
                  
                  if(type == "recent")
                    return;
                  
                  $( "#radio" ).buttonset();
                             
                  //Edit Search Template -> update entry in database
                  $('#showSearch input').keydown(function(event){
                        if(event.keyCode == 13) {
                            $('#showSearch img').attr('src','/static/img/spinner.gif');
                            event.preventDefault();
                            $.get("setsearch", {id : id, search : $('#showSearch input').val()}, function(data){
                                setTimeout(function() {
                                    $('#showSearch img').attr('src','/static/img/save.png');
                                }, 300);
                            });
                        }
                        else{
                            $('#showSearch img').attr('src','/static/img/not_save.png');
                        }
                   });
                             
                   seasons = [];
                   var season = 1;
                   while ($('#season' + season).length > 0){
                    seasons[season] = $('#season' + season).html();
                     $('#season' + season).remove();
                     season++;
                   }
                   var cur_season = $('.defaultSeason').attr('id').substring(5);
                   $('#episodes').html(seasons[cur_season]);
            });
        }

        //Open Panel and populate contents
        if(selectedShow == null){
            selectedShow = this;
            $(this).css({"background-color": "orange"});

            $('div#episodes_panel').animate({width: '758px'}, 100);
            
            var type = "seasons";
            if (id == "recent")
                type = "recent";
                       
            load_seasons(type, id.substring(1));
            
        }
        //TODO - Nothing?
        else if(selectedShow == this){
        }
        //TODO - Reload content of show panel
        else{
            $(selectedShow).css({"background-color": ""});
            $(this).css({"background-color": "orange"});
            selectedShow = this;

            var type = "seasons";
            if (id == "recent")
                type = "recent";
                       
            load_seasons(type, id.substring(1));
        }
    });

    //Click checkbox -> toggle downloading the show
    $('.downloadToggle').click(function(event){
        var id = $(this).attr('id');
        $.get("downloadtoggle",{id : id}, function(data){
            $('#s' + id).toggleClass('download');
        });
        event.stopPropagation();
    });

    //Click season button -> change season
    $('.seasonButton').live("click", function(){
        var cur_season = $(this).attr("id").substring(5);
        $('#episodes').html(seasons[cur_season]);
    });

    //Click PirateBay logo -> run search
    $('.epDownload a').live("click", function(){
        $('.pbSearch').animate({height: '0px'}, 200);   
        $('.pbSearch').html('');   
        if($(this).hasClass('selected')){
            $(this).removeClass('selected');   
        }
        else{
            $('.epDownload a').removeClass('selected');   
            $(this).addClass('selected');
            var id = $(this).closest('div').attr('id');
            $('#p' + id).animate({height: '130px'}, 500);
            $.get("gettorrents", {id : id}, function(data){
                $('#p' + id).html(data);    
            });
            $('#p' + id).html(spinner);    
        }
    });

});
