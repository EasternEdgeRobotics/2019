/**
 * Dashboardjs
 * 
 * Created by Andrew Troake
 */




/**
 * 
 *  Dashboard instance. Set values from the pages to make them interactive
 */
var $dash = {
    animation: {
        delay: 100,
        time: 3000,
        onPageClose: null,
        onPageOpen: null,
    },
    page: {
        file_name: null
    }
}

$(document).ready(function(){

    runPythonGET("dashboard/getmenujson", null, function(data){
        $.each(data.menus, function(index, menu){
            $.get(menu.icon_url, function(data){
                var svg = $(data).find("svg").attr("class", "nav-svg col-5 icon");
                var button = $("<div data-page='" + menu.file_name + "' class='btn-nav row'><div class='background'></div><svg viewbox='0 0 25 25' class='nav-svg col-5 icon'>" + svg.html() + "<svg><div class='text col-5 justify-content-center align-self-center'><p>" + menu.name + "</p></div></div>").click(function(){navButtonClick($(this))}).appendTo("#nav");
                if(index == 0){
                    navButtonClick(button);
                }
            });
        });
    });
});

function navButtonClick(btn){
    var page = btn.attr("data-page");
    if($dash.page.file_name != page){
        $(".btn-nav").toggleClass("active", false);
        btn.toggleClass("active", true);
        clearPage();
        loadPage(page);
    }
}

function loadPage(pageURL){
    clearPage();

    runPythonGET("dashboard/page?name=" + pageURL, null, function(pageData){
        $dash.page.file_name = pageURL
        $("#pageBody").html(pageData.responseText);
        //run on page open event
        runDashboardAnimation($dash.animation.onPageOpen, null);
    });
}

function clearPage(){
    //run the on page close event
    runDashboardAnimation($dash.animation.onPageClose, null);

    setTimeout(function(){
        $dash.page.file_name = null
        $("#pageBody").empty();
    }, $dash.animation.onPageClose != null ? $dash.animation.onPageClose.length: 0);
    
}

function runDashboardAnimation(animation, afterFunction){
    if(animation != null){
        if(animation instanceof Function){
            setTimeout(function(){animation();}, $dash.animation.delay);
            setTimeout(function(){if(afterFunction instanceof Function)afterFunction()}, $dash.animation.delay+$dash.animation.time);
        }
    }
}