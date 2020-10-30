console.log('hellow world')
//alert(user)
// Upate cart functionality
var updateBtns = document.getElementsByClassName('update-cart')

for (i=0; i < updateBtns.length; i++){
  updateBtns[i].addEventListener('click', function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    console.log('ProductId:', productId, 'Action:', action)

    console.log('User:', user)
    if(user == 'anonymousUser'){
      console.log('User is not authenticated')
    }else{
      updateUserOrder(productId, action)
    }
  })
}

function updateUserOrder(productId, action){
  console.log('User is logged in, sending data ...')

  var URL = '/updated_item/'
  fetch(URL, {
    method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "Accept": "application/json",
        'Content-Type': 'application/json'
  },
      body: JSON.stringify({'productId:':productId, 'action':action}) //JavaScript object of data to POST
  })
  .then((response)=>{
    return response.json()
  })
  .then((data)=>{
    console.log('data:', data)
    //location.reload()
  })
}

$('#quantity').change(function() {
  //var total_value = document.getElementsByClassName("final_total");
  var final_total = this.dataset.total;
  var single_total = this.dataset.single;
  var final_quantity = $('#quantity').val();
  console.log(final_quantity);
  console.log(single_total);
  if (final_quantity>0){
    var final_total_text = '€'+single_total*final_quantity

    $('#final_total').text(final_total_text)
  }

    //document.getElementsByClassName("final_total").submit();
});
