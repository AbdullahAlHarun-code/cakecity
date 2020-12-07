console.log('hellow world')
//alert(user)
// Upate cart functionality
var updateBtns = document.getElementsByClassName('update-cart')

$(".update-cart").click(function () {
	var productId = this.dataset.product;
	var action = this.dataset.action;
	var total = this.dataset.total;
	var flavour = this.dataset.flavour;
	var quantity = $('.quantity').val();
	console.log('ProductId:', productId, 'Action:', action)

	console.log('User:', user)
	if (user == 'anonymousUser') {
		console.log('User is not authenticated')
	} else {
		updateUserOrder(productId, action, total, flavour, quantity)
	}
});

// change quantity function
check_quantity();
$('#item_quantity').keyup(function(){
	check_quantity();
  });
$('.update_quantity').keyup(function(){
	//alert($(this).val())
	checkQuantity($(this).attr('input_data_id'));
  });

function check_quantity(){
	quantity = $('#item_quantity').val();
	if (quantity>0){
		$('#add_to_cart').removeAttr('disabled');
	}else{
		$('#add_to_cart').attr('disabled','disabled');
	}
}
function checkQuantity(id){
	quantity_id = '#item_'+id;
	update_id = '#update_item_'+id;
	quantity = $(quantity_id).val();
	if (quantity>0){
		$(update_id).removeAttr('disabled');
	}else{
		$(update_id).attr('disabled','disabled');
	}
}


// for (i=0; i < updateBtns.length; i++){
//   updateBtns[i].addEventListener('click', function(){
//     var productId = this.dataset.product;
//     var action = this.dataset.action;
//     var total = this.dataset.total;
//     var flavour = this.dataset.flavour;
//     var quantity = document.getElementById('quantity').value
//     console.log('ProductId:', productId, 'Action:', action)
//
//     console.log('User:', user)
//     if(user == 'anonymousUser'){
//       console.log('User is not authenticated')
//     }else{
//       updateUserOrder(productId, action, total, flavour, quantity)
//     }
//   })
// }

function updateUserOrder(productId, action, total, flavour, quantity) {
	console.log('User is logged in, sending data ...');

	var URL = '/updated_item/';
	fetch(URL, {
			method: "POST",
			headers: {
				"X-CSRFToken": csrftoken,
				"Accept": "application/json",
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				'productId:': productId,
				'action': action,
				'flavour': flavour,
				'total': total,
				'quantity': quantity
			}) //JavaScript object of data to POST
		})
		.then((response) => {
			return response.json()
		})
		.then((data) => {
			console.log('data:', data)
			//location.reload()
		})
}

$('#quantity').change(function () {
	//var total_value = document.getElementsByClassName("final_total");
	var final_total = this.dataset.total;
	var single_total = this.dataset.single;
	var final_quantity = $('#quantity').val();
	console.log(final_quantity);
	console.log(single_total);
	if (final_quantity > 0) {
		var final_total_text = '€' + single_total * final_quantity

		$('#final_total').text(final_total_text)
	}

	//document.getElementsByClassName("final_total").submit();
});
$('#add_to_cart').click(function () {
	$('#add_item_form').attr('action', $('#form_url').val());
	$('#add_item_form').submit();
});
$('.toast').toast('show');
