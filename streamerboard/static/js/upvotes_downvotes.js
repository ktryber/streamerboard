// code to execute the upvotes and downvotes


// UPVOTE JQUERY
$(document).on('click','.upvote-btn',function(e){
  e.preventDefault()
  var this_ = $(this)
  var upvoteToggleUrl = this_.attr("data-api-upvote")
  var voteCountAPIUrl = this_.next("#upvote-count").attr("data-upvotes");
  $.ajax({
    url: upvoteToggleUrl,
    method: 'GET',
    data: {},
    success: function(data){
      $.ajax({
        url: voteCountAPIUrl,
        method: 'GET',
        data: {},
        success: function(data){
          console.log(data.upvotes)
          this_.next('#upvote-count').text(data.upvotes);
        }, error: function(error){
          console.log(error)
          console.log("error")
        }
      })
    }, error: function(error){
      console.log(error)
      console.log("error")
    }
  })
})


//DOWNVOTE JQUERY
$(document).on('click','.downvote-btn',function(e){
  e.preventDefault()
  var this_ = $(this)
  var downvoteToggleUrl = this_.attr("data-api-downvote")
  var voteCountAPIUrl = this_.next("#downvote-count").attr("data-downvotes");
  $.ajax({
    url: downvoteToggleUrl,
    method: 'GET',
    data: {},
    success: function(data){
      $.ajax({
        url: voteCountAPIUrl,
        method: 'GET',
        data: {},
        success: function(data){
          console.log(data.downvotes)
          this_.next('#downvote-count').text(data.downvotes);
        }, error: function(error){
          console.log(error)
          console.log("error")
        }
      })
    }, error: function(error){
      console.log(error)
      console.log("error")
    }
  })
})
