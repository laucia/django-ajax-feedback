/**
 * Toggle the overlay display
 */
function toggle_feedback(){
	var $overlay = $('#overlay');
	var $feedback_panel = $('#feedback_panel');
	if($overlay.css('display') == 'block'){
		$overlay.css('display','none');
		$feedback_panel.css('display','none');
	} else {
		$overlay.css('display','block');
		$feedback_panel.css('display','block');
	}
}

/**
 * Load the feedback form into the #feedback_contents tag.
 * Form url is to be given to benefit from Django reverse urls.
 */
function load_contents(url){
	var $contents = $('#feedback_contents');
	$contents.empty();
	$contents.load(url, function(response, status, xhr){
		if(status == 'success'){
			var options = {
				dataType: 'json',
				success: process_json,
				beforeSubmit: before_form
			};
			var $form = $contents.children('form')
			$form.ajaxForm(options)
			toggle_feedback();
		}
	});
}

/**
 * Function to be executed before a form is submited
 */
function before_form(arr, $form, options) { 
	var $parent = $form.parent();
	$parent.children('.messages').empty(); //Get rid of any old errors
	return true;
}

/**
 * Function called when form response is received
 * The form should respond with json data
 */
function process_json(data, statusText, xhr, $form) {
	var $parent = $form.parent();
	if (data) {
		var success = data.success;
 		if(success) {
			$parent.children('.messages').append('<li class="success">' + success + '</li>');
			$form.remove()
			window.setTimeout(toggle_feedback,1500)
		} else {
			var errors = eval(data.errors)
			$.each(errors,function(fieldname,errmsg)
			{
				$parent.children('.messages').append('<li class="error">' + fieldname + ': ' + errmsg + '</li>');
			});
		}
	} else {
		$parent.children('.messages').append('<li class="error">Ajax error: no data received.</li>');
	}
}