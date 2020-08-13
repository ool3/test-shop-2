jQuery(document).ready(function($) {
	$('.block__item__title').click(function(event){
		$(this).toggleClass('active').next().slideToggle(300);
	})
});