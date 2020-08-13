jQuery(document).ready(function($) {
		if($(window).width() < 991){
			$('img.card-img-top').css('object-fit', 'cover')
			$('img.card-img-top').css('height', '280px')
			$('#div1').removeClass().addClass('col-9')
			$('#div2').removeClass().addClass('col-3')
			let row = $('#content')
			row.removeClass('row-cols-1')
			row.removeClass('row-cols-md-3')
			console.log(row)
		}else if ($(window).width() > 1199) {
			$('#div1').removeClass().addClass('col-6')
			$('#div2').removeClass().addClass('col-6')
		} else if ($(window).width() > 992) {
			$('img.card-img-top').css('height', '280px')
			$('img.card-img-top').css('object-fit', 'contain')
			$('#div1').removeClass().addClass('col-7')
			$('#div2').removeClass().addClass('col-5')
		}
		

});