jQuery(document).ready(function($) {
    $(".bibentry").hide();
    $("div.bib_tex_show_hide").click(function() {
        var $this = $(this),
        target = $this.next(".bibentry"),
        showing = target.is(':visible');
        if(showing){ // hide
            target.hide();
            $this.html("[+]Show Bib");
        }
        else {
            target.show();
            $this.html("[-]Hide Bib");
        }   
    });
    $(".ab_entry").hide();
    $("div.abstract_show_hide").click(function() {
        var $this = $(this),
        target = $this.next(".ab_entry"),
        showing = target.is(':visible');
        if(showing){ // hide
            target.hide();
            $this.html("[+]Show Abstract");
        }
        else {
            target.show();
            $this.html("[-]Hide Abstract");
        }   
    });
});

$(document).ready(function(){$('.nav-tabs a').click(function(){$(this).tab('show');});});