// code to execute the upvotes and downvotes

$(".upvote-btn").click(function(e){
  e.preventDefault()
  var this_ = $(this)
  var upvoteToggleUrl = this_.attr("data-href")
  var voteCountAPIUrl = $(".upvote-count").attr("data-href");
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
          $('.upvote-count').text(data.upvotes);
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
