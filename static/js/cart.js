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
