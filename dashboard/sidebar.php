<nav class="col-md-2 d-none d-md-block bg-dark sidebar">
	<div class="sidebar-sticky mt-2 p-3 text-light">
		<p>This data is based on quarterly reports from ? CCGs for Q? 20??.</p>
		<?php
        	set_query_var('map-template-id', 'tab1');
        	get_template_part('template-parts/graph/graph', 'tab1-controls');
        ?>
	</div>
</nav>
