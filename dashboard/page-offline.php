<?php
	get_header();
	get_template_part('template-parts/navigation/navigation', 'top');
?>
<div class="container-fluid position-absolute top-0 h-100">
	<div class="row h-100">
		<main role="main" class="col-12 col-md-12 ml-sm-auto px-0">
			<div class="d-flex flex-column justify-content-between h-100 px-0">
				<div class="p-4">
					<h1 class="display-4 d-none d-md-block">
						Unavailable
					</h1>
					<h1 class="h4 d-block d-md-none">
						Unavailable
					</h1>
					<p>
						The requested URL is currently not available while offline. Visiting while online will add it
						to your local cache. Any reports you have viewed whilst online will also be cached.
					</p>
				</div>
				<div class="mt-4">
					<?php get_template_part('template-parts/footer/footer', 'authorship'); ?>
				</div>
			</div>
		</main>
	</div>
</div>
<?php
	get_template_part('template-parts/footer/footer', 'keyscripts');
	get_footer();
?>
