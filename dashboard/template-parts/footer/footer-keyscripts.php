<!-- Bootstrap core JavaScript
================================================== -->
<!-- Placed at the end of the document so the pages load faster -->
<!-- //TODO move scripts to our host, check wp jquery -->
<script src="<?php echo get_theme_file_uri('/assets/js/vendor/jquery-3.3.1.slim.min.js'); ?>"></script>
<script src="<?php echo get_theme_file_uri('/assets/js/vendor/popper.min.js'); ?>"></script>
<script src="<?php echo get_theme_file_uri('/assets/js/vendor/bootstrap.min.js'); ?>"></script>
<script src="<?php echo get_theme_file_uri('/assets/js/scrollfix.js'); ?>"></script>

<!-- Icons -->
<script src="<?php echo get_theme_file_uri('/assets/js/vendor/feather.min.js'); ?>"></script>
<script>
	feather.replace()
</script>
<script>
	if (navigator.onLine === false) {
		document.getElementById("offlineIndicator").classList.remove('d-none');
	} else if ('serviceWorker' in navigator) {
	  window.addEventListener('load', function() {
		navigator.serviceWorker.register('/sw.js').then(function(registration) {
		  // Registration was successful
		  console.log('ServiceWorker registration successful with scope: ', registration.scope);
		}, function(err) {
		  // registration failed
		  console.log('ServiceWorker registration failed: ', err);
		});
	  });
	}
</script>
