/**
 * Dashboardjs
 * 
 * Created by Andrew Troake
 */


$(document).ready(function(){
    runPythonGET("dashboard/getmenujson", null, function(data){
        $.each(data.menus, function(index, menu){
            //loading all dashboard nav buttons
            $.get(menu.icon_url, function(data){
                var svg = $(data).find("svg").attr("class", "nav-svg col-5 icon");
                var button = $("<div data-page='" + menu.name + "' class='btn-nav row' style='order: " + index + "'><div class='background'></div><svg viewbox='0 0 25 25' class='nav-svg col-lg-5 col-md-12 col-5 icon'>" + svg.html() + "<svg><div class='text col-5 justify-content-center align-self-center'><p>" + menu.name + "</p></div></div>").click(function(){navButtonClick($(this))}).appendTo("#nav");
                if(index == 0 && getQueryParameter("page") == null){
                    navButtonClick(button);
                }else if(decodeURIComponent(getQueryParameter("page")) == menu.file_name){
                    button.toggleClass("active", true);
                }
            });
        });
        if(getQueryParameter("page") != null){
            $dash.loadPage(getQueryParameter("page"));
        }
    });

    runPythonGET("auth/check", null, function(data){
        $.get("static/res/icons/baseline-dns-24px.svg", function(data1){
            var svg = $(data1).find("svg").attr("class", "nav-svg col-5 icon");
            if(data.status != 200){
                var button = $("<div data-page='login' class='btn-nav row auth login' style='order:9999'><div class='background'></div><svg viewbox='0 0 25 25' class='nav-svg col-lg-5 col-md-12 col-5 icon'>" + svg.html() + "<svg><div class='text col-5 justify-content-center align-self-center'><p>Login</p></div></div>").click(function(){navButtonClick($(this))}).appendTo("#nav");
            }else{
                var button = $("<div data-page='' class='btn-nav row auth logout' style='order:9999'><div class='background'></div><svg viewbox='0 0 25 25' class='nav-svg col-lg-5 col-md-12 col-5 icon'>" + svg.html() + "<svg><div class='text col-5 justify-content-center align-self-center'><p>Logout</p></div></div>").click(function(){runPythonGET("/auth/logout", null, function(){window.location = window.location;})}).appendTo("#nav");
            }
        });
    });

    //init notification handler
    new NotificationHandler("notification");
});

function navButtonClick(btn){
    var page = btn.attr("data-page");
    if($dash.currentPage != page){
        $(".btn-nav").toggleClass("active", false);
        btn.toggleClass("active", true);
        $dash.loadPage(page);
    }
}

class dashboard{
    constructor(){
        this._animationdelay = 100;
        this._animationtime = 3000;
        this._onpageopen = function(){};
        //this._onpageopenafter = function(){};
        this._onpageclose = function(){};
        //this._onpagecloseafter = function(){};
        this._filename = "";
        this._bodyContainer = "#pageBody";
    }

    //Animation Delay
    
    set animationDelay(delay){
        this._animationdelay = delay;
    }

    get animationDelay(){
        return this._animationdelay;
    }

    //Page Body Selector
    set bodyContainer(s){
        this._bodyContainer = s;
    }

    //Animation Time

    set animationTime(t){
        this._animationtime = t;
    }

    get animationTime(){
        return this.animationTime;
    }

    //On Page Open

    pageLoad(f){
        this._onpageopen = f;
        this._onpageopenafter = function(){};
    }

    /*set pageLoad(f, a){
        this._onpageopen = f;
        this._onpageopenafter = a;
    }*/

    /*get pageLoad(){
        this._onpageopen();
    }*/

    //On Page Close

    pageClose(f){
        this._onpageclose = f;
        this._onpagecloseafter = null;
    }

    /*set pageClose(f, a){
        this._onpageclose = f;
        this._onpagecloseafter = a;
    }*/

    //pageURL
    get currentPage(){
        return this._filename;
    }




    navigate(url){
        if(this._onpageclose instanceof Function)
            this._onpageclose();
        this._clearPage();
        runPythonGET(url, null, function(pageData){
            $dash.filename = url;
            $($dash._bodyContainer).html(pageData.responseText);
            //run on page open event
            $dash._runDashboardAnimation($dash._onpageopen, null);
        });
    }


    loadPage(pageURL){
        if(this._onpageclose instanceof Function)
            this._onpageclose();
        this._clearPage();
        $("#loadingSpinner").toggleClass("hide", false);
        runPythonGET("dashboard/page/" + pageURL, null, function(pageData){
            $dash.filename = pageURL;
            setQueryParameter("page", pageURL);
            $($dash._bodyContainer).html(pageData.responseText);
            $("#loadingSpinner").toggleClass("hide", true);
            //run on page open event
            $dash._runDashboardAnimation($dash._onpageopen, null);
        });
    }

    _clearPage(){
        this._file_name = null
        $(this._bodyContainer).empty();
        this._onpageclose = null;
        this._onpageopen = null;
    }

    closePage(){
        this._runDashboardAnimation(this._onpageclose, null);
        
        setTimeout(function(){
            $dash._clearPage();
        }, $dash._onpageclose != null ? $dash._animationtime : 0);
    }

    _runDashboardAnimation(animation, afterFunction){
        if(animation != null){
            if(animation instanceof Function){
                setTimeout(function(){animation();}, this._animationdelay);
                setTimeout(function(){if(afterFunction instanceof Function)afterFunction()}, this._animationdelay+this._animationtime);
            }
        }
    }

}

/**
 * 
 *  Dashboard instance. Set values from the pages to make them interactive
 */

var $dash = new dashboard();