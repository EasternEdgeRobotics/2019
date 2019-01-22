/**
 * Dashboardjs
 * 
 * Created by Andrew Troake
 */


$(document).ready(function(){
    runPythonGET("dashboard/getmenujson", null, function(data){
        $.each(data.menus, function(index, menu){
            $.get(menu.icon_url, function(data){
                var svg = $(data).find("svg").attr("class", "nav-svg col-5 icon");
                var button = $("<div data-page='" + menu.file_name + "' class='btn-nav row'><div class='background'></div><svg viewbox='0 0 25 25' class='nav-svg col-5 icon'>" + svg.html() + "<svg><div class='text col-5 justify-content-center align-self-center'><p>" + menu.name + "</p></div></div>").click(function(){navButtonClick($(this))}).appendTo("#nav");
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
        this._clearPage();
        runPythonGET(url, null, function(pageData){
            $dash.filename = url;
            $($dash._bodyContainer).html(pageData.responseText);
            //run on page open event
            $dash._runDashboardAnimation($dash._onpageopen, null);
        });
    }


    loadPage(pageURL){
        this._clearPage();

        runPythonGET("dashboard/page?name=" + pageURL, null, function(pageData){
            $dash.filename = pageURL;
            setQueryParameter("page", pageURL);
            $($dash._bodyContainer).html(pageData.responseText);
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