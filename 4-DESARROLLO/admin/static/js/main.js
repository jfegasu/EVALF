$(document).ready(function(){
	$('ul.tabs li a').eq(1).addClass('active');
	$('.secciones article').hide();
	$('.secciones article').eq(0).show();

	$('ul.tabs li a').click(function(){
		$('ul.tabs li a').removeClass('active');
		$(this).addClass('active');
		$('.secciones article').hide();

		var activeTab = $(this).attr('href');
		$(activeTab).show();
		return false;
	});
});