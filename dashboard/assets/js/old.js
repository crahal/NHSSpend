function csvshare() {
    /* Get the text field */
    var copyText = document.getElementById(mapName + "-csvlink").getAttribute("href");

	if (navigator) {
		navigator.clipboard.writeText(copyText).then(function() {
			console.log('Async: Copying to clipboard was successful');
		}, function(err) {
			console.error('Async: Could not copy text: ', err);
		});
		/* Alert the copied text */
		//TODO toast don't alert
		alert("csv data link has been copied to your clipboard: " + copyText);
    }
    else
    {
    	alert("Can't copy link to your clipboard, please share manually" + copyText);
    }
}
