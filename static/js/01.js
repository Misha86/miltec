// JavaScript Document

$(document).ready( function() {
	
	//
	// The Rotator: Fading Images
	// By Dylan Wagstaff, http://www.alohatechsupport.net/webdesignmaui/maui-web-site-design/easy_jquery_auto_image_rotator.html
	//	
	// (en) Creates a Custom Image Fader
	// (de) Erstellt ein Custom Bidershow
	//
	
	//theRotator(); // turn on the rotator
	//$('span.partner_logos_fixed').remove(); // removes the original fixed partner logos
	//$('div.rotator').fadeIn(1000);
	//$('div.rotator ul li').fadeIn(1000); // tweek for IE
	$('div.rotator').remove(); // turn off the rotator
	
	
	
	//
	// Display Funktion
	//		 
	// (en) for the selected view to stay active we use cookies by Klaus Hartl (stilbuero.de)
	// (de) damit die ausgew�hlte Ansicht auf folgenden seiten bestehen bleibt nutzen wir cookies von Klaus Hartl (stilbuero.de)	
	
	// (en) switching the view from list to grid and visa versa - only within the current search results
	// (de) schaltung zwischen der Raster- und Listendarstellung und umgekehrt - nur innerhalb einer seite
		
	// (en) set the desired on-load view mode
	// (de) die gew�nschte Ansicht voreinstellen, die mit der seite geladen wird
	
	//var currentView = $.cookie('currentView');
	//if (currentView == null) {
	//	$(".display-viewStandard").addClass('display-viewStandard-active');
	//	$(".viewGrid").addClass('viewStandard');
	//	$(".viewGrid").removeClass('viewGrid');
	//	$(".display-viewGrid-active").removeClass('display-viewGrid-active');
	//	//$(".viewGrid, .sortOptions-viewGrid").hide();
	//};
	
	
	
	
	//
	// Activate prettyPhoto 3.1.2 http://www.no-margin-for-errors.com/projects/prettyphoto-jquery-lightbox-clone/
	//			
	
	$("a[rel^='prettyPhoto']").prettyPhoto({
		theme: 'pp_default',	/* pp_default / light_rounded / dark_rounded / light_square / dark_square / facebook */
		hideflash: false, /* Hides all the flash object on a page, set to TRUE if flash appears over prettyPhoto */
		social_tools: false, /* html or false to disable */
		deeplinking: false, /* Allow prettyPhoto to update the url to enable deeplinking. */			
		ie6_fallback: true,
		overlay_gallery: false /* If set to true, a gallery will overlay the fullscreen image on mouse over */,
		iframe_markup:'<div class="iOSscroll" style="width:{width}px;height:{height}px;"><iframe src ="{path}" width="{width}" height="{height}" frameborder="no"></iframe></div>' /* Bugfix for iOS Touch devices to be able to scroll */
	});



	//
	// JQZoom Evolution 1.0.1 - Javascript Image magnifier http://www.mind-projects.it/projects/jqzoom/
			
				
	var jqZoomOptions = {
		zoomWidth: 450,
		zoomHeight: 400,
		showEffect:'fadein',
		hideEffect:'fadeout',
		fadeoutSpeed: 'slow',
		fadeinSpeed: 'slow',
		zoomType:'reverse',
		showPreload: true,
		preloadText: 'Zoombild laden',
		title: true
	};
	$("#main div.imageContainer .jqzoom").jqzoom(jqZoomOptions);

});