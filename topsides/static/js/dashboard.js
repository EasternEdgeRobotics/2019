var CurrentPage = null;

$(document).ready(function(){

    runPythonGET("dashboard/getmenujson", null, function(data){
        $.each(data.menus, function(index, menu){
            $.get(menu.icon_url, function(data){
                var svg = $(data).find("svg").attr("class", "nav-svg col-5 icon");
                $("<div data-page='" + menu.file_name + "' class='btn-nav row'><svg viewbox='0 0 25 25' class='nav-svg col-5 icon'>" + svg.html() + "<svg><div class='text col-5 justify-content-center align-self-center'><p>" + menu.name + "</p></div></div>").click(function(){navButtonClick($(this))}).appendTo("#nav");
            });
        });
    });
});

function navButtonClick(btn){
    var page = btn.attr("data-page");
    if(CurrentPage != page){
        $(".btn-nav").toggleClass("active", false);
        btn.toggleClass("active", true);
        clearPage();
        loadPage(page);
        CurrentPage = page;
    }
}

function loadPage(pageURL){
    runPythonGET("dashboard/page?name=" + pageURL, null, function(pageData){
        $("#pageBody").html(pageData.responseText);
    });
}

function clearPage(){
    $("#pageBody").empty();
}