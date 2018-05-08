/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
$('.form-group').removeClass('row');


// nothing

console.log("nothing")
// AJAX for posting
function create_post() {
    console.log("create post is working!") // sanity check
    $.ajax({
        url : "streams/create_post/", // the endpoint
        type : "POST", // http method
        data : {
          stream_title : $('#stream-title').val(),
          stream_description : $('#stream-description').val(),
        },

        // handle a successful response
        success : function(json) {
            $('#stream-title').val(''); // remove the value from the input
            $('#stream-description').val('');
            console.log(json); // log the returned json to the console
            $('#stream-list').prepend(
              "<div class='post-list-box'><h1>"+json.title+"</h1><h4>"+json.description+"</h4>"+
              "<a class='btn btn-warning' href='/streams/detail/"+json.postpk+"/'>View Stream</a><p>comment area</p>Upvotes: "+json.up_votes+
              " Downvotes: "+json.down_votes+"</div>"
            )
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

// Submit post on Submit
$('#add-stream-form').on('submit', function(event){
  event.preventDefault();
  console.log("form submitted!")
  create_post();

})
